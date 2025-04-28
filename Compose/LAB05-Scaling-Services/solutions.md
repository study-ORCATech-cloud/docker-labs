# LAB05: Scaling Services with Docker Compose - Solutions

This document provides reference solutions to the Docker Compose scaling configurations in LAB05. These solutions are meant to be reviewed **after** you have attempted to implement the configurations yourself.

## Main Docker Compose File Solution

Here's the complete `docker-compose.yml` file with all configurations implemented:

```yaml
version: '3.8'

services:
  # Scalable web service
  web:
    build: ./web
    ports:
      - "5000"
    depends_on:
      - redis
    environment:
      - FLASK_ENV=development
    deploy:
      replicas: 1
      # Advanced configuration for production environments
      resources:
        limits:
          cpus: '0.5'
          memory: 256M
      restart_policy:
        condition: on-failure
        delay: 5s
        max_attempts: 3
    networks:
      - webnet
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:5000/"]
      interval: 30s
      timeout: 10s
      retries: 3
      start_period: 10s

  # Redis for data persistence
  redis:
    image: redis:6.2-alpine
    networks:
      - webnet
    volumes:
      - redis-data:/data
    command: ["redis-server", "--appendonly", "yes"]
    healthcheck:
      test: ["CMD", "redis-cli", "ping"]
      interval: 30s
      timeout: 10s
      retries: 3

  # Nginx load balancer
  nginx:
    image: nginx:alpine
    ports:
      - "80:80"
    volumes:
      - ./nginx/nginx.conf:/etc/nginx/nginx.conf:ro
    depends_on:
      - web
    networks:
      - webnet
    deploy:
      restart_policy:
        condition: on-failure
    healthcheck:
      test: ["CMD", "wget", "--quiet", "--tries=1", "--spider", "http://localhost/"]
      interval: 30s
      timeout: 10s
      retries: 3

networks:
  webnet:
    driver: bridge

volumes:
  redis-data:
    name: lab05_redis_data
```

## Nginx Load Balancer Configuration

Here's the complete `nginx.conf` file:

```nginx
events {
    worker_connections 1024;
}

http {
    # Define upstream server group for load balancing
    upstream web-app {
        # Advanced configuration: add load balancing method
        least_conn;  # Distributes load based on active connections
        
        # Define web app server with service name and port
        server web:5000;
        
        # Health check settings
        keepalive 16;
    }
    
    server {
        listen 80;
        
        # Access log configuration
        access_log /var/log/nginx/access.log;
        error_log /var/log/nginx/error.log;
        
        # Load balancing location configuration
        location / {
            proxy_pass http://web-app;
            proxy_set_header Host $host;
            proxy_set_header X-Real-IP $remote_addr;
            proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
            proxy_set_header X-Forwarded-Proto $scheme;
            
            # Timeout settings
            proxy_connect_timeout 10s;
            proxy_send_timeout 10s;
            proxy_read_timeout 10s;
        }
        
        # Health check endpoint
        location /health {
            access_log off;
            return 200 "healthy\n";
        }
    }
}
```

## Autoscaling Script

Here's the complete Python autoscaling script:

```python
import time
import subprocess
import docker

client = docker.from_env()

def get_cpu_usage(container):
    stats = container.stats(stream=False)
    cpu_delta = stats['cpu_stats']['cpu_usage']['total_usage'] - stats['precpu_stats']['cpu_usage']['total_usage']
    system_delta = stats['cpu_stats']['system_cpu_usage'] - stats['precpu_stats']['system_cpu_usage']
    if system_delta > 0:
        return (cpu_delta / system_delta) * 100
    return 0

def get_average_cpu(service_name):
    containers = client.containers.list(filters={"label": f"com.docker.compose.service={service_name}"})
    if not containers:
        return 0
    total_cpu = sum(get_cpu_usage(container) for container in containers)
    return total_cpu / len(containers)

def scale_service(service_name, replicas):
    subprocess.run(["docker", "compose", "up", "-d", "--scale", f"{service_name}={replicas}"])
    print(f"Scaled {service_name} to {replicas} replicas")

def autoscale():
    min_replicas = 2
    max_replicas = 10
    scale_up_threshold = 70  # CPU percentage
    scale_down_threshold = 30  # CPU percentage
    service_name = "web"
    
    while True:
        try:
            avg_cpu = get_average_cpu(service_name)
            current_replicas = len(client.containers.list(filters={"label": f"com.docker.compose.service={service_name}"}))
            
            print(f"Service: {service_name}, Replicas: {current_replicas}, Avg CPU: {avg_cpu:.2f}%")
            
            if avg_cpu > scale_up_threshold and current_replicas < max_replicas:
                scale_service(service_name, current_replicas + 1)
            elif avg_cpu < scale_down_threshold and current_replicas > min_replicas:
                scale_service(service_name, current_replicas - 1)
                
            time.sleep(30)  # Check every 30 seconds
        except Exception as e:
            print(f"Error: {e}")
            time.sleep(60)  # Wait longer if there's an error

if __name__ == "__main__":
    autoscale()
```

## Common Scaling Commands

### Manual Scaling

```bash
# Scale up to 5 instances
docker-compose up -d --scale web=5

# Scale down to 2 instances
docker-compose up -d --scale web=2

# Scale multiple services at once
docker-compose up -d --scale web=4 --scale nginx=2
```

### Testing the Load Balancer

```bash
# Test with curl in a loop to see load balancing in action
for i in {1..20}; do curl http://localhost/; echo; done

# Generate load for testing auto-scaling
while true; do curl -s http://localhost/ > /dev/null; done
```

## Key Learning Points

1. **Horizontal Scaling**: Docker Compose allows easy horizontal scaling with the `--scale` option.

2. **Load Balancing**: Nginx can distribute traffic across multiple service instances.

3. **Service Discovery**: Docker's built-in DNS resolves the service name to all container instances.

4. **Resource Limits**: The `deploy` section can set resource constraints for each service.

5. **Health Checks**: Containers can implement health checks to ensure they're responding correctly.

6. **Auto-scaling**: External tools can automate scaling based on metrics like CPU or memory usage.

## Common Questions and Answers

**Q**: Why doesn't the container ID change with every request even with multiple web containers?  
**A**: Nginx's default load balancing behavior may favor some containers. Try adding `least_conn;` to the upstream section for more even distribution.

**Q**: How can I scale services in a production environment?  
**A**: For production, consider using Docker Swarm mode or Kubernetes which provide more robust orchestration features.

**Q**: What happens if I scale a service with volume mounts?  
**A**: Each container will mount the same volume, which can cause conflicts if they all write to the same files.

**Q**: Why do we need Redis in this setup?  
**A**: Redis provides a centralized data store that all web instances can access, allowing them to share state.

**Q**: How do I view logs from all scaled instances?  
**A**: Use `docker-compose logs web` to see logs from all web service instances. Consider implementing a centralized logging solution for production. 