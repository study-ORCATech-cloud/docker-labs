# LAB01: Getting Started with Docker

This lab will introduce you to Docker basics, including installation, common commands, and running your first containers.

## Lab Overview

In this lab, you will:
- Install Docker Engine on your system
- Learn about Docker's architecture
- Run pre-built Docker containers
- Understand basic Docker commands
- Manage container lifecycle
- Access container logs and shell
- Complete hands-on TODO exercises to reinforce your learning
- Implement required code in Dockerfile and app.py

## Learning Objectives

- Install Docker Engine
- Understand Docker architecture
- Run your first container
- Learn basic Docker commands
- Pull images from Docker Hub
- List and manage containers
- Work with container logs
- Build a custom Docker image

## Prerequisites

- Linux, macOS, or Windows system
- Administrative/sudo access for installation
- Internet connection
- Basic Python knowledge (for code implementation tasks)

## Lab Tasks

### Task 1: Docker Installation

Follow the official Docker installation guide for your operating system:
- [Install on Windows](https://docs.docker.com/desktop/install/windows-install/)
- [Install on macOS](https://docs.docker.com/desktop/install/mac-install/)
- [Install on Linux](https://docs.docker.com/engine/install/)

Verify your installation:

```bash
docker version
docker info
```

### Task 2: Run Your First Container

Run a simple "Hello World" container:

```bash
docker run hello-world
```

You should see output explaining that your installation is working correctly.

### Task 3: Working with Basic Commands

Try these essential Docker commands:

```bash
# List all containers (running and stopped)
docker ps -a

# Pull an image from Docker Hub
docker pull nginx

# Run an nginx web server in the background
docker run -d -p 8080:80 --name my-nginx nginx

# Check that it's running
docker ps

# Access the web server in your browser at http://localhost:8080

# See container logs
docker logs my-nginx

# Stop the container
docker stop my-nginx

# Remove the container
docker rm my-nginx
```

### Task 4: Interactive Containers

Run a container in interactive mode:

```bash
# Run a bash shell in an Ubuntu container
docker run -it --name ubuntu-test ubuntu bash

# Inside the container, try some Linux commands
ls
cat /etc/os-release
exit
```

### Task 5: Container Management

Try these container management commands:

```bash
# Start a container in the background
docker run -d --name sleeper ubuntu sleep 1000

# Pause the container
docker pause sleeper

# Unpause the container
docker unpause sleeper

# Stop the container
docker stop sleeper

# Start it again
docker start sleeper

# Execute a command in a running container
docker exec -it sleeper bash

# Exit the container shell
exit
```

### Task 6: Clean Up

Clean up containers and images:

```bash
# Stop all running containers
docker stop $(docker ps -q)

# Remove all stopped containers
docker container prune

# List all images
docker images

# Remove an image
docker rmi hello-world
```

### Task 7: Code Implementation (Required)

This lab includes a custom demo application to practice Docker commands. Before running the demo, you need to implement several TODOs in the code:

#### 7.1 Complete the Dockerfile

Open the `Dockerfile` in this directory and implement the TODOs:
- Choose an appropriate base image
- Set up the working directory
- Copy and install requirements
- Copy the application code
- Expose the correct port
- Set the command to run the application

#### 7.2 Implement Missing Functionality in app.py

Open the `app.py` file and implement:
1. The container ID extraction code in the `container_info()` function
2. A new route at `/env-vars` that displays environment variables

#### 7.3 Run the Demo Application

After implementing the TODOs, run the demo:

```bash
# On Linux/macOS
chmod +x run-demo.sh
./run-demo.sh

# On Windows
run-demo.bat
```

If you've implemented everything correctly, you should see the web application at http://localhost:8080.

## TODO Exercises

Complete the following exercises to practice what you've learned. For each exercise, document the commands you used and the output you observed.

### TODO 1: Pull and Run a Redis Container
- Pull the official Redis image (latest tag)
- Run a Redis container named "my-redis" in detached mode
- Verify it's running with the appropriate Docker command
- Get the logs of the Redis container
- Stop and remove the container

### TODO 2: Create and Manage an Alpine Container
- Create an Alpine Linux container in interactive mode with a bash shell
- Inside the container, create a file called `/tmp/hello.txt` with the content "Hello from Docker!"
- Exit the container
- Start the same container again
- Verify your file still exists at `/tmp/hello.txt`
- Remove the container

### TODO 3: Container Resource Limits
- Run an Nginx container named "limited-nginx" with these resource constraints:
  - Memory limit: 200MB
  - CPU limit: 0.5 CPUs
  - Expose port 8888 on your host to port 80 in the container
- Verify the container is running with the resource limits
- Access the Nginx welcome page at http://localhost:8888
- Stop and remove the container

### TODO 4: Running Multiple Containers
- Run three different containers simultaneously:
  - httpd (Apache) container on port 8081
  - nginx container on port 8082
  - python:3.9-alpine container running "python -m http.server 80" on port 8083
- Verify all three containers are running
- List all running containers showing only container IDs
- Stop and remove all running containers with a single command for each operation

## Real-World Applications

These basic Docker skills enable:
- Running applications without installation complexity
- Testing software in isolated environments
- Creating reproducible development environments
- Deploying applications consistently across different systems

## Conclusion

In this lab, you've learned:
- How to install Docker
- Running, stopping, and removing containers
- Pulling images from Docker Hub
- Working with container logs
- Running containers in interactive mode
- Building and running a simple containerized application
- Implementing real Docker configuration files

After completing this lab and the TODO exercises, you should be comfortable with basic Docker commands and container management.

## Cleanup

Make sure to clean up all resources created during this lab:

```bash
# Stop all running containers
docker stop $(docker ps -q)

# Remove all containers
docker rm $(docker ps -a -q)

# Optionally, remove the images you pulled
docker rmi nginx redis httpd python:3.9-alpine
```

## Next Steps

Proceed to LAB02-BuildingImages to learn about building custom Docker images with Dockerfiles. 