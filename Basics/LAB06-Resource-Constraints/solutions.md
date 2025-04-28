# LAB06: Resource Constraints - Solutions

This document provides solutions to the exercises in LAB06. Only consult these solutions after attempting to solve the problems yourself.

## Task 3: CPU Resource Management

### Building the CPU-intensive application

```bash
cd cpu-intensive-app
docker build -t cpu-demo .
```

### Running without constraints

```bash
docker run --name cpu-demo-unconstrained cpu-demo
```

### Running with CPU constraints

```bash
# Limit to 0.5 CPUs
docker run --name cpu-demo-half --cpus=0.5 cpu-demo

# Limit to 1 CPU
docker run --name cpu-demo-one --cpus=1 cpu-demo

# Limit to 2 CPUs
docker run --name cpu-demo-two --cpus=2 cpu-demo
```

### Comparing performance

You can compare execution times from the container logs:

```bash
docker logs cpu-demo-unconstrained | grep "Total execution time"
docker logs cpu-demo-half | grep "Total execution time"
docker logs cpu-demo-one | grep "Total execution time"
docker logs cpu-demo-two | grep "Total execution time"
```

The results will show that:
- Unconstrained: Uses all available CPU resources
- 0.5 CPU: Takes approximately twice as long as the 1 CPU setting
- 1 CPU: Baseline performance with one full CPU core
- 2 CPUs: Better performance than 1 CPU if the application can utilize multiple cores

## Task 4: Memory Resource Management

### Building the memory-intensive application

```bash
cd ../memory-usage-demo
docker build -t memory-demo .
```

### Running without constraints

```bash
docker run --name memory-demo-unconstrained memory-demo
```

### Running with memory constraints

```bash
# Limit to 256MB
docker run --name memory-demo-256m --memory=256m memory-demo

# Limit to 512MB
docker run --name memory-demo-512m --memory=512m memory-demo

# Limit to 1GB
docker run --name memory-demo-1g --memory=1g memory-demo
```

### Handling memory constraints gracefully

In the Python application, implement memory usage monitoring and graceful degradation:

```python
import os
import psutil
import resource

def get_memory_limit():
    """Get the memory limit from cgroups or system."""
    try:
        with open('/sys/fs/cgroup/memory/memory.limit_in_bytes', 'r') as f:
            return int(f.read().strip())
    except:
        # Default to system memory
        return psutil.virtual_memory().total

def monitor_memory_usage(threshold_percent=80):
    """Monitor memory usage and take action if it exceeds threshold."""
    memory_limit = get_memory_limit()
    current_usage = psutil.Process(os.getpid()).memory_info().rss
    usage_percent = (current_usage / memory_limit) * 100
    
    if usage_percent > threshold_percent:
        # Take action to reduce memory usage
        # e.g., clear caches, reduce batch sizes, etc.
        print(f"Warning: Memory usage at {usage_percent:.2f}% - taking action")
        resource.setrlimit(resource.RLIMIT_DATA, 
                          (int(memory_limit * threshold_percent / 100), 
                           resource.RLIM_INFINITY))
        return True
    return False
```

### Testing with OOM killer settings

```bash
# Run with OOM killer disabled (container will hang instead of being killed)
docker run --name memory-demo-no-oom --memory=256m --oom-kill-disable memory-demo

# Run with memory reservation (soft limit)
docker run --name memory-demo-reservation --memory=512m --memory-reservation=256m memory-demo
```

## Task 5: Combining CPU and Memory Constraints

```bash
# Run CPU-intensive app with both constraints
docker run --name cpu-memory-demo --cpus=1 --memory=512m cpu-demo

# Run memory-intensive app with both constraints
docker run --name memory-cpu-demo --cpus=1 --memory=512m memory-demo
```

## Task 6: Resource Constraints in Production Scenarios

### Web Server (Nginx)

```bash
docker run --name nginx \
  --cpus=0.5 \
  --memory=256m \
  --memory-reservation=128m \
  -p 80:80 \
  nginx:latest
```

### Application Server (Python Flask)

```bash
docker run --name flask-app \
  --cpus=1 \
  --memory=512m \
  --memory-reservation=256m \
  -p 5000:5000 \
  flask-app:latest
```

### Database (PostgreSQL)

```bash
docker run --name postgres \
  --cpus=2 \
  --memory=1g \
  --memory-reservation=512m \
  -p 5432:5432 \
  postgres:latest
```

## Task 7: Resource Constraints in Docker Compose

