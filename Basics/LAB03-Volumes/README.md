# LAB03: Working with Docker Volumes

This lab explores how to use Docker volumes to manage data persistence, share data between containers, and between host and container.

## Lab Overview

In this lab, you will:
- Understand the difference between bind mounts, volumes, and tmpfs
- Create and use named volumes in Docker
- Share data between host and containers
- Mount host directories into containers (bind mounts)
- Manage volume lifecycle (create, list, remove)
- Complete hands-on TODO exercises to implement volume solutions

## Learning Objectives

- Learn how to persist container data with Docker volumes
- Understand when to use bind mounts vs. named volumes vs. tmpfs
- Practice mounting host directories for development
- Manage Docker volumes from the CLI
- Implement volume sharing between multiple containers

## Prerequisites

- Docker Engine installed
- Completion of LAB01-GettingStarted and LAB02-BuildingImages
- Basic understanding of Flask applications

## Lab Projects

This lab includes two demo projects:

1. **volume-demo**: A basic Flask app demonstrating volume usage for data persistence
2. **multi-container-demo**: A more complex setup showing volume sharing between containers

Both projects contain TODOs that you'll need to implement to complete the lab.

## Lab Tasks

### Task 1: Explore Volume Types

1. **Bind Mount** - Mount a host directory into a container:
   ```bash
   # TODO: Run a container with a bind mount
   # Mount the volume-demo/data directory from your host into /app/data in the container
   docker run -d \
     --name bind-demo \
     -v $(pwd)/volume-demo/data:/app/data \
     python:3.9-slim sleep infinity
   ```

2. **Named Volume** - Create and use a named volume:
   ```bash
   # TODO: Create a named volume
   docker volume create demo-volume
   
   # TODO: Run a container with the named volume
   docker run -d \
     --name volume-demo \
     -v demo-volume:/app/data \
     python:3.9-slim sleep infinity
   ```

3. **Tmpfs** - Use tmpfs for in-memory storage:
   ```bash
   # TODO: Run a container with a tmpfs mount
   docker run -d \
     --name tmpfs-demo \
     --tmpfs /app/data \
     python:3.9-slim sleep infinity
   ```

### Task 2: Inspect and Manage Volumes

List volumes:
```bash
docker volume ls
```

Inspect a volume:
```bash
docker volume inspect demo-volume
```

Remove containers and volumes:
```bash
docker rm -f bind-demo volume-demo tmpfs-demo
docker volume rm demo-volume
```

### Task 3: Basic Volume Persistence Demo

Navigate to the `volume-demo` directory and examine the code:

```bash
cd volume-demo
```

You'll need to:
1. Understand how the application uses the data directory
2. Complete the TODOs in the Dockerfile
3. Build and run the application with a named volume

After implementing the TODOs, run the application:

```bash
# Build the image
docker build -t volume-demo:1.0 .

# Run with a named volume
docker run -d \
  --name volume-demo-app \
  -v demo-data:/app/data \
  -p 5000:5000 \
  volume-demo:1.0
```

Test the application's persistence:
```bash
# Write data
curl -X POST -H "Content-Type: application/json" \
  -d '{"content": "Hello, Volumes!"}' \
  http://localhost:5000/write

# Read data
curl http://localhost:5000/read

# Stop and remove the container (but keep the volume)
docker stop volume-demo-app
docker rm volume-demo-app

# Start a new container using the same volume
docker run -d \
  --name volume-demo-app-2 \
  -v demo-data:/app/data \
  -p 5000:5000 \
  volume-demo:1.0

# Verify data persisted
curl http://localhost:5000/read
```

### Task 4: Multi-Container Volume Sharing

Navigate to the `multi-container-demo` directory:

```bash
cd multi-container-demo
```

This more advanced demo requires you to:
1. Complete the TODOs in the API's Dockerfile
2. Implement the Docker commands to set up shared volumes
3. Test communication between containers through shared volumes

Read the README.md in the multi-container-demo directory for specific instructions.

## TODO Exercises

In addition to implementing the Dockerfile TODOs, complete these exercises:

### TODO 1: Volume Backup and Restore
- Create a named volume with some data in it
- Create a backup of this volume to a tar file
- Delete the volume
- Restore the volume from your backup
- Verify your data is intact

### TODO 2: Implement a Development Environment
- Modify the volume-demo app to use bind mounts for development
- Set up a configuration so that code changes on your host automatically appear in the container
- Add a file watcher (optional) or manually restart the application to see changes

### TODO 3: Database Volume Management
- Run a database container (e.g., PostgreSQL, MySQL) with a named volume
- Create a database and add some data
- Stop and remove the container (keeping the volume)
- Start a new database container with the same volume
- Verify your data is still available

### TODO 4: Implement Volume Sharing in docker-compose.yml
- Create a docker-compose.yml file for the multi-container demo
- Define all necessary volumes and volume mappings
- Use the compose file to start and stop the entire application

## Clean Up

To clean up resources after completing this lab:

```bash
# Stop and remove all running containers
docker stop $(docker ps -a -q)
docker rm $(docker ps -a -q)

# List all volumes
docker volume ls

# Remove all unused volumes
docker volume prune

# Or remove specific volumes
docker volume rm demo-data web-content api-data db-data
```

## Real-World Applications

Using volumes is essential for stateful applications, databases, and sharing configuration or data between containers. The techniques you've learned are valuable for:

- Database persistence in production environments
- Sharing configuration files between services
- Development environments with hot-reload capabilities
- Backup and disaster recovery strategies
- Content management systems and file storage

## Next Steps

Proceed to LAB04-Layers to learn about Docker image layers and optimization. 