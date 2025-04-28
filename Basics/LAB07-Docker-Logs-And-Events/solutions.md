# LAB07: Docker Logs and Events - Solutions

This document provides solutions to the exercises in LAB07. Only consult these solutions after attempting to solve the problems yourself.

## Task 3: Log Exploration and Analysis

### Building and running the logging demo application

```bash
cd logging-demo
docker build -t logging-demo .
docker run -d --name logging-app logging-demo
```

### Exploring logs with different filtering options

```bash
# Filter logs by timestamp
docker logs --since 2023-01-01T00:00:00 logging-app
docker logs --until 2023-01-01T23:59:59 logging-app

# Filter logs by error level (using grep)
docker logs logging-app | grep ERROR
docker logs logging-app | grep WARN
docker logs logging-app | grep INFO

# Search for specific text patterns
docker logs logging-app | grep "Connection"
docker logs logging-app | grep "Failed to"
docker logs logging-app | grep -E "timeout|connection refused"
```

### Analyzing logs with command-line tools

```bash
# Count error occurrences
docker logs logging-app | grep ERROR | wc -l

# Extract and analyze timing information
docker logs logging-app | grep "processing time" | awk '{print $NF}' > processing_times.txt
# Calculate average processing time
awk '{ sum += $1; count++ } END { print sum/count }' processing_times.txt

# Create a summary of errors
docker logs logging-app | grep ERROR | sort | uniq -c | sort -nr > error_summary.txt
```

### Improving application logging

Modify the `app.py` file to include structured logging:

```python
import logging
import json
import time
import uuid
import os

# Configure structured logging
class StructuredMessage:
    def __init__(self, message, **kwargs):
        self.message = message
        self.kwargs = kwargs

    def __str__(self):
        return f"{self.message} {json.dumps(self.kwargs)}"

# Configure the logger
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)

# Create structured logger
logger = logging.getLogger(__name__)

def log_event(level, message, **kwargs):
    """Log a structured message with context."""
    # Add common context to all logs
    kwargs['hostname'] = os.uname()[1]
    kwargs['pid'] = os.getpid()
    kwargs['request_id'] = str(uuid.uuid4())
    
    # Log with appropriate level
    log_func = getattr(logger, level.lower())
    log_func(StructuredMessage(message, **kwargs))

# Example usage
log_event('info', 'Application started', version='1.0.0', environment='production')
log_event('error', 'Database connection failed', db_host='db.example.com', retry_count=3)
```

## Task 5: Working with Events in Real-Time

### Event monitoring script

Create a Python script `docker_event_monitor.py`:

