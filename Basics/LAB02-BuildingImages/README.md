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
- Complete hands-on TODO exercises to implement Docker best practices

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

In both projects, you'll need to implement the Dockerfiles based on the provided TODO instructions.

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

Navigate to the `simple-flask-app` directory and examine the application structure:

```bash
# Navigate to the project directory
cd simple-flask-app
```

Read through the files and note the TODO comments. You'll need to:

1. Complete the `Dockerfile` by implementing the TODO sections
2. Make any necessary adjustments to the application code

After implementing the TODOs, build and run the image:

```bash
# Build the image
docker build -t simple-flask-app:1.0 .

# Run the container
docker run -d -p 5000:5000 --name flask-demo simple-flask-app:1.0

# Test the application
curl http://localhost:5000
```

### Task 3: Implement Best Practices

Now examine the `python-api-service` project. This project requires you to implement several Docker best practices:

- Using specific base image versions
- Creating a non-root user
- Separating dependency installation from code copying
- Properly handling environment variables
- Implementing health checks

Complete the TODOs in the `Dockerfile` and then build and run this more advanced service:

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

Create or update the `.dockerignore` file with appropriate rules to exclude unnecessary files from the build context:

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

Analyze how this affects build time and context size.

### Task 5: Implement Multi-stage Builds

For the python-api-service project, complete the multi-stage build implementation in the Dockerfile:

```dockerfile
# Example structure (you'll need to implement the details):

# Build stage
FROM python:3.9 AS builder
# TODO: Implement build stage instructions

# Final stage
FROM python:3.9-slim
# TODO: Implement final stage instructions
```

Consider how this improves the final image size and security.

### Task 6: Push Images to Docker Hub

Tag and push your completed images to Docker Hub:

```bash
# Log in to Docker Hub
docker login

# Tag your image
docker tag python-api-service:1.0 yourusername/python-api-service:1.0

# Push to Docker Hub
docker push yourusername/python-api-service:1.0
```

## TODO Exercises

In addition to implementing the Dockerfile TODOs, complete these exercises:

### TODO 1: Optimize the Simple Flask App
- Modify the simple-flask-app Dockerfile to use a smaller base image
- Add a custom healthcheck to the Dockerfile
- Add a new endpoint to the Flask app that returns the container's hostname
- Build and test your optimized image

### TODO 2: Secure the Python API Service
- Implement proper user creation and permissions in the Dockerfile
- Add an environment variable that controls whether debug mode is enabled
- Implement a new security feature (e.g., rate limiting, additional auth)
- Build and test your secured image

### TODO 3: Create a Multi-stage Build for Both Projects
- Convert both projects to use multi-stage builds
- Compare the image sizes before and after
- Document the benefits of your approach

### TODO 4: Implement a CI/CD Pipeline Configuration
- Create a simple CI/CD pipeline configuration file (e.g., GitHub Actions, GitLab CI)
- Configure it to build, test, and push your Docker images
- Include security scanning in your pipeline

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

After completing the TODOs and exercises, you'll have practical experience with Docker image building best practices.

## Cleanup

To clean up resources after completing this lab:

```bash
# Stop and remove containers
docker stop flask-demo api-service
docker rm flask-demo api-service

# Optionally remove images
docker rmi simple-flask-app:1.0 python-api-service:1.0
```

## Next Steps

Proceed to LAB03-Volumes to learn about Docker volumes for data persistence, container data management, and sharing data between containers and the host system.