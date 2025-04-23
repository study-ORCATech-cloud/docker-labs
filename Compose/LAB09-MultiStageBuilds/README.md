# LAB09: Multi-Stage Builds with Docker Compose

This lab focuses on optimizing Docker images using multi-stage builds in Docker Compose applications, demonstrating best practices for creating efficient, secure, and production-ready containers.

## Learning Objectives

- Understand multi-stage build concepts and benefits
- Create optimized Docker images with smaller footprints
- Implement efficient build caching strategies
- Separate build-time dependencies from runtime environments
- Apply multi-stage builds in Docker Compose applications
- Improve security through minimal runtime images
- Implement language-specific optimization techniques for Python applications
- Measure and compare image sizes before and after optimization

## Prerequisites

- Docker Engine installed
- Docker Compose v2 installed
- Basic understanding of Docker concepts
- Familiarity with Docker Compose from previous labs
- Basic Python knowledge (for sample applications)

## Multi-Stage Build Concepts

Multi-stage builds allow you to use multiple FROM statements in your Dockerfile, enabling you to:

1. **Separate Build and Runtime Environments**: Keep build tools out of the final image
2. **Reduce Image Size**: Include only what's necessary for the application to run
3. **Improve Security**: Fewer components mean fewer potential vulnerabilities
4. **Optimize Caching**: Build stages can be cached for faster rebuilds
5. **Simplify Workflows**: Combine multiple build steps into a single Dockerfile

## Lab Exercises

### Exercise 1: Basic Multi-Stage Builds

Learn the fundamentals of multi-stage builds with a simple Python application.

1. Compare traditional single-stage vs. multi-stage Dockerfiles
2. Build and run the application using Docker Compose
3. Analyze image size differences
4. Understand the basics of copying artifacts between stages

### Exercise 2: Advanced Dependency Management

Build on Exercise 1 with more complex dependency handling.

1. Implement proper caching of dependencies
2. Separate development and production dependencies
3. Reduce build time with optimized layer ordering
4. Implement different build arguments for various environments

### Exercise 3: Production-Grade Python Application

Create a production-ready Python web application with multi-stage builds.

1. Set up a Flask application with static assets
2. Implement a multi-stage build with separate stages for:
   - Base dependencies
   - Development environment
   - Testing
   - Production
3. Optimize asset handling with compression and minification
4. Configure proper environment variables and runtime settings

### Exercise 4: Real-World Microservices Application

Implement a complete microservices application with multi-stage builds.

1. Create multiple services, each with its own multi-stage Dockerfile
2. Implement shared base images for consistency
3. Set up a complete application using Docker Compose
4. Implement production readiness checks and optimizations
5. Manage build and deployment across environments

## Files Included

- `docker-compose.yml` - Base configuration for all exercises
- `/exercise1-4/` - Exercise-specific files and applications
- `/exercise1-4/docker-compose.yml` - Exercise-specific Docker Compose configurations
- `/exercise1-4/Dockerfile` - Multi-stage Dockerfiles for each exercise
- `/exercise1-4/app/` - Application source code for each exercise

## Project Structure

```
LAB09-MultiStageBuilds/
├── exercise1/
│   ├── app/
│   │   ├── app.py
│   │   └── requirements.txt
│   ├── docker-compose.yml
│   ├── Dockerfile
│   └── Dockerfile.original
├── exercise2/
│   ├── app/
│   │   ├── app.py
│   │   ├── requirements.txt
│   │   └── requirements-dev.txt
│   ├── docker-compose.yml
│   └── Dockerfile
├── exercise3/
│   ├── app/
│   │   ├── app.py
│   │   ├── static/
│   │   ├── templates/
│   │   ├── requirements.txt
│   │   └── requirements-dev.txt
│   ├── docker-compose.yml
│   └── Dockerfile
├── exercise4/
│   ├── api-service/
│   │   ├── app/
│   │   ├── Dockerfile
│   │   └── requirements.txt
│   ├── web-service/
│   │   ├── app/
│   │   ├── Dockerfile
│   │   └── requirements.txt
│   ├── db-service/
│   │   └── Dockerfile
│   ├── docker-compose.yml
│   └── docker-compose.prod.yml
└── README.md
```

## Lab Steps

### Step 1: Basic Multi-Stage Builds

Let's start by understanding the fundamentals of multi-stage builds:

```bash
cd exercise1
```

First, build the application using a traditional single-stage Dockerfile:

```bash
docker compose -f docker-compose.yml build app-original
docker compose -f docker-compose.yml up -d app-original
```

Now, build the application using a multi-stage Dockerfile:

```bash
docker compose -f docker-compose.yml build app
docker compose -f docker-compose.yml up -d app
```

Compare the image sizes:

```bash
docker images
```

You'll notice the multi-stage build produces a significantly smaller image. Access both applications to verify they work the same:

- Original app: http://localhost:8001
- Multi-stage app: http://localhost:8000