```python
#!/usr/bin/env python3
"""
Docker Event Monitor

This script monitors Docker events and takes actions based on specific events.
"""

import json
import subprocess
import sys
import time
import os
import smtplib
from email.message import EmailMessage
from datetime import datetime

# Configuration
LOG_FILE = "docker_events.log"
STATS_FILE = "event_stats.json"
ALERT_EMAIL = "admin@example.com"  # Change to your email

def log_event(event_data):
    """Log the event to a file."""
    with open(LOG_FILE, "a") as f:
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        f.write(f"{timestamp} - {json.dumps(event_data)}\n")

def update_stats(event_data):
    """Update event statistics."""
    # Load existing stats or create new
    if os.path.exists(STATS_FILE):
        with open(STATS_FILE, "r") as f:
            try:
                stats = json.load(f)
            except json.JSONDecodeError:
                stats = {"container": {}, "image": {}, "volume": {}, "network": {}}
    else:
        stats = {"container": {}, "image": {}, "volume": {}, "network": {}}
    
    # Update stats
    event_type = event_data.get("Type", "unknown")
    event_action = event_data.get("Action", "unknown")
    
    if event_type not in stats:
        stats[event_type] = {}
    
    if event_action not in stats[event_type]:
        stats[event_type][event_action] = 1
    else:
        stats[event_type][event_action] += 1
    
    # Save updated stats
    with open(STATS_FILE, "w") as f:
        json.dump(stats, f, indent=2)

def send_alert(event_data, message):
    """Send an email alert for critical events."""
    # In a real implementation, configure actual email sending
    print(f"ALERT: {message}")
    print(f"Event details: {json.dumps(event_data, indent=2)}")
    
    # Simulated email sending (replace with actual implementation)
    # msg = EmailMessage()
    # msg.set_content(f"Docker Event Alert:\n{message}\n\nEvent details: {json.dumps(event_data, indent=2)}")
    # msg['Subject'] = 'Docker Event Alert'
    # msg['From'] = 'docker-monitor@example.com'
    # msg['To'] = ALERT_EMAIL
    # server = smtplib.SMTP('smtp.example.com')
    # server.send_message(msg)
    # server.quit()

def handle_event(event_data):
    """Process an event and take appropriate actions."""
    event_type = event_data.get("Type", "")
    event_action = event_data.get("Action", "")
    
    # Log all events
    log_event(event_data)
    
    # Update statistics
    update_stats(event_data)
    
    # Handle container events
    if event_type == "container":
        container_name = event_data.get("Actor", {}).get("Attributes", {}).get("name", "unknown")
        
        if event_action == "start":
            print(f"Container started: {container_name}")
        
        elif event_action == "die":
            exit_code = event_data.get("Actor", {}).get("Attributes", {}).get("exitCode", "")
            if exit_code != "0":
                send_alert(
                    event_data, 
                    f"Container {container_name} exited with non-zero code: {exit_code}"
                )
        
        elif event_action == "oom":
            send_alert(
                event_data,
                f"Container {container_name} ran out of memory (OOM killed)"
            )
    
    # Handle image events
    elif event_type == "image":
        image_name = event_data.get("Actor", {}).get("Attributes", {}).get("name", "unknown")
        
        if event_action == "delete":
            print(f"Image deleted: {image_name}")
        
        elif event_action == "pull":
            print(f"Image pulled: {image_name}")
    
    # Handle volume events
    elif event_type == "volume":
        volume_name = event_data.get("Actor", {}).get("Attributes", {}).get("name", "unknown")
        
        if event_action == "create":
            print(f"Volume created: {volume_name}")
        
        elif event_action == "destroy":
            print(f"Volume deleted: {volume_name}")
    
    # Handle network events
    elif event_type == "network":
        network_name = event_data.get("Actor", {}).get("Attributes", {}).get("name", "unknown")
        
        if event_action == "create":
            print(f"Network created: {network_name}")
        
        elif event_action == "destroy":
            print(f"Network deleted: {network_name}")

def generate_report():
    """Generate a report of collected event statistics."""
    if not os.path.exists(STATS_FILE):
        print("No statistics collected yet.")
        return
    
    with open(STATS_FILE, "r") as f:
        stats = json.load(f)
    
    report = ["# Docker Event Statistics Report", ""]
    report.append(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    report.append("")
    
    for event_type, actions in stats.items():
        report.append(f"## {event_type.capitalize()} Events")
        for action, count in actions.items():
            report.append(f"- {action}: {count}")
        report.append("")
    
    report_content = "\n".join(report)
    
    with open("event_report.md", "w") as f:
        f.write(report_content)
    
    print("Report generated: event_report.md")

def main():
    """Main function to monitor Docker events."""
    if len(sys.argv) > 1 and sys.argv[1] == "--report":
        generate_report()
        return
    
    print("Starting Docker event monitor...")
    print(f"Logging events to: {LOG_FILE}")
    
    try:
        # Run docker events command with JSON output
        cmd = ["docker", "events", "--format", "{{json .}}"]
        process = subprocess.Popen(cmd, stdout=subprocess.PIPE, text=True)
        
        # Process each event as it occurs
        for line in process.stdout:
            try:
                event_data = json.loads(line.strip())
                handle_event(event_data)
            except json.JSONDecodeError:
                print(f"Error parsing event: {line}")
    
    except KeyboardInterrupt:
        print("\nMonitoring stopped.")
    
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()
```

### Testing the event monitoring script

Run the script in one terminal:

```bash
python docker_event_monitor.py
```

Generate events in another terminal:

```bash
# Create a container
docker run --name test-container -d nginx

# Stop the container
docker stop test-container

# Remove the container
docker rm test-container

# Pull an image
docker pull alpine

# Create a volume
docker volume create test-volume

# Remove the volume
docker volume rm test-volume
```

### Generate a report

```bash
python docker_event_monitor.py --report
```

## Task 6: Log Rotation and Management

### Configure log rotation with Docker's built-in options

Edit or create `/etc/docker/daemon.json`:

```json
{
  "log-driver": "json-file",
  "log-opts": {
    "max-size": "10m",
    "max-file": "3"
  }
}
```

Restart Docker service:

```bash
sudo systemctl restart docker
```

Run containers with specific log options:

```bash
docker run -d --log-opt max-size=5m --log-opt max-file=2 --name nginx-with-rotation nginx
```

### Implement a log cleanup policy

Create a script `cleanup_logs.sh`:

```bash
#!/bin/bash
# Docker log cleanup script

# Configuration
LOG_DIR="/var/lib/docker/containers"
MAX_AGE_DAYS=7
DRY_RUN=false

# Print usage information
usage() {
    echo "Usage: $0 [OPTIONS]"
    echo "Cleanup old Docker container logs"
    echo ""
    echo "Options:"
    echo "  --dry-run     Show what would be deleted without actually deleting"
    echo "  --days NUM    Delete logs older than NUM days (default: 7)"
    echo "  --help        Show this help message"
    exit 1
}

# Parse command-line arguments
while [[ $# -gt 0 ]]; do
    case "$1" in
        --dry-run)
            DRY_RUN=true
            shift
            ;;
        --days)
            MAX_AGE_DAYS="$2"
            shift 2
            ;;
        --help)
            usage
            ;;
        *)
            echo "Unknown option: $1"
            usage
            ;;
    esac
done

# Check if running as root
if [[ $EUID -ne 0 ]]; then
    echo "This script must be run as root"
    exit 1
fi

# Find container directories
echo "Scanning for container log directories..."
CONTAINER_DIRS=$(find "$LOG_DIR" -mindepth 1 -maxdepth 1 -type d)

# Process each container directory
for DIR in $CONTAINER_DIRS; do
    CONTAINER_ID=$(basename "$DIR")
    echo "Processing container: $CONTAINER_ID"
    
    # Find log files older than MAX_AGE_DAYS
    OLD_LOGS=$(find "$DIR" -name "*.log.*" -type f -mtime +$MAX_AGE_DAYS)
    
    if [[ -z "$OLD_LOGS" ]]; then
        echo "  No old logs found"
        continue
    fi
    
    # Process each old log file
    for LOG_FILE in $OLD_LOGS; do
        LOG_SIZE=$(du -h "$LOG_FILE" | cut -f1)
        if [[ "$DRY_RUN" == true ]]; then
            echo "  Would delete: $LOG_FILE (size: $LOG_SIZE)"
        else
            echo "  Deleting: $LOG_FILE (size: $LOG_SIZE)"
            rm "$LOG_FILE"
        fi
    done
done

echo "Log cleanup completed"
```

Make the script executable:

```bash
chmod +x cleanup_logs.sh
```

### Set up a cron job for log cleanup

```bash
sudo crontab -e
```

Add the following line to run the cleanup script daily at 3 AM:

```
0 3 * * * /path/to/cleanup_logs.sh --days 7 >> /var/log/docker-log-cleanup.log 2>&1
```

### Archive logs before deletion

Modify the cleanup script to archive logs before deletion:

```bash
# Inside the loop processing log files
for LOG_FILE in $OLD_LOGS; do
    LOG_SIZE=$(du -h "$LOG_FILE" | cut -f1)
    ARCHIVE_NAME="$(basename "$LOG_FILE").$(date +%Y%m%d).gz"
    
    if [[ "$DRY_RUN" == true ]]; then
        echo "  Would archive and delete: $LOG_FILE (size: $LOG_SIZE)"
    else
        echo "  Archiving: $LOG_FILE to /var/log/docker-archives/$ARCHIVE_NAME"
        # Create archive directory if it doesn't exist
        mkdir -p /var/log/docker-archives
        # Compress the log file
        gzip -c "$LOG_FILE" > "/var/log/docker-archives/$ARCHIVE_NAME"
        # Delete the original
        rm "$LOG_FILE"
    fi
done
```

