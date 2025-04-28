# Docker Container Orchestration from CLI

This guide covers advanced techniques for orchestrating Docker containers using only CLI commands, without relying on higher-level orchestration tools like Docker Swarm or Kubernetes.

## Overview

While dedicated orchestration platforms are recommended for production, understanding CLI-based orchestration is valuable for:
- Development environments
- Testing and debugging
- Small-scale deployments
- Learning the fundamentals of container orchestration
- Automation scripts and CI/CD pipelines
- Environments where higher-level tools are unavailable

## Container Dependency Management

### Managing Container Startup Order

```bash
# Basic sequential start with dependency checking
docker run -d --name db postgres:13
until docker exec db pg_isready; do
  echo "Waiting for database to be ready..."
  sleep 2
done
docker run -d --name api --link db api:latest
```

### Using Docker Networks for Service Discovery

```bash
# Create a user-defined network
docker network create myapp-network

# Run containers on the network
docker run -d --name db --network myapp-network postgres:13
docker run -d --name redis --network myapp-network redis:alpine
docker run -d --name api --network myapp-network myapi:latest
```

### Health Checks for Dependencies

```bash
# Create containers with health checks
docker run -d --name db \
  --health-cmd="pg_isready -U postgres" \
  --health-interval=5s \
  --health-timeout=3s \
  --health-retries=3 \
  postgres:13

# Wait for healthy status before starting dependent containers
until [ "$(docker inspect --format='{{.State.Health.Status}}' db)" = "healthy" ]; do
  echo "Waiting for database to be healthy..."
  sleep 2
done

docker run -d --name api --link db myapi:latest
```

## Coordinated Container Deployments

### Rolling Updates

```bash
# Perform a rolling update of web containers
for i in {1..3}; do
  # Stop and remove one container
  docker stop web-$i
  docker rm web-$i
  
  # Start new container with updated image
  docker run -d --name web-$i --network myapp-network \
    -e "SERVICE_COUNT=3" -e "SERVICE_ID=$i" \
    myapp:2.0
  
  # Wait for container to be healthy
  until [ "$(docker inspect --format='{{.State.Health.Status}}' web-$i)" = "healthy" ]; do
    echo "Waiting for web-$i to be healthy..."
    sleep 2
  done
  
  echo "Updated web-$i successfully"
done
```

### Blue-Green Deployment

```bash
# Deploy new "green" containers
for i in {1..3}; do
  docker run -d --name web-green-$i --network myapp-network myapp:2.0
done

# Wait for all green containers to be healthy
for i in {1..3}; do
  until [ "$(docker inspect --format='{{.State.Health.Status}}' web-green-$i)" = "healthy" ]; do
    echo "Waiting for web-green-$i to be healthy..."
    sleep 2
  done
done

# Update load balancer to point to green containers
docker stop nginx
docker rm nginx
docker run -d --name nginx --network myapp-network -p 80:80 -v ./nginx-green.conf:/etc/nginx/nginx.conf nginx:alpine

# Remove old "blue" containers
for i in {1..3}; do
  docker stop web-blue-$i
  docker rm web-blue-$i
done
```

## Container Restart Policies

### Setting Appropriate Restart Policies

```bash
# Always restart (good for critical services)
docker run -d --restart always --name db postgres:13

# Restart on failure, with limit (good for services that might need recovery)
docker run -d --restart on-failure:5 --name api myapi:latest

# No restart (good for one-time jobs)
docker run --restart no --name data-processor data-processor:latest
```

### Managing Restart Limits

```bash
# Start a container with limited restarts
docker run -d --restart on-failure:3 --name web myapp:latest

# Update a running container's restart policy
docker update --restart always web
```

## Health Monitoring and Recovery

### Setting Up Health Checks

```bash
# Create a container with a health check
docker run -d --name web \
  --health-cmd="curl -f http://localhost:8080/health || exit 1" \
  --health-interval=10s \
  --health-timeout=5s \
  --health-retries=3 \
  --health-start-period=30s \
  myapp:latest
```

### Monitoring Health Status

```bash
# Check health status of a container
docker inspect --format='{{.State.Health.Status}}' web

# List all containers with health status
docker ps --format "table {{.Names}}\t{{.Status}}\t{{.Image}}"

# Filter to show only unhealthy containers
docker ps --filter health=unhealthy
```

### Automated Recovery

```bash
# Monitor and auto-recover unhealthy containers
watch -n 10 'for container in $(docker ps --filter health=unhealthy -q); do
  echo "Restarting unhealthy container: $(docker inspect --format="{{.Name}}" $container)"
  docker restart $container
done'
```