```yaml
version: '3'

services:
  nginx:
    image: nginx:latest
    ports:
      - "80:80"
    deploy:
      resources:
        limits:
          cpus: '0.5'
          memory: 256M
        reservations:
          cpus: '0.1'
          memory: 128M

  app:
    image: flask-app:latest
    ports:
      - "5000:5000"
    deploy:
      resources:
        limits:
          cpus: '1'
          memory: 512M
        reservations:
          cpus: '0.5'
          memory: 256M

  database:
    image: postgres:latest
    ports:
      - "5432:5432"
    environment:
      POSTGRES_PASSWORD: example
    deploy:
      resources:
        limits:
          cpus: '2'
          memory: 1G
        reservations:
          cpus: '1'
          memory: 512M
    volumes:
      - postgres_data:/var/lib/postgresql/data

volumes:
  postgres_data:
```

## Task 8: Monitoring with Advanced Tools

### Prometheus Configuration (prometheus.yml)

```yaml
global:
  scrape_interval: 15s

scrape_configs:
  - job_name: 'prometheus'
    static_configs:
      - targets: ['localhost:9090']

  - job_name: 'cadvisor'
    static_configs:
      - targets: ['cadvisor:8080']
```

### Docker Compose for Monitoring Stack

```yaml
version: '3'

services:
  prometheus:
    image: prom/prometheus:latest
    ports:
      - "9090:9090"
    volumes:
      - ./prometheus.yml:/etc/prometheus/prometheus.yml
    command:
      - '--config.file=/etc/prometheus/prometheus.yml'

  cadvisor:
    image: gcr.io/cadvisor/cadvisor:latest
    ports:
      - "8080:8080"
    volumes:
      - /:/rootfs:ro
      - /var/run:/var/run:ro
      - /sys:/sys:ro
      - /var/lib/docker/:/var/lib/docker:ro
      - /dev/disk/:/dev/disk:ro

  grafana:
    image: grafana/grafana:latest
    ports:
      - "3000:3000"
    environment:
      - GF_SECURITY_ADMIN_PASSWORD=admin
    volumes:
      - grafana_data:/var/lib/grafana

volumes:
  grafana_data:
```

## Task 9: Troubleshooting Resource-Related Issues

### Container being killed due to memory constraints

Diagnosis:
```bash
docker logs <container_id>
dmesg | grep -i "Out of memory"
```

Solution:
```bash
# Increase memory limit
docker run --memory=1g <image_name>

# Add swap limit
docker run --memory=512m --memory-swap=1g <image_name>

# Optimize application memory usage
# - Reduce batch sizes
# - Implement memory-efficient algorithms
# - Add proper garbage collection triggers
```

### Container suffering from CPU throttling

Diagnosis:
```bash
docker stats <container_id>
```

Solution:
```bash
# Increase CPU allocation
docker run --cpus=2 <image_name>

# Use CPU shares instead of fixed limit for better resource utilization
docker run --cpu-shares=1024 <image_name>
```

### Container experiencing disk I/O bottlenecks

Diagnosis:
```bash
docker exec <container_id> iostat
docker exec <container_id> iotop
```

Solution:
```bash
# Use volume mounts with better performance
docker run -v /fast-storage:/data <image_name>

# Use tmpfs for temporary data
docker run --tmpfs /tmp:rw,noexec,nosuid,size=1g <image_name>

# Optimize application I/O patterns
# - Batch writes
# - Buffer reads
# - Use appropriate filesystem caching
```

## Task 10: Resource Constraints Best Practices

### CPU Allocation Best Practices

- Start with modest CPU limits and increase as needed based on monitoring
- For CPU-bound applications, allocate at least 1 CPU
- For background or non-critical services, use lower CPU shares
- Consider using relative CPU shares for better resource utilization in shared environments
- Monitor CPU throttling events to identify under-provisioned containers

### Memory Management Best Practices

- Always set explicit memory limits to prevent container memory leaks from affecting the host
- Set memory reservation (soft limit) to about 50-75% of the hard limit
- Account for the application's memory usage patterns (peak vs average)
- For Java applications, be aware of JVM memory settings and their interaction with container limits
- For databases, memory limits should account for both cache and operational memory

### Storage Constraints Best Practices

- Use named volumes for persistent data
- Implement proper cleanup procedures for temporary data
- Consider using tmpfs volumes for high-performance temporary storage
- Monitor disk usage within containers
- Implement log rotation to prevent disk space exhaustion

### Network Resource Management

- Use network rate limiting for bandwidth-intensive applications
- Implement proper connection pooling within applications
- Consider using separate networks for different traffic types
- Monitor network traffic patterns to identify bottlenecks

### Microservices Resource Allocation Strategy

- Allocate resources based on service criticality and performance requirements
- Implement proper monitoring and alerting for resource usage
- Use auto-scaling based on resource utilization
- Document resource requirements for each service
- Review and adjust resource allocations regularly based on usage patterns 