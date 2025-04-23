# LAB05: Debugging Docker Containers

This lab teaches techniques for debugging containers and troubleshooting common Docker issues.

## Lab Overview

In this lab, you will:
- Learn methods for inspecting container state and logs
- Debug running and stopped containers
- Enter container environments for troubleshooting
- Understand and resolve common Docker issues
- Use specialized debugging tools with Docker
- Practice debugging in real-world scenarios

## Learning Objectives

- Master Docker's built-in debugging commands
- Understand container logs and logging drivers
- Learn techniques for interactive debugging sessions
- Troubleshoot networking and volume issues
- Identify and fix resource constraints
- Debug application crashes and performance problems

## Prerequisites

- Docker Engine installed
- Completion of LAB01-GettingStarted, LAB02-BuildingImages, LAB03-Volumes, and LAB04-Layers
- Basic understanding of Linux command line

## Lab Projects

This lab includes two examples:
1. **debug-app**: A Flask application with intentional bugs to debug
2. **debug-tools**: Specialized debugging tools and utilities for Docker

## Lab Tasks

### Task 1: Understanding Container States

Containers can be in different states. Learn to interpret them:

```bash
docker ps -a
```

Common states:
- `Created`: Container created but never started
- `Running`: Container is currently running
- `Exited`: Container has stopped with an exit code
- `Paused`: Container execution is paused
- `Restarting`: Container is being restarted

Note the exit code for stopped containers. `0` indicates successful execution, while any other number indicates an error.

### Task 2: Inspecting Container Logs

Docker logs are the primary tool for diagnosing issues:

```bash
# Basic logs
docker logs <container_id>

# Follow logs in real-time
docker logs -f <container_id>

# Show timestamps
docker logs --timestamps <container_id>

# Show last N lines
docker logs --tail=100 <container_id>

# Logs since a timestamp or duration
docker logs --since 2023-01-01T00:00:00 <container_id>
docker logs --since 10m <container_id>
```

### Task 3: Inspecting Container Details

Get detailed information about a container:

```bash
docker inspect <container_id>
```

Parse specific information:

```bash
# Get IP address
docker inspect -f '{{range .NetworkSettings.Networks}}{{.IPAddress}}{{end}}' <container_id>

# Get volume mounts
docker inspect -f '{{range .Mounts}}{{.Source}} -> {{.Destination}}{{end}}' <container_id>

# Get environment variables
docker inspect -f '{{range .Config.Env}}{{.}}{{end}}' <container_id>
```

### Task 4: Interactive Debugging

Enter a running container for interactive debugging:

```bash
# Start an interactive shell in a running container
docker exec -it <container_id> /bin/bash

# If bash is not available, try sh
docker exec -it <container_id> /bin/sh
```

For containers that immediately exit or won't start, modify the container's command:

```bash
# Override the entrypoint to start a shell
docker run -it --entrypoint /bin/bash <image_name>

# Or keep the entrypoint but replace the command
docker run -it <image_name> /bin/bash
```

### Task 5: Debugging with Improved Visibility

Run containers with enhanced debugging options:

```bash
# Run with more verbose output
docker run --verbose <image_name>

# Run container with increased log level
docker run --log-level=debug <image_name>

# Keep STDIN open after container exits
docker run -i <image_name>
```

### Task 6: Debugging Resource Issues

Identify resource usage and constraints:

```bash
# Show container resource usage statistics
docker stats <container_id>

# Monitor events in real-time
docker events

# Check system-wide Docker information
docker info
```

### Task 7: Debugging Network Issues

Troubleshoot container networking problems:

```bash
# List networks
docker network ls

# Inspect a network
docker network inspect <network_name>

# Connect a running container to a network
docker network connect <network_name> <container_id>

# Run network diagnostics inside a container
docker exec <container_id> ping <destination>
docker exec <container_id> curl <url>
docker exec <container_id> nslookup <hostname>
```

### Task 8: Debugging Volume Issues

Troubleshoot container volume problems:

```bash
# List volumes
docker volume ls

# Inspect a volume
docker volume inspect <volume_name>

# Check permissions inside a container
docker exec <container_id> ls -la <mount_point>
```

### Task 9: Lab Exercise - Debug the Flask Application

Navigate to the `debug-app` directory:

```bash
cd debug-app
```

Follow these steps:
1. Build and run the buggy Flask application
2. Identify the issues using Docker debugging techniques
3. Fix the issues in the Dockerfile and application code
4. Verify the fixes by rebuilding and running the container

### Task 10: Using Advanced Debugging Tools

Navigate to the `debug-tools` directory:

```bash
cd ../debug-tools
```

Explore specialized debugging tools:

1. **Dive**: Analyze image layers
   ```bash
   docker run --rm -it -v /var/run/docker.sock:/var/run/docker.sock wagoodman/dive:latest <image_name>
   ```

2. **Docker Debug**: Mount debugging tools in a container
   ```bash
   docker run --rm -it --pid=container:<container_id> nicolaka/netshoot
   ```

3. **Portainer**: Web-based Docker management
   ```bash
   docker run -d -p 9000:9000 -v /var/run/docker.sock:/var/run/docker.sock portainer/portainer-ce
   ```

## Common Issues and Solutions

### Container Exits Immediately
- Check logs: `docker logs <container_id>`
- Override entrypoint to debug: `docker run -it --entrypoint /bin/sh <image_name>`
- Ensure a foreground process is running in the container

### Container Cannot Connect to Network
- Verify container IP: `docker inspect -f '{{range .NetworkSettings.Networks}}{{.IPAddress}}{{end}}' <container_id>`
- Check network configuration: `docker network inspect <network_name>`
- Test network from inside: `docker exec <container_id> ping <destination>`

### Volume Permission Issues
- Check volume mount: `docker inspect -f '{{range .Mounts}}{{.Source}} -> {{.Destination}}{{end}}' <container_id>`
- Verify permissions: `docker exec <container_id> ls -la <directory>`
- Fix permissions in Dockerfile or at runtime

### Application Performance Issues
- Monitor resource usage: `docker stats <container_id>`
- Check for resource constraints in your Docker run command
- Analyze application logs for slow operations

### Image Build Failures
- Review error messages in the build output
- Check for issues with the Dockerfile syntax
- Ensure build context doesn't include unnecessary large files

## Best Practices for Dockerized Applications

1. **Proper Logging**: Configure applications to log to stdout/stderr
2. **Health Checks**: Implement Docker health checks
3. **Graceful Shutdown**: Handle SIGTERM signals properly
4. **Single Concern**: One primary process per container
5. **Non-root User**: Run containers as non-root users
6. **Minimal Images**: Use minimal base images to reduce complexity
7. **Runtime Configuration**: Use environment variables for configuration

## Clean Up

```bash
# Remove containers
docker rm -f $(docker ps -aq)

# Remove images
docker rmi <image_name>
```

## Real-World Applications

These debugging techniques are essential for:
- Production container troubleshooting
- CI/CD pipeline issue resolution
- Microservices architecture maintenance
- Container orchestration management

## Next Steps

Congratulations on completing the Docker Basics lab series! You can now move on to the Docker Compose labs to learn about multi-container applications and orchestration. 