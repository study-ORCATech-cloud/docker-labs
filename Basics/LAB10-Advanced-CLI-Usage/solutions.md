# LAB10: Advanced CLI Usage - Solutions Guide

This document provides guidance for completing the tasks in LAB10. These are not complete solutions, but rather hints and partial examples to help you work through the exercises.

## Task 1: Advanced Filtering and Formatting

### Filtering Examples

```bash
# Filter containers by name pattern
docker ps -a --filter "name=web"

# Filter by status
docker ps -a --filter "status=running"

# Filter by label
docker ps -a --filter "label=environment=production"

# Combine multiple filters
docker ps -a --filter "status=running" --filter "label=service=api"

# Filter images by reference
docker images --filter "reference=nginx:1.*"

# Filter dangling volumes
docker volume ls --filter "dangling=true"
```

### Formatting Examples

```bash
# Basic table formatting
docker ps --format "table {{.Names}}\t{{.Status}}\t{{.Ports}}"

# Custom container information
docker ps --format "{{.Names}} is using {{.Image}} and has status: {{.Status}}"

# JSON output
docker ps --format "{{json .}}"

# Format and filter together
docker ps --filter "name=web" --format "{{.Names}}: {{.Status}}"
```

### Custom Format Templates

Create template files in a directory such as `custom_view_templates/`:

```
# container_compact.tmpl
{{.Names}}\t{{.Image}}\t{{.Status}}

# security_view.tmpl
{{.Names}}\t{{.Image}}\t{{.Mounts}}\t{{.Ports}}
```

Use them with:

```bash
docker ps --format "table $(cat custom_view_templates/container_compact.tmpl)"
```

## Task 2: Context Management

### Creating and Managing Contexts

```bash
# Create a context for local development
docker context create dev --description "Local Development" --docker "host=unix:///var/run/docker.sock"

# Create a context for a remote server
docker context create prod --description "Production Server" --docker "host=ssh://user@remote-server"

# List available contexts
docker context ls

# Use a different context
docker context use prod

# Run a command in a specific context without switching
docker --context dev ps
```

### Context Export/Import

```bash
# Export a context
docker context export prod --output prod-context.tar.gz

# Import a context
docker context import new-prod prod-context.tar.gz
```

## Task 3: Resource Monitoring and Inspection

### Stats Monitoring

```bash
# Basic stats for all containers
docker stats

# Formatting stats output
docker stats --format "table {{.Name}}\t{{.CPUPerc}}\t{{.MemUsage}}\t{{.NetIO}}"

# One-time stats snapshot
docker stats --no-stream
```

### Container Inspection

```bash
# Basic inspection
docker inspect container_name

# Extract specific information
docker inspect --format '{{.State.Status}}' container_name

# Check health status
docker inspect --format '{{.State.Health.Status}}' container_name

# Extract networking information
docker inspect --format '{{range .NetworkSettings.Networks}}{{.IPAddress}}{{end}}' container_name

# List all environment variables
docker inspect --format '{{range .Config.Env}}{{println .}}{{end}}' container_name
```

## Task 4: CLI Plugins and Extensions

### Using Official Plugins

```bash
# Use the buildx plugin
docker buildx ls
docker buildx create --name mybuilder --use

# Use the scout plugin
docker scout quickview nginx:latest
```

### Creating a Basic Plugin

Create a file at `~/.docker/cli-plugins/docker-hello`:

```bash
#!/bin/bash

# Handle --help
if [ "$1" = "--help" ]; then
    echo "Usage: docker hello [OPTIONS] [NAME]"
    echo ""
    echo "Say hello to someone"
    echo ""
    echo "Options:"
    echo "  --name string    Name to greet (default \"World\")"
    exit 0
fi

# Handle --version
if [ "$1" = "--version" ]; then
    echo "Docker Hello Plugin version 1.0.0"
    exit 0
fi

# Handle invocation
NAME="World"
if [ "$1" = "--name" ]; then
    NAME="$2"
fi

echo "Hello, $NAME from Docker plugin!"
```

Make it executable:

```bash
chmod +x ~/.docker/cli-plugins/docker-hello
```

Test your plugin:

```bash
docker hello
docker hello --name Student
```

## Task 5: Event Monitoring and Automation

### Basic Event Monitoring

```bash
# View all events
docker events

# Filter by type
docker events --filter 'type=container'

# Format event output
docker events --format '{{.Time}}: {{.Type}} {{.Action}} {{.Actor.Attributes.name}}'
```

### Event-Driven Scripts

Create an event reaction script:

```bash
# Monitor container stops and restart if needed
docker events --filter 'type=container' --filter 'event=die' --format '{{.Actor.Attributes.name}} {{.Actor.Attributes.exitCode}}' | while read container exit_code; do
    # Extract container name and exit code
    name=$(echo $container | cut -d' ' -f1)
    code=$(echo $container | cut -d' ' -f2)
    
    echo "Container $name exited with code $code"
    
    # Restart on error (non-zero exit)
    if [ "$code" -ne 0 ]; then
        echo "Restarting container $name..."
        docker start $name
    fi
done
```

## Task 6: Advanced Image Management

### Image Cleanup