## Task 7: Centralized Logging for Containers

### Set up an ELK stack for centralized logging

Create a `docker-compose.yml` file:

```yaml
version: '3'

services:
  elasticsearch:
    image: docker.elastic.co/elasticsearch/elasticsearch:7.17.0
    environment:
      - discovery.type=single-node
      - "ES_JAVA_OPTS=-Xms512m -Xmx512m"
    volumes:
      - es_data:/usr/share/elasticsearch/data
    ports:
      - "9200:9200"
    networks:
      - logging

  logstash:
    image: docker.elastic.co/logstash/logstash:7.17.0
    volumes:
      - ./logstash/pipeline:/usr/share/logstash/pipeline
      - ./logstash/config/logstash.yml:/usr/share/logstash/config/logstash.yml
    ports:
      - "5044:5044"
      - "5000:5000/tcp"
      - "5000:5000/udp"
      - "9600:9600"
    networks:
      - logging
    depends_on:
      - elasticsearch

  kibana:
    image: docker.elastic.co/kibana/kibana:7.17.0
    environment:
      - ELASTICSEARCH_HOSTS=http://elasticsearch:9200
    ports:
      - "5601:5601"
    networks:
      - logging
    depends_on:
      - elasticsearch

volumes:
  es_data:

networks:
  logging:
    driver: bridge
```

Create Logstash configuration:

```bash
mkdir -p logstash/config logstash/pipeline
```

Create `logstash/config/logstash.yml`:

```yaml
http.host: "0.0.0.0"
```

Create `logstash/pipeline/docker.conf`:

```
input {
  gelf {
    port => 5000
  }
}

filter {
  json {
    source => "message"
  }
}

output {
  elasticsearch {
    hosts => ["elasticsearch:9200"]
    index => "docker-logs-%{+YYYY.MM.dd}"
  }
  stdout { codec => rubydebug }
}
```

Start the ELK stack:

```bash
docker-compose up -d
```

### Configure Docker to use the GELF logging driver

Edit `/etc/docker/daemon.json`:

```json
{
  "log-driver": "gelf",
  "log-opts": {
    "gelf-address": "udp://localhost:5000",
    "tag": "{{.Name}}/{{.ID}}"
  }
}
```

Restart Docker:

```bash
sudo systemctl restart docker
```

Run a container with GELF logging:

```bash
docker run -d --log-driver=gelf --log-opt gelf-address=udp://localhost:5000 --name gelf-test nginx
```

## Task 8: Logging Best Practices

### Best practices document

Create a file `logging_best_practices.md`:

