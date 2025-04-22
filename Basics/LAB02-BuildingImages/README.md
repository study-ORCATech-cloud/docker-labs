# LAB02: Building Docker Images

This lab focuses on building custom Docker images using Dockerfiles, with a specific emphasis on Python applications. You'll learn how to create efficient, secure, and properly structured Docker images for your applications.

## Lab Overview

In this lab, you will:
- Create Dockerfiles for Python applications
- Understand the Dockerfile syntax and best practices
- Build and tag images
- Work with image layers and caching
- Implement multi-stage builds
- Use .dockerignore to exclude files
- Push images to Docker Hub

## Learning Objectives

- Understand how to create efficient Dockerfiles
- Learn best practices for containerizing Python applications
- Work with image tags and versions
- Implement Docker build context and .dockerignore
- Optimize images for size and security
- Use environment variables in containers
- Build multi-stage images for production

## Prerequisites

- Docker Engine installed
- Completion of LAB01-GettingStarted
- Basic understanding of Python
- Docker Hub account (for pushing images)

## Lab Projects

This lab includes two Python project examples:

1. **simple-flask-app**: A basic Flask web application that demonstrates fundamental Dockerfile concepts
2. **python-api-service**: A more complex API service with dependencies and environment configuration

## Lab Tasks

### Task 1: Understand Dockerfile Basics

Explore the anatomy of a Dockerfile and understand common instructions:

```dockerfile
# Comments begin with a hash
FROM base-image:tag          # Specifies the base image
WORKDIR /app                 # Sets the working directory
COPY . .                     # Copies files from host to container
RUN command                  # Executes commands during build
EXPOSE port                  # Documents which ports the container listens on
ENV NAME=value               # Sets environment variables
CMD ["executable", "param"]  # Defines the default command to run
```

Key Dockerfile instructions:
- **FROM**: Specifies the base image
- **WORKDIR**: Sets the working directory inside the container
- **COPY/ADD**: Copies files from the build context into the image
- **RUN**: Executes commands during the build process
- **EXPOSE**: Documents which ports the container will listen on
- **ENV**: Sets environment variables
- **CMD/ENTRYPOINT**: Defines what runs when the container starts

### Task 2: Build a Simple Flask Application

Navigate to the `simple-flask-app` directory and examine the application structure. Then build and run the image:

```bash
# Navigate to the project directory
cd simple-flask-app

# Build the image
docker build -t simple-flask-app:1.0 .

# Run the container
docker run -d -p 5000:5000 --name flask-demo simple-flask-app:1.0

# Test the application
curl http://localhost:5000
```

### Task 3: Implement Best Practices

Examine the `python-api-service` project which implements several Docker best practices:
- Using specific base image versions
- Creating a non-root user
- Separating dependency installation from code copying
- Properly handling environment variables
- Implementing health checks

Build and run this more advanced service:

```bash
# Navigate to the project
cd python-api-service

# Build the image with a tag
docker build -t python-api-service:1.0 .

# Run with environment variables
docker run -d -p 8000:8000 \
  -e API_KEY="demo-key" \
  -e LOG_LEVEL="info" \
  --name api-service \
  python-api-service:1.0

# Check it's running
curl http://localhost:8000/health
```

### Task 4: Use .dockerignore

Create and understand the purpose of a `.dockerignore` file to exclude unnecessary files from the build context:

```
# Example .dockerignore file
__pycache__/
*.py[cod]
*$py.class
.env
.venv
venv/
ENV/
.git
.gitignore
Dockerfile
README.md
```

### Task 5: Implement Multi-stage Builds

Understand how to use multi-stage builds to create smaller production images:

```dockerfile
# Build stage
FROM python:3.9 AS builder
WORKDIR /app
COPY requirements.txt .
RUN pip wheel --no-cache-dir --no-deps --wheel-dir /app/wheels -r requirements.txt

# Final stage
FROM python:3.9-slim
WORKDIR /app
COPY --from=builder /app/wheels /wheels
RUN pip install --no-cache /wheels/*
COPY . .
CMD ["python", "app.py"]
```

### Task 6: Push Images to Docker Hub

Tag and push your images to Docker Hub:

```bash
# Log in to Docker Hub
docker login

# Tag your image
docker tag python-api-service:1.0 yourusername/python-api-service:1.0

# Push to Docker Hub
docker push yourusername/python-api-service:1.0
```

## Real-World Applications

These Docker image building skills enable:
- Creating portable, reproducible application environments
- Implementing CI/CD pipelines for container deployments
- Distributing applications in a standardized format
- Ensuring consistent development and production environments
- Optimizing container size and security for production use

## Conclusion

In this lab, you've learned:
- How to write effective Dockerfiles for Python applications
- Best practices for containerizing applications
- How to optimize Docker images for production
- Using multi-stage builds for efficient images
- How to publish and distribute your Docker images

## Next Steps

Proceed to LAB03-Volumes to learn about Docker volumes for data persistence, container data management, and sharing data between containers and the host system.