## Resource Allocation and Balancing

### Setting Resource Limits

```bash
# Set CPU and memory limits
docker run -d --name api \
  --cpus 0.5 \
  --memory 512m \
  --memory-reservation 256m \
  myapi:latest
```

### Balancing Workloads

```bash
# Distribute containers across multiple hosts manually
# (When using Docker CLI with multiple contexts)
for i in {1..6}; do
  host=$((i % 3))  # Distribute across 3 hosts
  docker --context "host$host" run -d --name worker-$i myworker:latest
done
```

## Load Balancing with HAProxy or Nginx

```bash
# Generate dynamic HAProxy configuration
cat > haproxy.cfg << EOF
global
    daemon
    maxconn 256

defaults
    mode http
    timeout connect 5000ms
    timeout client 50000ms
    timeout server 50000ms

frontend http-in
    bind *:80
    default_backend servers

backend servers
    balance roundrobin
EOF

# Add backend servers from running containers
for container in $(docker ps -f name=web -q); do
  ip=$(docker inspect -f '{{range .NetworkSettings.Networks}}{{.IPAddress}}{{end}}' $container)
  name=$(docker inspect -f '{{.Name}}' $container | cut -c 2-)
  echo "    server $name $ip:8080 check" >> haproxy.cfg
done

# Launch HAProxy load balancer with the generated config
docker run -d --name loadbalancer \
  -v $(pwd)/haproxy.cfg:/usr/local/etc/haproxy/haproxy.cfg:ro \
  -p 80:80 \
  haproxy:latest
```

## Service Discovery and Configuration

### Environment Variable Configuration

```bash
# Create a configuration container
docker run --name config-container \
  -e "DATABASE_URL=postgres://user:pass@db:5432/mydb" \
  -e "REDIS_URL=redis://redis:6379" \
  -e "API_KEY=abc123" \
  busybox sleep 3600

# Start services with configuration from the config container
docker run -d --name api \
  --volumes-from config-container \
  --env-file <(docker exec config-container env) \
  myapi:latest
```

### Dynamic Service Discovery

```bash
# Generate a service registry file
echo "{" > services.json
first=true
for container in $(docker ps -q); do
  name=$(docker inspect -f '{{.Name}}' $container | cut -c 2-)
  ip=$(docker inspect -f '{{range .NetworkSettings.Networks}}{{.IPAddress}}{{end}}' $container)
  ports=$(docker inspect -f '{{json .Config.ExposedPorts}}' $container)
  
  if [ "$first" = true ]; then
    first=false
  else
    echo "," >> services.json
  fi
  
  echo "  \"$name\": {" >> services.json
  echo "    \"ip\": \"$ip\"," >> services.json
  echo "    \"ports\": $ports" >> services.json
  echo "  }" >> services.json
done
echo "}" >> services.json

# Use the registry file for service discovery
docker run -d --name service-discovery \
  -v $(pwd)/services.json:/data/services.json \
  -p 8500:8500 \
  consul agent -dev -client=0.0.0.0
```

## Logging and Monitoring Integration

### Centralized Logging

```bash
# Create a logging container
docker run -d --name logstash \
  -p 12201:12201/udp \
  -v logstash-config:/etc/logstash \
  logstash:latest

# Run containers with logging configured
docker run -d --name app \
  --log-driver=gelf \
  --log-opt gelf-address=udp://localhost:12201 \
  myapp:latest
```

### Resource Monitoring

```bash
# Run container stats in the background
docker stats --no-stream > stats.log &

# Process stats into metrics
cat stats.log | awk '{print $2, $3, $4}' | sort | uniq -c
```

## Backup and Restore for CLI Orchestration

### Volume Backup

```bash
# Backup a data volume
docker run --rm \
  -v pgdata:/source:ro \
  -v $(pwd)/backup:/backup \
  busybox tar -czf /backup/pgdata-$(date +%Y%m%d).tar.gz -C /source .
```

### Container Configuration Backup

```bash
# Backup container configurations
mkdir -p container-configs
for container in $(docker ps -q); do
  name=$(docker inspect -f '{{.Name}}' $container | cut -c 2-)
  docker inspect $container > container-configs/$name.json
done
tar -czf container-configs-$(date +%Y%m%d).tar.gz container-configs
```

## Complete Orchestration Example

Here's a complete example of a CLI-based orchestration for a three-tier application:

```bash
#!/bin/bash
# File: deploy-app.sh

# Create network
docker network create myapp-network

# Deploy database
docker run -d --name db \
  --network myapp-network \
  -e POSTGRES_PASSWORD=mysecretpassword \
  -e POSTGRES_DB=myapp \
  -v pgdata:/var/lib/postgresql/data \
  --health-cmd="pg_isready -U postgres" \
  --health-interval=5s \
  --health-timeout=3s \
  --health-retries=3 \
  --restart always \
  postgres:13

# Wait for database to be healthy
echo "Waiting for database to be healthy..."
until [ "$(docker inspect --format='{{.State.Health.Status}}' db)" = "healthy" ]; do
  sleep 2
done

# Deploy cache
docker run -d --name redis \
  --network myapp-network \
  --restart always \
  redis:alpine

# Deploy backend API
docker run -d --name api \
  --network myapp-network \
  -e DB_HOST=db \
  -e DB_USER=postgres \
  -e DB_PASSWORD=mysecretpassword \
  -e DB_NAME=myapp \
  -e REDIS_HOST=redis \
  --health-cmd="curl -f http://localhost:3000/health || exit 1" \
  --health-interval=10s \
  --health-timeout=3s \
  --health-retries=3 \
  --restart on-failure:5 \
  myapi:latest

# Wait for API to be healthy
echo "Waiting for API to be healthy..."
until [ "$(docker inspect --format='{{.State.Health.Status}}' api)" = "healthy" ]; do
  sleep 2
done

# Deploy frontend replicas
for i in {1..3}; do
  docker run -d --name frontend-$i \
    --network myapp-network \
    -e API_URL=http://api:3000 \
    --health-cmd="curl -f http://localhost:80/health || exit 1" \
    --health-interval=10s \
    --health-timeout=3s \
    --health-retries=3 \
    --restart on-failure:3 \
    myfrontend:latest
  
  echo "Waiting for frontend-$i to be healthy..."
  until [ "$(docker inspect --format='{{.State.Health.Status}}' frontend-$i)" = "healthy" ]; do
    sleep 2
  done
done

# Deploy load balancer
docker run -d --name nginx \
  --network myapp-network \
  -p 80:80 \
  -v $(pwd)/nginx.conf:/etc/nginx/nginx.conf:ro \
  --restart always \
  nginx:alpine

echo "Application deployed successfully"
```

## TODO Tasks

1. Create a deployment script for a multi-container application:
   - Design a network layout with proper isolation
   - Implement container dependency ordering
   - Add health checks for all components
   - Include a load balancer configuration

2. Implement a rolling update mechanism:
   - Create a script that updates containers one at a time
   - Add validation of new containers before moving to the next
   - Implement rollback in case of failures
   - Test the update process with different failure scenarios

3. Build a container health monitoring system:
   - Create a script that checks the health of all containers
   - Implement automatic recovery for unhealthy containers
   - Set up notifications for persistent health issues
   - Add detailed logging of health status changes

4. Develop a resource management solution:
   - Create a script that balances resources across containers
   - Implement automatic scaling based on load
   - Set appropriate resource limits for each container type
   - Monitor resource usage and generate reports

5. Implement a backup and restore system:
   - Create a script for automated volume backups
   - Add container configuration backups
   - Implement a restore procedure
   - Test the backup and restore process

6. Create a service discovery mechanism:
   - Develop a dynamic service registry
   - Implement automatic service registration
   - Add service health monitoring
   - Create a client-side discovery pattern

7. Build a logging and monitoring infrastructure:
   - Set up centralized logging
   - Create a monitoring dashboard
   - Implement alerting based on metrics
   - Add log rotation and archiving

8. Develop a blue-green deployment strategy:
   - Create scripts for parallel environments
   - Implement traffic switching
   - Add validation before switching
   - Include rollback procedures

9. Create a container lifecycle management system:
   - Implement startup, scaling, and shutdown procedures
   - Add cleanup of old containers and images
   - Create a container inventory
   - Implement container update policies

10. Document your CLI orchestration approach:
    - Create a reference guide with examples
    - Document architecture decisions
    - Include troubleshooting procedures
    - Add performance optimization tips

## Additional Resources

- [Docker Run Reference](https://docs.docker.com/engine/reference/run/)
- [Docker Network Command Reference](https://docs.docker.com/engine/reference/commandline/network/)
- [Docker Health Checks](https://docs.docker.com/engine/reference/builder/#healthcheck)
- [Docker Update Command](https://docs.docker.com/engine/reference/commandline/update/)
- [Docker Restart Policies](https://docs.docker.com/config/containers/start-containers-automatically/) 