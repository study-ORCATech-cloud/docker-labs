# Real-World Application Refactoring

This directory contains a more complex Flask application with Redis caching and a Dockerfile that exhibits many common real-world issues. Your task is to refactor it using all the best practices you've learned.

## The Real-World Challenge

In real-world applications, Dockerfiles often:
- Accumulate issues over time
- Mix different concerns
- Lack security considerations
- Have inefficient layer structures
- Don't consider production requirements

## Project Structure

- `app.py`: A Flask REST API with Redis caching and external API calls
- `requirements.txt`: Python dependencies
- `Dockerfile`: A problematic Dockerfile with multiple issues

## Task: Refactor a Real-World Dockerfile

The goal is to apply all the best practices you've learned to refactor the Dockerfile:
1. Optimize layer structure and caching
2. Implement security best practices
3. Use multi-stage builds
4. Add proper health checks
5. Set up proper process management

## Instructions

1. Review the provided real-world application:
   - Analyze the `app.py` to understand dependencies and requirements
   - Review the `Dockerfile` and identify all issues

2. Build the original image:
   ```bash
   docker build -t real-world:original .
   ```

3. Apply all best practices to create a significantly improved Dockerfile:
   - Use an appropriate base image
   - Optimize layer structure
   - Implement proper caching
   - Set up a non-root user
   - Add health checks
   - Implement proper process management
   - Use build arguments for configurability
   - Add proper labeling and documentation
   - Remove unnecessary packages
   - Manage secrets properly

4. Build your refactored image:
   ```bash
   docker build -t real-world:optimized -f Dockerfile.optimized .
   ```

5. Compare the original and optimized images:
   ```bash
   docker images real-world
   docker history real-world:original
   docker history real-world:optimized
   ```

6. Test both images to ensure functionality is preserved:
   ```bash
   # First terminal: Redis
   docker run --name redis -d redis:alpine

   # Second terminal: Original app
   docker run --name app-original --link redis:redis -p 8080:8080 real-world:original

   # Third terminal: Optimized app
   docker run --name app-optimized --link redis:redis -p 8081:8080 real-world:optimized

   # Fourth terminal: Test both
   curl http://localhost:8080/health
   curl http://localhost:8081/health
   ```

## Common Real-world Dockerfile Issues

- **Bloated base images**: Using full Ubuntu/Debian instead of slim/alpine
- **Unnecessary packages**: Installing dev tools not needed at runtime
- **Poor layer caching**: Not separating dependency installation from code changes
- **Security issues**: Running as root, hardcoded secrets
- **No health checks**: Container orchestrators can't properly monitor the app
- **Lack of multi-stage builds**: Including build tools in the final image
- **Hard-coded configurations**: Not using environment variables or build arguments

## TODO

Complete the following tasks:
1. Analyze the provided real-world application Dockerfile
2. Apply all best practices you've learned to refactor it
3. Compare before and after: image size, build time, security, maintainability
4. Document all the improvements you made
5. Create a presentation explaining your optimization strategy 