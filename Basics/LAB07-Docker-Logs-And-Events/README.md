# LAB07: Docker Logs and Events

This lab teaches how to monitor, manage, and analyze Docker logs and events.

## Lab Overview

In this lab, you will:
- Learn how to view and manage container logs
- Configure Docker logging drivers
- Understand Docker events and their importance
- Implement log rotation and management strategies
- Capture and analyze Docker events
- Set up centralized logging for containers
- Practice real-world logging and event monitoring

## Learning Objectives

- Master Docker's logging commands and options
- Configure different logging drivers for containers
- Parse and filter logs for relevant information
- Use Docker events to monitor container lifecycle
- Set up log rotation and cleanup policies
- Implement centralized logging solutions
- Apply logging best practices in production environments

## Prerequisites

- Docker Engine installed
- Completion of LAB01-LAB06
- Basic understanding of Linux command line
- Familiarity with container concepts

## Important Instructions

This lab is designed for hands-on learning. You are expected to:
- Implement solutions yourself for each task
- Practice using various logging commands and tools
- Work through the exercises systematically
- Document your findings regarding logging and events

Do not look for ready-made solutions online - the goal is to develop your logging and monitoring skills by working through the issues yourself.

## Lab Projects

This lab includes two examples:
1. **logging-demo**: Applications demonstrating different logging approaches
2. **event-monitoring**: Tools and scripts for Docker event monitoring

## Lab Tasks

### Task 1: Understanding Docker Logs

Docker captures stdout and stderr from containers and makes them accessible through the `docker logs` command:

```bash
# Basic logs
docker logs <container_id>

# Follow logs in real-time
docker logs -f <container_id>

# Show timestamps
docker logs --timestamps <container_id>

# Show last N lines
docker logs --tail=100 <container_id>

# Show logs since a specific time
docker logs --since 2023-01-01T00:00:00 <container_id>
docker logs --since 10m <container_id>

# Show logs until a specific time
docker logs --until 2023-01-01T00:00:00 <container_id>
docker logs --until 5m <container_id>
```

### Task 2: Working with Logging Drivers

Docker supports various logging drivers:

```bash
# Check the default logging driver
docker info | grep "Logging Driver"

# Run a container with a specific logging driver
docker run --log-driver=json-file --log-opt max-size=10m --log-opt max-file=3 nginx

# Common logging drivers
# - json-file (default)
# - syslog
# - journald
# - gelf (Graylog)
# - fluentd
# - awslogs
# - splunk
# - none (disables logging)
```

### Task 3: Log Exploration and Analysis

Navigate to the `logging-demo` directory:

```bash
cd logging-demo
```

TODO:
1. Build and run the provided logging demo application
2. Explore the logs using different filtering options:
   - Filter logs by timestamp
   - Filter logs by error level
   - Search for specific text patterns
3. Use command-line tools to analyze logs:
   - Count error occurrences
   - Extract and analyze timing information
   - Create a summary of errors
4. Modify the application to improve its logging:
   - Add structured logging
   - Include contextual information
   - Implement appropriate log levels

### Task 4: Docker Events

Docker events provide a real-time stream of activity happening in the Docker daemon:

```bash
# Stream all events
docker events

# Filter events by type
docker events --filter type=container
docker events --filter type=image
docker events --filter type=volume
docker events --filter type=network

# Filter events by action
docker events --filter event=start
docker events --filter event=stop
docker events --filter event=die

# Combine multiple filters
docker events --filter type=container --filter event=start

# Format events output
docker events --format '{{json .}}'
docker events --format 'ID: {{.ID}} Status: {{.Status}}'
```

### Task 5: Working with Events in Real-Time

Navigate to the `event-monitoring` directory:

```bash
cd ../event-monitoring
```

TODO:
1. Implement a script that monitors Docker events and takes actions based on specific events
2. Configure the script to:
   - Log container starts and stops
   - Send alerts for container failures
   - Track image usage
   - Monitor volume attachments
3. Test your script by generating various Docker events
4. Extend your script to capture event statistics and generate reports

### Task 6: Log Rotation and Management

TODO:
1. Configure log rotation for container logs using Docker's built-in options
2. Implement a log cleanup policy for old container logs
3. Set up a cron job to periodically archive and compress old logs
4. Test your log rotation policy and verify it works as expected
5. Document your log retention and rotation strategy

### Task 7: Centralized Logging for Containers

TODO:
1. Research and choose a centralized logging solution (e.g., ELK stack, Graylog, Fluentd)
2. Configure Docker to use your chosen logging driver
3. Set up a basic centralized logging infrastructure
4. Configure containers to send logs to your central log server
5. Test that logs are being properly collected and indexed
6. Create dashboards to visualize your logs

### Task 8: Logging Best Practices

TODO:
1. Research and document best practices for:
   - Container logging in production
   - Log format standardization
   - Sensitive data handling in logs
   - Log storage and retention policies
2. Implement these best practices in a sample application
3. Create a logging guideline document for your organization

### Task 9: Building a Comprehensive Monitoring Solution

TODO:
1. Combine logging and event monitoring to create a comprehensive monitoring solution
2. Set up alerting based on logs and events
3. Create a dashboard for real-time monitoring
4. Implement automated responses to specific events or log patterns
5. Test your solution with various scenarios

### Task 10: Troubleshooting with Logs and Events

TODO:
1. Use the provided troubleshooting scenarios to practice debugging with logs and events
2. For each scenario:
   - Identify the issue using logs and events
   - Document the troubleshooting process
   - Implement a fix
   - Verify the solution
3. Create your own troubleshooting scenario and solution

## Testing Your Understanding

After completing the lab exercises, you should be able to:
- Use Docker logs and events to monitor containers effectively
- Configure appropriate logging drivers for different scenarios
- Implement log rotation and management strategies
- Set up centralized logging for containerized applications
- Troubleshoot issues using logs and events
- Apply logging best practices in production environments

## Lab Cleanup

Clean up all containers, images, and volumes created during this lab:

```bash
# Stop all running containers
docker stop $(docker ps -q)

# Remove all containers
docker rm $(docker ps -a -q)

# Remove images created for this lab (if needed)
docker rmi $(docker images -q <your-image-name>)

# Remove any volumes created for this lab (if needed)
docker volume prune -f
```

## Additional Resources

- [Docker Logging Documentation](https://docs.docker.com/config/containers/logging/)
- [Docker Events Documentation](https://docs.docker.com/engine/reference/commandline/events/)
- [Fluentd Logging Driver](https://docs.docker.com/config/containers/logging/fluentd/)
- [ELK Stack for Container Logging](https://www.elastic.co/guide/en/logs/guide/current/docker-logging.html)
- [Logging Best Practices for Docker and Containers](https://www.datadoghq.com/blog/docker-logging/) 