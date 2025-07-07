# Deployment: Systemd & Docker

## Systemd Service (Production)

1. Copy `deployment/monitor.service` to `/etc/systemd/system/monitor.service`:
   ```bash
   sudo cp deployment/monitor.service /etc/systemd/system/monitor.service
   ```
2. Edit the `User`, `WorkingDirectory`, and `ExecStart` fields in the service file to match your environment.
3. Reload systemd and start the service:
   ```bash
   sudo systemctl daemon-reload
   sudo systemctl enable monitor
   sudo systemctl start monitor
   sudo systemctl status monitor
   ```

## Docker (Local Development & Testing)

1. Build the Docker image:
   ```bash
   docker build -t linux-resources-monitoring-service .
   ```
2. Run the container:
   ```bash
   docker run --rm linux-resources-monitoring-service
   ```

## Troubleshooting
- Check logs: `journalctl -u monitor` (systemd) or `docker logs <container>`
- Ensure all paths in the service file are absolute (no `~`)
- For more, see [docs/RELIABILITY.md](RELIABILITY.md)
