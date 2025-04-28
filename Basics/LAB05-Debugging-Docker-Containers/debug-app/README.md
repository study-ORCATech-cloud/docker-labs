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

## TODO Checklist

After identifying issues, implement fixes for each one:

- [ ] Fix the Dockerfile working directory issue (TODO 1)
- [ ] Improve dependency installation (TODO 2)
- [ ] Fix file copying in the Dockerfile (TODO 3)
- [ ] Resolve port configuration mismatch (TODO 4)
- [ ] Fix application execution path (TODO 5)
- [ ] Implement container healthcheck (TODO 6)
- [ ] Set required environment variables (TODO 7)
- [ ] Create necessary log directories (TODO 8)
- [ ] Fix logging configuration in the app (TODO 1 in app.py)
- [ ] Resolve memory leak issues (TODO 2 in app.py)
- [ ] Fix thread synchronization (TODO 3 in app.py)
- [ ] Align port configuration with Dockerfile (TODO 4 in app.py)
- [ ] Fix unreachable endpoints (TODO 5 in app.py)
- [ ] Implement thread-safe operations (TODO 6 in app.py)
- [ ] Add memory limits to prevent leaks (TODO 7 in app.py)
- [ ] Add proper error handling (TODO 8 in app.py)
- [ ] Fix blocking operations (TODO 9 in app.py)
- [ ] Implement proper environment variable handling (TODO 10 in app.py)

## Important Note

You need to implement your own solutions for each issue. Don't copy solutions from external sources - the goal is to understand Docker debugging techniques and develop your problem-solving skills.

## Running Your Fixed Application

After implementing your fixes, you should be able to build and run the application successfully:

```bash
# Build your fixed image
docker build -t debug-app:fixed .

# Run your fixed container
docker run -d -p 5000:5000 --name fixed-container debug-app:fixed

# Test the endpoints
curl http://localhost:5000/
curl http://localhost:5000/health
```

## Testing Your Solutions

To verify your fixes are working:

1. All endpoints should be accessible without errors
2. The container should remain stable under load
3. The application should handle errors gracefully
4. The container should pass its healthcheck
5. Logs should be written correctly
6. The application should use resources efficiently

## Learning Objectives

This exercise helps you practice:

- Reading Docker logs and error messages
- Debugging running containers
- Fixing Dockerfile issues
- Resolving application runtime problems
- Implementing proper Docker configurations
- Understanding common container pitfalls 