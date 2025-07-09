import json
import logging
import os
from datetime import datetime, timezone
from typing import Any, Dict

import psutil
from fastapi import FastAPI, HTTPException, Request
from pydantic import BaseModel, Field

API_VERSION = "1.0.0"

app = FastAPI(
    title="Linux Resources Monitoring API",
    description="API for ingesting and monitoring Linux system metrics",
    version=API_VERSION,
)


class MetricsPayload(BaseModel):
    timestamp: str = Field(..., description="UTC ISO timestamp")
    hostname: str = Field(..., description="Hostname of the sender")
    metrics: Dict[str, Any] = Field(..., description="System metrics")


class HealthResponse(BaseModel):
    status: str = Field(..., description="Health status")
    timestamp: str = Field(..., description="UTC ISO timestamp")
    version: str = Field(..., description="API version")
    uptime: float = Field(..., description="Uptime in seconds")


class DetailedHealthResponse(HealthResponse):
    system_info: Dict[str, Any] = Field(..., description="System information")
    memory_usage: Dict[str, Any] = Field(..., description="Memory usage statistics")
    disk_usage: Dict[str, Any] = Field(..., description="Disk usage statistics")


class JSONLogFormatter(logging.Formatter):
    def format(self, record):
        log_record = {
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "level": record.levelname,
            "message": record.getMessage(),
        }
        if isinstance(record.msg, dict):
            log_record.update(record.msg)
        return json.dumps(log_record)


logger = logging.getLogger("CloudIngestion")
logger.setLevel(logging.INFO)
handler = logging.StreamHandler()
handler.setFormatter(JSONLogFormatter())
if not logger.hasHandlers():
    logger.addHandler(handler)

# Track startup time for uptime calculation
startup_time = datetime.now(timezone.utc)


@app.get("/health", response_model=HealthResponse)
async def health_check():
    """
    Basic health check endpoint.
    Returns 200 if the service is running.
    """
    uptime = (datetime.now(timezone.utc) - startup_time).total_seconds()
    return HealthResponse(
        status="healthy",
        timestamp=datetime.now(timezone.utc).isoformat(),
        version=API_VERSION,
        uptime=uptime,
    )


@app.get("/health/ready", response_model=HealthResponse)
async def readiness_check():
    """
    Readiness check endpoint.
    Returns 200 if the service is ready to accept requests.
    """
    uptime = (datetime.now(timezone.utc) - startup_time).total_seconds()
    return HealthResponse(
        status="ready",
        timestamp=datetime.now(timezone.utc).isoformat(),
        version=API_VERSION,
        uptime=uptime,
    )


@app.get("/health/live", response_model=HealthResponse)
async def liveness_check():
    """
    Liveness check endpoint.
    Returns 200 if the service is alive and responsive.
    """
    uptime = (datetime.now(timezone.utc) - startup_time).total_seconds()
    return HealthResponse(
        status="alive",
        timestamp=datetime.now(timezone.utc).isoformat(),
        version=API_VERSION,
        uptime=uptime,
    )


@app.get("/health/detailed", response_model=DetailedHealthResponse)
async def detailed_health_check():
    """
    Detailed health check endpoint.
    Returns comprehensive system information and health status.
    """
    try:
        # Get system information
        system_info = {
            "hostname": os.uname().nodename,
            "platform": os.uname().sysname,
            "release": os.uname().release,
            "version": os.uname().version,
            "machine": os.uname().machine,
            "cpu_count": psutil.cpu_count(),
            "cpu_percent": psutil.cpu_percent(interval=1),
        }

        # Get memory information
        memory = psutil.virtual_memory()
        memory_usage = {
            "total_gb": round(memory.total / (1024**3), 2),
            "available_gb": round(memory.available / (1024**3), 2),
            "used_gb": round(memory.used / (1024**3), 2),
            "percent": memory.percent,
        }

        # Get disk information
        disk = psutil.disk_usage("/")
        disk_usage = {
            "total_gb": round(disk.total / (1024**3), 2),
            "used_gb": round(disk.used / (1024**3), 2),
            "free_gb": round(disk.free / (1024**3), 2),
            "percent": disk.percent,
        }

        uptime = (datetime.now(timezone.utc) - startup_time).total_seconds()

        return DetailedHealthResponse(
            status="healthy",
            timestamp=datetime.now(timezone.utc).isoformat(),
            version=API_VERSION,
            uptime=uptime,
            system_info=system_info,
            memory_usage=memory_usage,
            disk_usage=disk_usage,
        )
    except Exception as e:
        logger.error({"event": "health_check_error", "error": str(e)})
        raise HTTPException(status_code=500, detail=f"Health check failed: {str(e)}")


@app.get("/")
async def root():
    """
    Root endpoint with API information.
    """
    return {
        "message": "Linux Resources Monitoring API",
        "version": API_VERSION,
        "endpoints": {
            "health": "/health",
            "readiness": "/health/ready",
            "liveness": "/health/live",
            "detailed_health": "/health/detailed",
            "metrics": "/api/metrics",
            "docs": "/docs",
        },
    }


@app.post("/api/metrics")
async def receive_metrics(payload: MetricsPayload, request: Request):
    """
    Receive system metrics as JSON payload and log them in structured format.
    """
    log_data = payload.model_dump()
    log_data["client_host"] = request.client.host
    logger.info({"event": "metrics_received", **log_data})
    return {
        "status": "ok",
        "received_at": datetime.now(timezone.utc).isoformat(),
        "hostname": payload.hostname,
    }


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