### Step 2: Advanced Dependency Management

In this exercise, we'll implement more sophisticated dependency management:

```bash
cd ../exercise2
docker compose build
docker compose up -d
```

This exercise demonstrates:
- Separating development and production dependencies
- Caching pip dependencies for faster rebuilds
- Using build arguments to customize the build process

Access the application at http://localhost:8010.

Try modifying the source code and rebuilding to see how the caching works:

```bash
docker compose build
docker compose up -d
```

### Step 3: Production-Grade Python Application

Now let's implement a more complete Python web application:

```bash
cd ../exercise3
docker compose build
docker compose up -d
```

This exercise demonstrates:
- Multi-stage builds for a Flask application with static assets
- Separate stages for base dependencies, development, testing, and production
- Asset optimization with compression and minification
- Proper runtime configuration

Access the application at http://localhost:8020.

You can also build the production version:

```bash
docker compose -f docker-compose.prod.yml build
docker compose -f docker-compose.prod.yml up -d
```

Access the production version at http://localhost:8021.

### Step 4: Real-World Microservices Application

Finally, let's implement a complete microservices application:

```bash
cd ../exercise4
docker compose build
docker compose up -d
```

This exercise ties everything together:
- Multiple services with their own multi-stage Dockerfiles
- Shared base images for consistency
- A complete application with frontend, API, and database
- Production readiness checks and optimizations

Access the application at http://localhost:8030.

You can also build and run the production version:

```bash
docker compose -f docker-compose.prod.yml build
docker compose -f docker-compose.prod.yml up -d
```

Access the production version at http://localhost:8031.

## Commands Reference

```bash
# Build images with multi-stage Dockerfile
docker compose build

# Build a specific service
docker compose build web-service

# Build with specific build arguments
docker compose build --build-arg BUILD_ENV=production

# View image sizes
docker images

# Check running containers
docker compose ps

# Check logs
docker compose logs

# Stop and remove resources
docker compose down
```

## Best Practices

- **Base Image Selection**: Choose minimal base images like python:3.11-slim or alpine
- **Layer Ordering**: Put infrequently changing layers earlier in the Dockerfile
- **Dependency Caching**: Copy requirements files first to leverage Docker's layer caching
- **Multi-stage Structure**: Use clear stage names with the `AS` keyword
- **Use .dockerignore**: Exclude unnecessary files from the build context
- **Minimize RUN Commands**: Combine commands to reduce layers
- **Non-root Users**: Run containers as non-root users for security
- **Build Arguments**: Use ARG instructions for build-time variability
- **Environment Variables**: Use ENV for runtime configuration
- **Health Checks**: Implement proper HEALTHCHECK instructions

## Security Considerations

- **Minimal Base Images**: Fewer packages mean fewer vulnerabilities
- **Updated Dependencies**: Keep base images and dependencies updated
- **Avoid Development Tools**: Don't include build tools in the final stage
- **Non-root Users**: Always run as a non-root user when possible
- **Secrets Handling**: Don't include secrets in the image layers
- **Image Scanning**: Scan images for vulnerabilities
- **Distroless Images**: Consider using distroless images for ultimate minimalism
- **Read-only Filesystem**: Mount filesystems read-only where possible

## Performance Optimizations

- **Caching Dependencies**: Copy and install dependencies before adding application code
- **Multi-stage Parallelism**: Build multiple stages in parallel when possible
- **Compiled Assets**: Pre-compile assets in build stages
- **Layer Optimization**: Minimize layer count and size for better caching
- **Shared Base Images**: Use shared base images across services
- **Build Context Optimization**: Keep build context small with .dockerignore

## Cleanup

When you're completely finished with all exercises, clean up all resources:

```bash
# Exercise 1
cd exercise1
docker compose down -v

# Exercise 2
cd ../exercise2
docker compose down -v

# Exercise 3
cd ../exercise3
docker compose down -v

# Exercise 4
cd ../exercise4
docker compose down -v

# Remove all unused images
docker image prune -a
```

## Troubleshooting

- **Build Failures**: Check for syntax errors in Dockerfile
- **Missing Dependencies**: Verify requirements files are copied correctly
- **Access Denied Errors**: Ensure proper file permissions
- **Port Conflicts**: Check for port conflicts with existing containers
- **Container Crashes**: Check logs with `docker compose logs`
- **Performance Issues**: Review image size and layer count

## Extensions

- **CI/CD Integration**: Implement multi-stage builds in CI/CD pipelines
- **Custom Base Images**: Create your own optimized base images
- **Language-specific Optimizations**: Implement specific optimizations for your language
- **Cross-architecture Builds**: Use multi-stage builds for multi-architecture support
- **Build Cache Warming**: Implement build cache warming in CI/CD pipelines

## Next Steps

After completing this lab, you'll be ready to move on to LAB10-ComposeNetworking to learn about advanced networking configurations in Docker Compose. 