```markdown
# Docker Container Logging Best Practices

## Log Format Standardization

1. **Use structured logging**
   - Log in JSON format for machine-readable logs
   - Include consistent fields across all services
   - Required fields: timestamp, service name, log level, message

2. **Include context with every log entry**
   - Request ID / Correlation ID for request tracing
   - User ID when applicable (anonymized if needed)
   - Resource identifiers (container ID, pod name, etc.)
   - Environment information

3. **Use appropriate log levels**
   - ERROR: Fatal errors that cause application failure
   - WARN: Non-fatal issues that require attention
   - INFO: Important operational events
   - DEBUG: Detailed information for troubleshooting
   - TRACE: Very detailed debugging information

## Sensitive Data Handling

1. **Never log sensitive information**
   - Passwords, API keys, tokens
   - Personal Identifiable Information (PII)
   - Financial information
   - Health information

2. **Implement data masking for sensitive fields**
   - Use patterns like `xxxx-xxxx-xxxx-1234` for card numbers
   - Hash or redact sensitive values
   - Implement masking at the logger level

3. **Audit logs for sensitive data exposure**
   - Regularly scan logs for sensitive data patterns
   - Implement automated detection tools

## Storage and Retention

1. **Implement appropriate retention policies**
   - Retain logs based on importance
     - Critical service logs: 90+ days
     - Standard application logs: 30 days
     - Debug logs: 7 days
   - Consider compliance requirements (GDPR, HIPAA, etc.)

2. **Compress and archive old logs**
   - Compress logs older than 24 hours
   - Archive to cost-effective storage
   - Maintain index for searchability

3. **Implement log rotation**
   - Rotate logs based on size and time
   - Recommended settings:
     - max-size: 100MB
     - max-file: 3-5 files

## Operational Best Practices

1. **Configure logging during container deployment**
   - Set appropriate logging driver
   - Configure log limits
   - Apply appropriate tags

2. **Monitor log storage usage**
   - Set up alerts for excessive log volume
   - Watch for storage issues
   - Detect abnormal logging patterns

3. **Implement centralized logging**
   - Collect logs from all containers in one place
   - Use standardized collection methods
   - Ensure proper access controls

4. **Optimize logging performance**
   - Use asynchronous logging when possible
   - Buffer logs during high-load periods
   - Consider sampling for high-volume debug logs

5. **Implement log-based alerting**
   - Alert on error frequency
   - Alert on critical errors
   - Alert on missing logs
```

## Task 9: Building a Comprehensive Monitoring Solution

### Docker Monitoring Dashboard with Prometheus and Grafana

Create a `docker-compose.yml` file:

```yaml
version: '3'

services:
  prometheus:
    image: prom/prometheus:latest
    volumes:
      - ./prometheus/prometheus.yml:/etc/prometheus/prometheus.yml
    ports:
      - "9090:9090"
    networks:
      - monitoring

  cadvisor:
    image: gcr.io/cadvisor/cadvisor:latest
    volumes:
      - /:/rootfs:ro
      - /var/run:/var/run:ro
      - /sys:/sys:ro
      - /var/lib/docker/:/var/lib/docker:ro
      - /dev/disk/:/dev/disk:ro
    ports:
      - "8080:8080"
    networks:
      - monitoring

  node-exporter:
    image: prom/node-exporter:latest
    volumes:
      - /proc:/host/proc:ro
      - /sys:/host/sys:ro
      - /:/rootfs:ro
    command:
      - '--path.procfs=/host/proc'
      - '--path.sysfs=/host/sys'
      - '--collector.filesystem.ignored-mount-points=^/(sys|proc|dev|host|etc)($$|/)'
    ports:
      - "9100:9100"
    networks:
      - monitoring

  alertmanager:
    image: prom/alertmanager:latest
    volumes:
      - ./alertmanager/config.yml:/etc/alertmanager/config.yml
    ports:
      - "9093:9093"
    networks:
      - monitoring

  grafana:
    image: grafana/grafana:latest
    volumes:
      - grafana_data:/var/lib/grafana
      - ./grafana/provisioning:/etc/grafana/provisioning
    environment:
      - GF_SECURITY_ADMIN_PASSWORD=admin
      - GF_USERS_ALLOW_SIGN_UP=false
    ports:
      - "3000:3000"
    networks:
      - monitoring
    depends_on:
      - prometheus

  elasticsearch:
    image: docker.elastic.co/elasticsearch/elasticsearch:7.17.0
    environment:
      - discovery.type=single-node
      - "ES_JAVA_OPTS=-Xms512m -Xmx512m"
    volumes:
      - es_data:/usr/share/elasticsearch/data
    ports:
      - "9200:9200"
    networks:
      - monitoring

  logstash:
    image: docker.elastic.co/logstash/logstash:7.17.0
    volumes:
      - ./logstash/pipeline:/usr/share/logstash/pipeline
      - ./logstash/config/logstash.yml:/usr/share/logstash/config/logstash.yml
    ports:
      - "5044:5044"
      - "5000:5000/tcp"
      - "5000:5000/udp"
    networks:
      - monitoring
    depends_on:
      - elasticsearch

  kibana:
    image: docker.elastic.co/kibana/kibana:7.17.0
    environment:
      - ELASTICSEARCH_HOSTS=http://elasticsearch:9200
    ports:
      - "5601:5601"
    networks:
      - monitoring
    depends_on:
      - elasticsearch

  event-monitor:
    build:
      context: ./event-monitor
    volumes:
      - /var/run/docker.sock:/var/run/docker.sock
    networks:
      - monitoring
    depends_on:
      - elasticsearch

volumes:
  grafana_data:
  es_data:

networks:
  monitoring:
    driver: bridge
```

