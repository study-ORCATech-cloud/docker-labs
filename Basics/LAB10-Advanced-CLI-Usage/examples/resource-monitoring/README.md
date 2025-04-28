# Docker Resource Monitoring and Inspection

This guide covers advanced techniques for monitoring and inspecting Docker resources using CLI commands.

## Overview

Docker provides powerful CLI commands for monitoring container resources and inspecting detailed information about Docker objects. In this module, you will learn:

- How to use `docker stats` for real-time resource monitoring
- Advanced `docker inspect` usage for detailed information extraction
- Techniques for resource monitoring across multiple containers
- Methods for parsing and analyzing resource data
- Best practices for resource monitoring and management

## Resource Monitoring with `docker stats`

The `docker stats` command provides a live stream of container resource usage statistics.

### Basic Usage

```bash
# Monitor all running containers
docker stats

# Monitor specific containers
docker stats container1 container2

# Display a single snapshot (non-streaming)
docker stats --no-stream
```

### Advanced Formatting

```bash
# Show only specific columns with custom format
docker stats --format "table {{.Name}}\t{{.CPUPerc}}\t{{.MemUsage}}\t{{.NetIO}}"

# Format as JSON
docker stats --format "{{json .}}" --no-stream

# Custom output format focusing on memory
docker stats --format "{{.Name}}: Memory {{.MemPerc}} ({{.MemUsage}})" --no-stream

# Create a compact resource view
docker stats --format "{{.Name}}: CPU {{.CPUPerc}} | MEM {{.MemPerc}}" --no-stream
```

### Available Fields for Stats Formatting

- `.Container` - Container ID
- `.Name` - Container name
- `.ID` - Container ID
- `.CPUPerc` - CPU percentage
- `.MemUsage` - Memory usage
- `.MemPerc` - Memory percentage
- `.NetIO` - Network I/O
- `.BlockIO` - Block I/O
- `.PIDs` - Number of PIDs

## Container Inspection with `docker inspect`

The `docker inspect` command provides detailed information about Docker objects.

### Basic Inspect Commands

```bash
# Inspect a container
docker inspect container_name

# Inspect multiple objects
docker inspect container1 container2

# Inspect an image
docker inspect image_name

# Inspect a volume
docker inspect volume_name

# Inspect a network
docker inspect network_name
```

### Filtering Inspect Output

```bash
# Extract specific information using format
docker inspect --format='{{.State.Status}}' container_name

# Get container IP address
docker inspect --format='{{range .NetworkSettings.Networks}}{{.IPAddress}}{{end}}' container_name

# List all mounted volumes
docker inspect --format='{{range .Mounts}}{{.Source}} -> {{.Destination}}{{println}}{{end}}' container_name

# Check if container is running
docker inspect --format='{{.State.Running}}' container_name

# Get container environment variables
docker inspect --format='{{range .Config.Env}}{{println .}}{{end}}' container_name
```

### Complex Data Extraction

```bash
# Get the PID of a container
docker inspect --format='{{.State.Pid}}' container_name

# Extract health check status
docker inspect --format='{{.State.Health.Status}}' container_name

# Get container restart policy
docker inspect --format='{{.HostConfig.RestartPolicy.Name}}' container_name

# List exposed ports
docker inspect --format='{{range $port, $_ := .NetworkSettings.Ports}}{{$port}}{{println}}{{end}}' container_name

# List all labels
docker inspect --format='{{range $k, $v := .Config.Labels}}{{$k}}={{$v}}{{println}}{{end}}' container_name
```

## Combining Commands for Advanced Monitoring

### Filter and Monitor Specific Containers

```bash
# Monitor only containers with a specific label
docker stats $(docker ps -q --filter "label=environment=production")

# Monitor containers running a specific image
docker stats $(docker ps -q --filter "ancestor=nginx")

# Monitor containers on a specific network
docker stats $(docker ps -q --filter "network=my-network")
```

### Resource Usage Snapshots

```bash
# Get CPU usage of all running containers
docker stats --no-stream --format "{{.Name}}: {{.CPUPerc}}" $(docker ps -q)

# Get memory usage with sorting
docker stats --no-stream --format "{{.MemUsage}} {{.Name}}" | sort -hr

# Get network I/O for specific containers
docker stats --no-stream --format "{{.Name}}: {{.NetIO}}" $(docker ps -q --filter "name=web")
```

## Resource Thresholds and Alerting

When monitoring containers, it's useful to establish thresholds for resource usage:

- **CPU:** Consider investigating if consistently above 80-90%
- **Memory:** Watch for containers using more than expected or nearing their limits
- **Network I/O:** Unusually high traffic could indicate issues
- **Block I/O:** High disk activity might suggest performance problems
- **PID count:** Unexpected increases could indicate memory leaks

## Advanced Inspection Techniques

### Comparing Container Configurations

```bash
# Compare environment variables between containers
diff <(docker inspect --format='{{range .Config.Env}}{{println .}}{{end}}' container1) \
     <(docker inspect --format='{{range .Config.Env}}{{println .}}{{end}}' container2)

# Compare volume mounts
diff <(docker inspect --format='{{range .Mounts}}{{.Source}} -> {{.Destination}}{{println}}{{end}}' container1) \
     <(docker inspect --format='{{range .Mounts}}{{.Source}} -> {{.Destination}}{{println}}{{end}}' container2)
```

### Checking Resource Limits

```bash
# Check memory limits
docker inspect --format='Memory Limit: {{.HostConfig.Memory}} bytes' container_name

# Check CPU limits
docker inspect --format='CPU Limit: {{.HostConfig.NanoCpus}}' container_name

# Check both CPU and memory limits
docker inspect --format='CPU: {{if .HostConfig.NanoCpus}}{{.HostConfig.NanoCpus}}{{else}}unlimited{{end}} - Memory: {{if .HostConfig.Memory}}{{.HostConfig.Memory}} bytes{{else}}unlimited{{end}}' container_name
```

### Monitoring Health Checks

```bash
# Show health check status of all containers with health checks
docker ps -a --filter "health=starting" --filter "health=healthy" --filter "health=unhealthy" --format "{{.Names}}: {{.Status}}"

# Detailed health check information
docker inspect --format='{{.State.Health}}' container_name
```

## Using System Commands

```bash
# View system-wide information
docker system df

# Detailed disk usage analysis
docker system df -v

# View events
docker events --filter "type=container" --filter "event=die" --format '{{.ID}} {{.Status}}'
```

## Best Practices for Resource Monitoring

1. **Establish Baselines:**
   - Monitor normal resource usage patterns before setting thresholds
   - Document expected resource consumption for different workloads

2. **Implement Regular Monitoring:**
   - Create scheduled checks for resource usage
   - Keep historical data to analyze trends

3. **Set Appropriate Resource Limits:**
   - Use `--memory` and `--cpus` flags when running containers
   - Ensure limits match application requirements

4. **Use Labels for Monitoring Groups:**
   - Add labels to containers for filtering during monitoring
   - Group related containers with common labels

5. **Monitor Storage Usage:**
   - Regularly check volume usage and container filesystem growth
   - Set up alerts for low disk space

## TODO Tasks

1. Set up a monitoring scenario with at least 5 containers running different applications:
   - A web server (e.g., nginx)
   - A database (e.g., postgres)
   - A cache service (e.g., redis)
   - A compute-intensive service
   - A service with fluctuating resource usage

2. Create custom formatting templates for different monitoring scenarios:
   - A compact view for overview monitoring
   - A detailed view for troubleshooting
   - A resource-focused view for optimization work

3. Implement a bash loop that monitors containers and records stats snapshots at regular intervals

4. Practice extracting specific configuration details using `docker inspect` for:
   - Network configurations
   - Volume mounts
   - Environment variables
   - Resource limits
   - Health check status

5. Create a command that identifies the top 3 containers by:
   - CPU usage
   - Memory usage
   - Network I/O
   - Block I/O

6. Implement a monitoring approach for containers with health checks:
   - Show containers that are unhealthy
   - Show last health check result
   - Monitor containers that frequently change health status

7. Execute commands that compare resource usage across different container types and document findings

8. Practice commands that monitor container restarts and exits, identifying patterns

9. Create a system monitoring command set that checks:
   - Overall disk usage
   - Available container resources
   - Image storage efficiency
   - Build cache usage

10. Document your preferred monitoring commands and approaches in a reference sheet

## Additional Resources

- [Docker Stats Documentation](https://docs.docker.com/engine/reference/commandline/stats/)
- [Docker Inspect Documentation](https://docs.docker.com/engine/reference/commandline/inspect/)
- [Docker System Commands](https://docs.docker.com/engine/reference/commandline/system/)
- [Container Resource Management](https://docs.docker.com/config/containers/resource_constraints/)
- [Docker Health Checks](https://docs.docker.com/engine/reference/builder/#healthcheck) 