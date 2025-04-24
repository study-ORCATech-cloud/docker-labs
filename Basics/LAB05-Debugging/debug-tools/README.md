# Docker Debugging Tools

This directory contains information about specialized tools that can help with debugging Docker containers.

## Overview

As a DevOps engineer, you need to be familiar with a variety of debugging tools to diagnose and resolve issues with containerized applications. This directory contains scripts and instructions for using various debugging tools to troubleshoot Docker containers.

## Learning Objectives

- Learn how to use specialized debugging tools for Docker
- Understand when to use each tool based on the problem
- Gain hands-on experience with real-world debugging scenarios
- Develop a systematic approach to container troubleshooting

## Available Tools

### 1. Dive - Image Layer Analysis

[Dive](https://github.com/wagoodman/dive) is a tool for exploring Docker images, layer contents, and discovering ways to shrink the size of your Docker/OCI image.

**Exercise 1**: Analyze the debug-app image for inefficient layers
```bash
docker run --rm -it \
  -v /var/run/docker.sock:/var/run/docker.sock \
  wagoodman/dive:latest debug-app:buggy
```

**TODO**: Document which layers contribute most to the image size and identify potential optimizations.

### 2. Netshoot - Network Debugging Toolkit

[Netshoot](https://github.com/nicolaka/netshoot) is a container with a set of networking tools useful for troubleshooting issues with Docker containers.

**Exercise 2**: Debug network connectivity issues
```bash
# First, run the debug-app
docker run -d --name network-test debug-app:buggy

# Then, attach netshoot to analyze its network
docker run --rm -it \
  --network container:network-test \
  nicolaka/netshoot
```

**TODO**: Use the networking tools in netshoot to perform:
- Hostname resolution tests
- Port connectivity checks
- Network latency analysis
- Document your findings and methodology

### 3. Resource Monitoring

Resource constraints are a common source of container problems.

**Exercise 3**: Monitor container resource usage

1. Run the monitor.sh script:
```bash
chmod +x monitor.sh
./monitor.sh
```

2. In another terminal, run a container with resource constraints:
```bash
docker run -d --name resource-test --memory=50m --cpu-shares=50 debug-app:buggy
```

**TODO**: Document the resource usage patterns you observe. What happens when the container reaches its memory limit?

### 4. Container Health Checks

Healthchecks help detect when a container is not functioning properly.

**Exercise 4**: Implement and test container health checks

1. Run the healthcheck.sh script on a container:
```bash
chmod +x healthcheck.sh
./healthcheck.sh debug-container
```

**TODO**: Create your own improved version of the healthcheck.sh script that includes additional checks:
- File system usage check
- Check for error patterns in logs
- Application-specific status checks

### 5. Network Inspector

Networking issues are among the most complex to debug in containerized environments.

**Exercise 5**: Debug container networking

1. Run the network-inspector.sh script:
```bash
chmod +x network-inspector.sh
./network-inspector.sh debug-container
```

**TODO**: Create a test setup with multiple containers in different networks and use the network inspector to map the connectivity between them. Document your findings.

### 6. Clean-Exit Script

Managing exited containers is an important housekeeping task.

**Exercise 6**: Clean up exited containers and analyze failure patterns

1. Run the clean-exit.sh script:
```bash
chmod +x clean-exit.sh
./clean-exit.sh
```

**TODO**: Enhance the clean-exit.sh script to:
- Categorize containers by exit code
- Save logs from exited containers before removing them
- Create a summary report of container failures

## Advanced Debugging Techniques

### Creating a Custom Debugging Container

**Exercise 7**: Create your own debugging container

**TODO**: Create a Dockerfile for a custom debugging container that includes:
- Network troubleshooting tools
- Disk and memory analysis utilities
- Log parsing tools
- A simple web interface to view results

### Systematic Debugging Approach

Develop a systematic approach to debugging Docker containers:

1. **Gather information**: Collect logs, inspect configuration, check resource usage
2. **Form a hypothesis**: Based on the evidence, identify potential causes
3. **Test your hypothesis**: Make a targeted change to test your theory
4. **Implement a solution**: Apply a permanent fix
5. **Verify and document**: Ensure the fix works and document the process

**TODO**: Apply this approach to debug the Flask application from the debug-app directory and document each step in your process.

## Assessment Criteria

You'll be assessed on:

1. Your ability to use the debugging tools effectively
2. The improvements you make to the provided scripts
3. Your systematic approach to debugging
4. The quality of your documentation and findings

## Additional Resources

- [Docker Debugging Best Practices](https://docs.docker.com/engine/reference/commandline/container_inspect/)
- [Docker Troubleshooting Guide](https://success.docker.com/article/troubleshooting-container-networking)
- [Container Performance Analysis](https://docs.docker.com/config/containers/resource_constraints/)

## Resources

- [Docker Documentation - Logs](https://docs.docker.com/config/containers/logging/)
- [Docker Documentation - Debug](https://docs.docker.com/engine/reference/commandline/container_inspect/)
- [Docker Troubleshooting Guide](https://success.docker.com/article/troubleshooting-container-networking) 