### Create Prometheus configuration

```yaml
global:
  scrape_interval: 15s
  evaluation_interval: 15s

alerting:
  alertmanagers:
    - static_configs:
        - targets:
            - alertmanager:9093

rule_files:
  - "alert_rules.yml"

scrape_configs:
  - job_name: 'prometheus'
    static_configs:
      - targets: ['localhost:9090']

  - job_name: 'cadvisor'
    static_configs:
      - targets: ['cadvisor:8080']

  - job_name: 'node-exporter'
    static_configs:
      - targets: ['node-exporter:9100']
```

### Create alert rules

```yaml
groups:
  - name: docker_alerts
    rules:
      - alert: ContainerDown
        expr: absent(container_last_seen{name="important-container"})
        for: 1m
        labels:
          severity: critical
        annotations:
          summary: "Container Down: {{ $labels.name }}"
          description: "Container {{ $labels.name }} has been down for more than 1 minute."

      - alert: HighCPUUsage
        expr: sum(rate(container_cpu_usage_seconds_total{name!=""}[1m])) by (name) > 0.8
        for: 1m
        labels:
          severity: warning
        annotations:
          summary: "High CPU Usage: {{ $labels.name }}"
          description: "Container {{ $labels.name }} has CPU usage above 80% for more than 1 minute."

      - alert: HighMemoryUsage
        expr: container_memory_usage_bytes{name!=""} / container_spec_memory_limit_bytes{name!=""} * 100 > 90
        for: 1m
        labels:
          severity: warning
        annotations:
          summary: "High Memory Usage: {{ $labels.name }}"
          description: "Container {{ $labels.name }} is using more than 90% of its memory limit."
```

## Task 10: Troubleshooting with Logs and Events

### Scenario 1: Application Container Crashing

1. Check container status:
   ```bash
   docker ps -a | grep app-container
   ```

2. Check exit code:
   ```bash
   docker inspect app-container | grep ExitCode
   ```

3. View container logs:
   ```bash
   docker logs app-container
   ```

4. Check for OOM events:
   ```bash
   docker events --filter type=container --filter event=oom
   ```

5. Solution:
   ```bash
   # Increase container memory limit
   docker run -d --name app-container --memory=512m --restart=on-failure app-image
   ```

### Scenario 2: Database Connection Issues

1. Check application logs:
   ```bash
   docker logs app-container | grep -i "database\|connection\|timeout"
   ```

2. Verify network connectivity:
   ```bash
   docker exec app-container ping db-container
   ```

3. Check if database container is running:
   ```bash
   docker ps | grep db-container
   ```

4. Check database logs:
   ```bash
   docker logs db-container
   ```

5. Solution:
   ```bash
   # Ensure containers are on the same network
   docker network create app-network
   docker network connect app-network app-container
   docker network connect app-network db-container
   
   # Restart the application
   docker restart app-container
   ```

### Scenario 3: Volume Mount Issues

1. Check container configuration:
   ```bash
   docker inspect app-container | grep -A 10 Mounts
   ```

2. Check Docker events for volume issues:
   ```bash
   docker events --filter type=volume
   ```

3. Verify volume exists:
   ```bash
   docker volume ls | grep data-volume
   ```

4. Check permissions inside the container:
   ```bash
   docker exec app-container ls -la /data
   ```

5. Solution:
   ```bash
   # Create volume with correct permissions
   docker volume create data-volume
   
   # Run container with proper volume mount
   docker run -d --name app-container -v data-volume:/data app-image
   
   # Fix permissions inside container
   docker exec app-container chown -R app-user:app-user /data
   ```