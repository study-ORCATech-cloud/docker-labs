# Docker Events Monitoring and Automation

This guide covers how to monitor Docker events and automate actions based on these events.

## Overview

Docker's event stream provides real-time notifications about what's happening in your Docker environment, including:
- Container lifecycle events (create, start, stop, die, etc.)
- Image events (pull, push, remove, etc.)
- Volume events (create, mount, remove, etc.)
- Network events (create, connect, disconnect, remove, etc.)
- Plugin events (install, enable, disable, etc.)

By monitoring these events, you can create automated responses to specific conditions.

## Basic Event Monitoring

### Viewing the Event Stream

The `docker events` command shows a live stream of Docker events:

```bash
# View all events in real-time
docker events

# View events for the last 1 hour
docker events --since 1h

# View events until a specific time
docker events --until '2023-12-31T23:59:59'

# Format events as JSON
docker events --format '{{json .}}'
```

### Filtering Events

You can filter the event stream to focus on specific event types:

```bash
# Filter by event type
docker events --filter 'type=container'
docker events --filter 'type=image'
docker events --filter 'type=volume'
docker events --filter 'type=network'

# Filter by event action
docker events --filter 'event=start'
docker events --filter 'event=stop'
docker events --filter 'event=die'

# Filter by container name
docker events --filter 'container=my-nginx'

# Filter by image
docker events --filter 'image=nginx:alpine'

# Combine multiple filters (AND logic)
docker events --filter 'type=container' --filter 'event=start' --filter 'image=nginx'
```

### Formatting Event Output

Customize the output format of Docker events:

```bash
# Basic formatting with specific fields
docker events --format '{{.ID}}: {{.Status}}'

# Table format
docker events --format 'table {{.Type}}\t{{.Action}}\t{{.Actor.ID}}'

# Detailed formatting with nested fields
docker events --format '{{.Time}}: {{.Type}} {{.Action}} {{.Actor.Attributes.name}}'

# JSON formatting (useful for parsing)
docker events --format '{{json .}}'
```

## Creating Event-Driven Automation

Using event monitoring, you can create scripts that respond automatically to Docker events.

### Simple Event Reaction Pattern

```bash
# Basic pattern for event-driven actions
docker events --filter 'type=container' --filter 'event=die' --format '{{.Actor.Attributes.name}}' | while read container; do
    echo "Container $container has stopped. Taking action..."
    # Your action here, for example:
    # - Send notification
    # - Restart container
    # - Log the event
    # - Trigger cleanup
done
```

### Practical Examples

#### Restart Containers Automatically

```bash
# Restart containers that exit with non-zero status
docker events --filter 'type=container' --filter 'event=die' --format '{{.ID}} {{.Actor.Attributes.exitCode}}' | while read id exit_code; do
    if [ "$exit_code" -ne 0 ]; then
        echo "Container $id exited with code $exit_code. Restarting..."
        docker restart $id
    fi
done
```

#### Monitor Container Health Status Changes

```bash
# React to health status changes
docker events --filter 'type=container' --filter 'event=health_status' --format '{{.Actor.Attributes.name}} {{.Actor.Attributes.healthStatus}}' | while read container status; do
    if [ "$status" = "unhealthy" ]; then
        echo "Container $container became unhealthy. Sending alert..."
        # Send alert via email, Slack, etc.
    fi
done
```

#### Log Container Starts and Stops

```bash
# Log container lifecycle events
docker events --filter 'type=container' --filter 'event=start' --filter 'event=stop' --format '{{.Time}} {{.Action}} {{.Actor.Attributes.name}}' >> /var/log/container-lifecycle.log
```

#### Cleanup After Image Operations

```bash
# Clean up dangling images after a build
docker events --filter 'type=image' --filter 'event=untag' | while read event; do
    echo "Image untagged. Cleaning up dangling images..."
    docker image prune -f
done
```

## Advanced Event Automation

### Event Data Fields

Docker events provide rich data you can use in your automation scripts:

- `Type`: The object type (container, image, volume, network, etc.)
- `Action`: The event action (create, start, stop, die, etc.)
- `Actor.ID`: The ID of the object
- `Actor.Attributes`: Additional object attributes
  - `name`: Name of the container/volume/network
  - `image`: Image used by the container
  - `exitCode`: Exit code when a container dies
  - `signal`: Signal that killed the container
  - Various labels

### Combining with Other Docker Commands

For comprehensive automation, combine `docker events` with other Docker commands:

```bash
# Scale up when containers are running at high CPU
docker events --filter 'type=container' --filter 'event=start' | while read event; do
    # Check current CPU usage
    high_cpu_containers=$(docker stats --no-stream --format "{{.Name}}: {{.CPUPerc}}" | grep -E "[0-9]{2,3}\.[0-9]{2}%" | wc -l)
    if [ $high_cpu_containers -gt 5 ]; then
        echo "High CPU load detected, scaling up service..."
        docker service scale myservice=10
    fi
done
```

### Event-Driven Monitoring Dashboard

```bash
# Create a real-time dashboard of container events
docker events --format 'table {{.Time}}\t{{.Type}}\t{{.Action}}\t{{.Actor.Attributes.name}}' --filter 'type=container'
```

## Implementation Patterns

### Background Processing

For long-running event monitoring, use background processing:

```bash
# Run event monitor in the background
nohup bash -c 'docker events --filter "type=container" | while read event; do echo "Event: $event" >> /var/log/docker-events.log; done' &
```

### Distributed Event Handling

For larger environments, implement distributed event handling:

```bash
# Collect events from multiple hosts
for host in host1 host2 host3; do
    ssh $host "docker events --format '{{json .}}'" | jq --arg host "$host" '. + {host: $host}'
done | tee events.jsonl
```

### Event Storage and Analysis

Store events for later analysis:

```bash
# Store events in a time-series database
docker events --format '{{json .}}' | while read event; do
    curl -XPOST "http://influxdb:8086/write?db=docker" --data-binary "events,type=$(echo $event | jq -r .Type) value=1"
done
```

## Best Practices

1. **Filter Efficiently**
   - Use specific filters to reduce processing load
   - Combine multiple filters for precise targeting

2. **Handle Interruptions**
   - Implement reconnection logic for network issues
   - Use supervisor processes to ensure monitoring stays active

3. **Process Events Asynchronously**
   - For complex actions, queue events for processing
   - Avoid blocking the event stream processing

4. **Log Event Handling**
   - Keep records of events and actions taken
   - Include timestamps for troubleshooting

5. **Define Clear Responsibilities**
   - Each event handler should have a single purpose
   - Avoid complex conditional logic in event handling

## Security Considerations

1. **Access Control**
   - Ensure scripts have appropriate Docker API permissions
   - Use principle of least privilege for automation scripts

2. **Validation**
   - Validate event data before taking action
   - Implement safeguards against unexpected events

3. **Rate Limiting**
   - Protect against event storms with rate limiting
   - Implement cooldown periods for repeated actions

4. **Audit Trail**
   - Log all automated actions for audit purposes
   - Include event trigger details with actions

## TODO Tasks

1. Set up basic event monitoring:
   - Create a script that monitors and logs container start/stop events
   - Implement different output formats and analyze which is most useful
   - Test filtering capabilities with various combinations

2. Implement notification systems:
   - Create an event handler that sends email alerts for container failures
   - Implement a messaging integration (Slack, Teams, etc.) for critical events
   - Set up differentiated notifications based on event severity

3. Develop automated recovery:
   - Create a script that automatically restarts containers that exit with errors
   - Implement a health status monitor that takes action when containers become unhealthy
   - Create an automated backup when certain events occur

4. Build an event-driven scaling system:
   - Monitor resource usage events and automatically scale services
   - Implement cooldown periods to prevent oscillation
   - Test the system under various load conditions

5. Create a comprehensive event dashboard:
   - Design a real-time event visualization system
   - Include filtering and searching capabilities
   - Implement event aggregation and statistics

6. Implement a distributed event collection system:
   - Collect events from multiple Docker hosts
   - Centralize event processing and response
   - Handle network interruptions gracefully

7. Develop specialized event handlers:
   - Create handlers for image events (pull, push)
   - Implement network event monitoring
   - Set up volume event tracking

8. Build a forensic analysis tool:
   - Create a script that captures detailed information when containers crash
   - Implement log correlation with events
   - Build a timeline visualization of related events

9. Create a preventive maintenance system:
   - Monitor warning signs in the event stream
   - Take proactive action before failures occur
   - Log trends and patterns in events

10. Document your event automation strategy:
    - Create a reference of events and their automated responses
    - Implement a testing protocol for event handlers
    - Develop an event handling policy for your environment

## Additional Resources

- [Docker Events Command Reference](https://docs.docker.com/engine/reference/commandline/events/)
- [Docker API Events Endpoint](https://docs.docker.com/engine/api/v1.41/#operation/SystemEvents)
- [Event Types Reference](https://docs.docker.com/engine/reference/commandline/events/#object-types)
- [Docker Engine API Events](https://docs.docker.com/engine/api/v1.41/#tag/System) 