```bash
# Remove dangling images
docker image prune

# Remove all unused images
docker image prune -a

# Remove images with specific filter
docker image prune -a --filter "until=24h"
```

### Layer Analysis

```bash
# View image layers
docker history nginx:latest

# Check image size and layers
docker inspect --format='Size: {{.Size}} bytes, Layers: {{len .RootFS.Layers}}' nginx:latest
```

### Multi-Architecture Support

```bash
# Create a buildx instance
docker buildx create --name mybuilder --use

# Build for multiple platforms
docker buildx build --platform linux/amd64,linux/arm64 -t myapp:latest .
```

## Task 7: Container Orchestration from CLI

### Managing Container Dependencies

```bash
# Start containers with dependency checking
docker run -d --name db postgres:13
until docker exec db pg_isready; do
  echo "Waiting for database..."
  sleep 2
done
docker run -d --name api --link db myapi:latest
```

### Health Checks and Recovery

```bash
# Create containers with health checks
docker run -d --name web \
  --health-cmd="curl -f http://localhost/ || exit 1" \
  --health-interval=10s \
  --health-timeout=5s \
  --health-retries=3 \
  nginx

# Monitor health status
watch -n 10 'docker ps --format "table {{.Names}}\t{{.Status}}" | grep -v "health: starting"'
```

## Task 8: Security Scanning and Checks

### Using Docker Scout

```bash
# Basic vulnerability scan
docker scout cves nginx:latest

# Get a security overview
docker scout quickview nginx:latest
```

### Using Docker Bench Security

```bash
# Clone the Docker Bench Security repository
git clone https://github.com/docker/docker-bench-security.git
cd docker-bench-security

# Run the security checks
./docker-bench-security.sh
```

## Task 9: CLI-Based Backup and Restore

### Volume Backup

```bash
# Back up a named volume
docker run --rm -v my-volume:/source:ro -v $(pwd):/backup alpine tar -czf /backup/my-volume-backup.tar.gz -C /source .

# Restore a volume from backup
docker run --rm -v my-volume:/target -v $(pwd):/backup alpine sh -c "cd /target && tar -xzf /backup/my-volume-backup.tar.gz"
```

### Container Configuration Backup

```bash
# Back up container configuration
docker inspect my-container > my-container-config.json
```

## Task 10: Creating a Complete CLI Workflow

For this task, you'll need to combine techniques from previous tasks to create a comprehensive workflow. Here's a skeleton to get started:

```bash
#!/bin/bash
# workflow.sh - Master workflow script

ACTION=$1
shift

case "$ACTION" in
    deploy)
        # Deploy containers with proper ordering and health checks
        ;;
    monitor)
        # Implement monitoring
        ;;
    backup)
        # Back up volumes and configuration
        ;;
    update)
        # Perform rolling updates
        ;;
    cleanup)
        # Clean up resources
        ;;
    status)
        # Show status of all components
        ;;
    *)
        echo "Unknown action: $ACTION"
        echo "Usage: $0 {deploy|monitor|backup|update|cleanup|status}"
        exit 1
        ;;
esac
```

## General Best Practices

1. **Use filtering to focus your commands** - The more specific your filters, the faster and more efficient your commands will be.

2. **Create reusable templates and scripts** - Don't repeat complex command patterns; save them in template files or shell scripts.

3. **Implement proper error handling** - Always check command return codes and implement fallback options.

4. **Use environment variables for configuration** - Store common settings in environment variables to make scripts more flexible.

5. **Set up proper logging** - Ensure all automated scripts have good logging for troubleshooting.

6. **Test in a safe environment** - Always test your complex scripts in a non-production environment first.

7. **Document everything** - Create good documentation for your custom scripts and workflows.

## Challenge Solutions

### Challenge 1: Custom Monitoring Dashboard

<details>
<summary>Hint</summary>

Combine `docker stats` with formatting and use a loop to update the output regularly:

```bash
watch -n 5 'docker stats --no-stream --format "table {{.Name}}\t{{.CPUPerc}}\t{{.MemPerc}}\t{{.NetIO}}" | sort -k 3 -hr'
```
</details>

### Challenge 2: Auto-healing System

<details>
<summary>Hint</summary>

Monitor container health status and restart unhealthy containers:

```bash
while true; do
  for container in $(docker ps --filter health=unhealthy -q); do
    name=$(docker inspect --format='{{.Name}}' $container | sed 's/^\///')
    echo "$(date): Container $name is unhealthy, restarting..."
    docker restart $container
  done
  sleep 30
done
```
</details>

### Challenge 3: Custom CLI Plugin for Container Management

<details>
<summary>Hint</summary>

Create a plugin that helps manage container groups:

```bash
#!/bin/bash
# ~/.docker/cli-plugins/docker-group

# See the example in Task 4 for the basic structure
# Implement commands like:
# - docker group create <group-name> <container1> <container2>...
# - docker group start <group-name>
# - docker group stop <group-name>
# - docker group restart <group-name>
# - docker group ls
```
</details>

## Conclusion

Remember that this solutions guide is meant to help you get started and provide hints, not to give you complete solutions. The real learning comes from experimenting with these commands and creating your own solutions.

If you're still having trouble with any specific part, review the official Docker documentation or ask for help! 