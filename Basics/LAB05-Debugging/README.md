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

## Important Instructions

This lab is designed for hands-on learning. You are expected to:
- Implement solutions yourself for each debugging issue
- Practice using various debugging tools and commands
- Work through the problems systematically
- Document your debugging process and findings

Do not look for ready-made solutions online - the goal is to develop your debugging skills by working through the issues yourself.

## Lab Projects

This lab includes two examples:
1. **debug-app**: A Flask application with intentional bugs for you to find and fix
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

TODO:
1. Read the README.md file in the debug-app directory for specific instructions
2. Build and run the buggy Flask application
3. Use Docker debugging techniques to identify all 10 issues in the app
4. Implement your own solutions for each issue in the Dockerfile and app.py
5. Test your fixes to ensure they resolve the problems
6. Document which debugging techniques helped you find each issue

### Task 10: Using Advanced Debugging Tools

Navigate to the `debug-tools` directory:

```bash
cd ../debug-tools
```

TODO:
1. Review the README.md in the debug-tools directory
2. Try each of the debugging tools provided
3. Use the appropriate tools to debug the following scenarios:
   - A container with resource constraints
   - A container with networking issues
   - A container that exits unexpectedly
4. Document which tools were most effective for each scenario

## Common Issues and Solutions

Here are some typical issues you might encounter and approaches to debug them:

### Container Exits Immediately
TODO: Implement debugging steps for this issue using the techniques learned

### Container Cannot Connect to Network
TODO: Implement debugging steps for this issue using the techniques learned

### Volume Permission Issues
TODO: Implement debugging steps for this issue using the techniques learned

### Application Performance Issues
TODO: Implement debugging steps for this issue using the techniques learned

### Image Build Failures
TODO: Implement debugging steps for this issue using the techniques learned

## Testing Your Understanding

After completing the lab exercises, you should be able to:

1. Explain the different container states and what they indicate
2. Use Docker logs to troubleshoot application issues
3. Inspect container configuration to identify misconfigurations
4. Use interactive debugging to explore container environments
5. Apply appropriate debugging techniques for different types of issues
6. Implement fixes for common Docker problems

## Clean Up

Don't forget to clean up resources after completing the lab:

```bash
docker stop $(docker ps -a -q)
docker rm $(docker ps -a -q)
docker rmi debug-app:buggy debug-app:fixed
```

## Next Steps

After mastering debugging techniques in this lab, you'll be ready to move on to more advanced Docker topics in the next labs. 