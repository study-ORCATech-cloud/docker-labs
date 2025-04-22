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

## Learning Objectives

- Install Docker Engine
- Understand Docker architecture
- Run your first container
- Learn basic Docker commands
- Pull images from Docker Hub
- List and manage containers
- Work with container logs

## Prerequisites

- Linux, macOS, or Windows system
- Administrative/sudo access for installation
- Internet connection

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

### Task 7: Run the Lab Demo Application

This lab includes a custom demo application that helps you practice Docker commands. The demo is a simple Python Flask web application that shows container information when you access it.

To run the demo:

#### Option 1: Using the helper script (recommended for beginners)

```bash
# On Linux/macOS
chmod +x run-demo.sh
./run-demo.sh

# On Windows
run-demo.bat
```

#### Option 2: Manual build and run

```bash
# Build the image
docker build -t docker-getting-started-py .

# Run the container
docker run -d -p 8080:80 --name docker-lab-py docker-getting-started-py

# Access the application in your browser at http://localhost:8080
```

After starting the demo application, practice these commands:

```bash
# View logs
docker logs docker-lab-py

# Access the container shell
docker exec -it docker-lab-py bash

# Stop and remove the container
docker stop docker-lab-py
docker rm docker-lab-py
```

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

## Next Steps

Proceed to LAB02-BuildingImages to learn about building custom Docker images with Dockerfiles. 