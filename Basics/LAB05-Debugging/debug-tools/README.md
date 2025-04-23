# Docker Debugging Tools

This directory contains information about specialized tools that can help with debugging Docker containers.

## Available Tools

### 1. Dive - Image Layer Analysis

[Dive](https://github.com/wagoodman/dive) is a tool for exploring Docker images, layer contents, and discovering ways to shrink the size of your Docker/OCI image.

Run Dive against any image:

```bash
docker run --rm -it \
  -v /var/run/docker.sock:/var/run/docker.sock \
  wagoodman/dive:latest <image_name>
```

Example:
```bash
docker run --rm -it \
  -v /var/run/docker.sock:/var/run/docker.sock \
  wagoodman/dive:latest nginx:latest
```

### 2. Netshoot - Network Debugging Toolkit

[Netshoot](https://github.com/nicolaka/netshoot) is a container with a set of networking tools useful for troubleshooting issues with Docker containers.

Execute network diagnostics inside a running container:

```bash
docker run --rm -it \
  --network container:<container_name> \
  nicolaka/netshoot
```

Analyze a container's network namespace:

```bash
docker run --rm -it \
  --pid container:<container_name> \
  nicolaka/netshoot
```

### 3. Portainer - Container Management UI

[Portainer](https://www.portainer.io/) provides a graphical interface for Docker management.

Run Portainer:

```bash
docker run -d -p 9000:9000 \
  -v /var/run/docker.sock:/var/run/docker.sock \
  portainer/portainer-ce
```

Access the UI at http://localhost:9000

### 4. cAdvisor - Container Resource Monitoring

[cAdvisor](https://github.com/google/cadvisor) provides container users with resource usage and performance metrics.

Run cAdvisor:

```bash
docker run \
  --volume=/:/rootfs:ro \
  --volume=/var/run:/var/run:ro \
  --volume=/sys:/sys:ro \
  --volume=/var/lib/docker/:/var/lib/docker:ro \
  --publish=8080:8080 \
  --detach=true \
  --name=cadvisor \
  gcr.io/cadvisor/cadvisor:latest
```

Access the UI at http://localhost:8080

### 5. Docker Logs with JSON Formatter

Parse Docker logs in JSON format:

```bash
# For pretty-printing JSON logs
docker logs <container_id> | jq
```

Install jq (JSON parser):
- Linux: `apt-get install jq` or `yum install jq`
- macOS: `brew install jq`
- Windows: `scoop install jq`

### 6. Docker Debug Container

Create a debugging container to inspect files inside volumes:

```bash
docker run -it --rm \
  --volumes-from <target_container> \
  alpine sh
```

### 7. Docker Events Watcher

Monitor Docker events in real-time:

```bash
docker events --filter 'container=<container_name>'
```

Monitor all events:

```bash
docker events
```

### 8. nsenter - Access Container Namespaces

On Linux, access the namespaces of a running container:

```bash
# Get container PID
PID=$(docker inspect --format '{{.State.Pid}}' <container_id>)

# Enter all namespaces
sudo nsenter -t $PID -a

# Enter only network namespace
sudo nsenter -t $PID -n
```

## Advanced Debugging Scripts

### Resource Usage Monitor

```bash
#!/bin/bash
# monitor.sh - Container resource monitoring
while true; do 
  echo "===== $(date) ====="
  docker stats --no-stream --format "table {{.Name}}\t{{.CPUPerc}}\t{{.MemUsage}}"
  sleep 5
done
```

### Container Healthcheck

```bash
#!/bin/bash
# healthcheck.sh - Check container health
CONTAINER=$1

if [ -z "$CONTAINER" ]; then
  echo "Usage: $0 <container_name>"
  exit 1
fi

echo "Container: $CONTAINER"
echo "Status: $(docker inspect -f '{{.State.Status}}' $CONTAINER)"
echo "Running: $(docker inspect -f '{{.State.Running}}' $CONTAINER)"
echo "Exitcode: $(docker inspect -f '{{.State.ExitCode}}' $CONTAINER)"
echo "Health: $(docker inspect -f '{{.State.Health.Status}}' $CONTAINER 2>/dev/null || echo "No health check")"
echo "Logs (last 5 lines):"
docker logs --tail 5 $CONTAINER
```

## Best Practices

1. **Always enable Docker logging**:
   ```bash
   # Set log driver to json-file with size limits
   docker run --log-driver=json-file --log-opt max-size=10m --log-opt max-file=3 <image>
   ```

2. **Include debugging tools in development images**:
   ```dockerfile
   # In your Dockerfile for development
   RUN apt-get update && apt-get install -y \
       curl \
       procps \
       net-tools \
       iproute2 \
       dnsutils \
       && rm -rf /var/lib/apt/lists/*
   ```

3. **Use container labels for organized debugging**:
   ```bash
   docker run --label "environment=dev" --label "debug=true" <image>
   
   # Later filter by these labels
   docker ps --filter "label=debug=true"
   ```

## Resources

- [Docker Documentation - Logs](https://docs.docker.com/config/containers/logging/)
- [Docker Documentation - Debug](https://docs.docker.com/engine/reference/commandline/container_inspect/)
- [Docker Troubleshooting Guide](https://success.docker.com/article/troubleshooting-container-networking) 