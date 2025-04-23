# Docker Debugging Exercise

This directory contains a buggy Flask application with multiple issues that need to be fixed.

## The Challenge

The application has intentional bugs in both the code and the Docker configuration. Your task is to:

1. Build and run the container
2. Use Docker debugging techniques to identify the issues
3. Fix the problems one by one
4. Create a stable, production-ready container

## Known Issues

This application has the following types of issues:

- Container build problems
- Application startup failures
- Runtime errors
- Performance problems
- Resource leaks
- Configuration issues

## Getting Started

Try to build and run the application:

```bash
# Build the image
docker build -t debug-app:buggy .

# Try to run the container
docker run -d -p 8080:5000 --name debug-container debug-app:buggy
```

## Debugging Steps

1. Check if the container is running:
   ```bash
   docker ps -a
   ```

2. Examine the container logs:
   ```bash
   docker logs debug-container
   ```

3. Try to execute commands inside the container:
   ```bash
   docker exec -it debug-container /bin/bash
   ```

4. Check container resource usage:
   ```bash
   docker stats debug-container
   ```

## Fix Checklist

After identifying issues, fix them one by one:

- [ ] Fix logging configuration
- [ ] Fix port configuration mismatch
- [ ] Fix the Dockerfile working directory
- [ ] Fix API endpoint paths
- [ ] Fix environment variable handling
- [ ] Fix memory leak
- [ ] Fix concurrency issues
- [ ] Add proper error handling
- [ ] Implement healthcheck
- [ ] Fix performance bottlenecks

## Reference Solutions

For reference (after you've tried to fix the issues yourself), you can look at:

- `fixed_app.py` - A corrected version of the application
- `fixed_Dockerfile` - A corrected Dockerfile

## Running the Fixed Application

After implementing your fixes, you should be able to build and run the application successfully:

```bash
# Build the fixed image
docker build -t debug-app:fixed -f your_fixed_Dockerfile .

# Run the fixed container
docker run -d -p 5000:5000 --name fixed-container debug-app:fixed

# Test the endpoints
curl http://localhost:5000/
curl http://localhost:5000/health
```

## Learning Objectives

This exercise helps you practice:

- Reading Docker logs and error messages
- Debugging running containers
- Fixing Dockerfile issues
- Resolving application runtime problems
- Implementing proper Docker configurations
- Understanding common container pitfalls 