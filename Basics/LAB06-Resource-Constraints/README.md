# LAB06: Resource Constraints in Docker

This lab teaches how to manage and monitor resource usage in Docker containers.

## Lab Overview

In this lab, you will:
- Learn how to limit CPU, memory, and storage resources for containers
- Monitor resource usage of running containers
- Understand the impact of resource constraints on container performance
- Implement appropriate resource limits for different application types
- Troubleshoot resource-related issues in Docker
- Practice resource management in real-world scenarios

## Learning Objectives

- Master Docker's resource constraint flags and options
- Understand how to allocate appropriate resources to containers
- Learn techniques for monitoring container resource usage
- Troubleshoot performance issues related to resource constraints
- Implement best practices for resource management in production environments
- Balance resource allocation in multi-container environments

## Prerequisites

- Docker Engine installed
- Completion of LAB01-LAB05
- Basic understanding of Linux command line
- Familiarity with container concepts

## Important Instructions

This lab is designed for hands-on learning. You are expected to:
- Implement solutions yourself for each task
- Practice using various resource constraint flags and monitoring tools
- Work through the exercises systematically
- Document your findings regarding resource allocation and performance

Do not look for ready-made solutions online - the goal is to develop your resource management skills by working through the issues yourself.

## Lab Projects

This lab includes two examples:
1. **cpu-intensive-app**: An application that demonstrates CPU usage patterns
2. **memory-usage-demo**: An application that demonstrates memory allocation and usage

## Lab Tasks

### Task 1: Understanding Docker Resource Constraints

Docker provides several flags to limit container resources:

```bash
# CPU constraints
--cpus=<value>           # Number of CPUs
--cpu-shares=<value>     # CPU shares (relative weight)
--cpu-period=<value>     # Limit CPU CFS period
--cpu-quota=<value>      # Limit CPU CFS quota

# Memory constraints
--memory=<value>         # Memory limit (e.g., 512m, 1g)
--memory-reservation=<value>  # Memory soft limit
--memory-swap=<value>    # Total memory limit (memory + swap)
--oom-kill-disable       # Disable OOM Killer

# Storage constraints
--storage-opt size=<value>  # Set container storage size limit
```

### Task 2: Monitoring Container Resource Usage

Learn to use Docker's built-in monitoring tools:

```bash
# Show resource usage statistics of all running containers
docker stats

# Show statistics for specific containers
docker stats <container_id1> <container_id2>

# Format output to show specific metrics
docker stats --format "table {{.Name}}\t{{.CPUPerc}}\t{{.MemUsage}}"
```

### Task 3: CPU Resource Management

Navigate to the `cpu-intensive-app` directory:

```bash
cd cpu-intensive-app
```

TODO:
1. Build the provided CPU-intensive application
2. Run the application without any CPU constraints and observe resource usage
3. Re-run the application with the following CPU constraints and compare performance:
   - Limit to 0.5 CPUs
   - Limit to 1 CPU
   - Limit to 2 CPUs (if your host has multiple cores)
4. Document the differences in execution time and CPU utilization
5. Determine the optimal CPU allocation for this application

### Task 4: Memory Resource Management

Navigate to the `memory-usage-demo` directory:

```bash
cd ../memory-usage-demo
```

TODO:
1. Build the provided memory-intensive application
2. Run the application without any memory constraints and observe usage
3. Re-run the application with the following memory constraints:
   - Limit to 256MB
   - Limit to 512MB
   - Limit to 1GB
4. Observe what happens when the application exceeds its memory limit
5. Configure the application to gracefully handle memory constraints
6. Experiment with the OOM killer settings

### Task 5: Combining CPU and Memory Constraints

TODO:
1. Run the CPU-intensive application with both CPU and memory constraints
2. Run the memory-intensive application with both CPU and memory constraints
3. Observe how the combination of constraints affects performance
4. Document your findings on the interaction between different resource constraints

### Task 6: Resource Constraints in Production Scenarios

TODO:
1. Consider a web application with the following components:
   - Web server (Nginx)
   - Application server (Python Flask)
   - Database (PostgreSQL)
2. Determine appropriate resource allocations for each component
3. Implement these constraints using Docker run commands
4. Test the application under load and adjust constraints as needed
5. Document your resource allocation strategy and rationale

### Task 7: Resource Constraints in Docker Compose

TODO:
1. Create a docker-compose.yml file for the web application stack from Task 6
2. Add appropriate resource constraints for each service
3. Deploy the stack and observe resource utilization
4. Adjust constraints in the compose file and redeploy as needed
5. Document the pros and cons of setting resource constraints in Docker Compose

### Task 8: Monitoring with Advanced Tools

TODO:
1. Explore third-party monitoring tools compatible with Docker
2. Set up a simple monitoring stack using Prometheus and Grafana
3. Create dashboards to visualize container resource usage
4. Set up alerts for resource threshold violations
5. Document your monitoring setup and findings

### Task 9: Troubleshooting Resource-Related Issues

Common resource-related issues you might encounter:

TODO:
1. Diagnose and resolve the following scenarios:
   - Container being killed due to memory constraints
   - Container suffering from CPU throttling
   - Container experiencing disk I/O bottlenecks
2. Implement appropriate solutions for each issue
3. Document your troubleshooting process and resolutions

### Task 10: Resource Constraints Best Practices

TODO:
1. Research and document best practices for:
   - CPU allocation in containerized environments
   - Memory management for different application types
   - Storage constraints and considerations
   - Network resource management
2. Create a resource allocation strategy for a microservices application
3. Document your recommendations and the rationale behind them

## Testing Your Understanding

After completing the lab exercises, you should be able to:
- Apply appropriate resource constraints to containers based on application needs
- Monitor and analyze container resource usage effectively
- Troubleshoot and resolve resource-related issues
- Implement resource management best practices in production environments

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

- [Docker Resource Constraints Documentation](https://docs.docker.com/config/containers/resource_constraints/)
- [Docker Stats Command Reference](https://docs.docker.com/engine/reference/commandline/stats/)
- [Monitoring Docker](https://docs.docker.com/config/containers/runmetrics/)
- [Docker Compose Resource Constraints](https://docs.docker.com/compose/compose-file/compose-file-v3/#resources) 