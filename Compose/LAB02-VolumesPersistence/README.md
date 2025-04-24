# LAB02: Volume Management and Data Persistence

This lab focuses on implementing data persistence in Docker containers using volumes and bind mounts with Docker Compose.

## Learning Objectives

- Understand different types of Docker storage options
- Implement named volumes with Docker Compose
- Configure bind mounts for development environments
- Implement data persistence between container restarts
- Manage volume backup and restoration
- Share data between containers

## Prerequisites

- Docker Engine installed
- Docker Compose v2 installed
- Basic understanding of Docker concepts
- Completion of previous labs recommended

## Important Instructions

This lab is designed for hands-on learning. You are expected to:
- Implement Docker Compose volume configurations yourself
- Follow the TODOs in the provided YAML files
- Test volume persistence with various storage options
- Document your findings about how Docker volumes work

## Volume Concepts in Docker

Docker provides several options for persistent storage:

1. **Named Volumes**: Managed by Docker, portable, ideal for production data
2. **Bind Mounts**: Connect container paths to host filesystem, good for development
3. **tmpfs Mounts**: Stored in host memory only, useful for sensitive or temporary data

## Lab Structure

This lab contains a main `docker-compose.yml` file with TODO comments where you'll need to implement various volume configurations. The file is structured to support all four exercises, each demonstrating a different aspect of Docker volume management:

```
LAB02-VolumesPersistence/
│
├── docker-compose.yml       # Main configuration file with TODOs
├── exercise1/               # Basic volume persistence
│   ├── README.md            # Instructions for exercise 1
│   └── init.sql             # Database initialization script
│
├── exercise2/               # Development with bind mounts
│   ├── README.md            # Instructions for exercise 2
│   ├── Dockerfile           # Application container definition
│   └── app/                 # Application source code
│
├── exercise3/               # Sharing data between services
│   ├── README.md            # Instructions for exercise 3
│   ├── producer/            # Data producer service
│   └── consumer/            # Data consumer service
│
└── exercise4/               # Volume backup and restore
    ├── README.md            # Instructions for exercise 4
    ├── backup.sh            # Backup script
    ├── restore.sh           # Restore script
    └── backups/             # Directory for backup files
```

## Lab Exercises

### Exercise 1: Basic Volume Persistence

In this exercise, you'll create a simple database application that persists data between container restarts.

1. Configure a PostgreSQL container with a named volume
2. Store and retrieve data
3. Destroy and recreate the container to verify data persistence

### Exercise 2: Development Environment with Bind Mounts

Create a development environment for a web application where code changes reflect immediately.

1. Configure a web application with code mounted from the host
2. Make changes to the code and observe them in real-time
3. Configure proper development settings in Compose

### Exercise 3: Sharing Data Between Services

Set up a multi-container application that shares data between services.

1. Configure a data processing pipeline with shared volumes
2. Implement read-only volumes where appropriate
3. Test data flow between containers

### Exercise 4: Volume Backup and Restore

Learn how to back up and restore data from Docker volumes.

1. Configure a backup service with access to database volumes
2. Back up volume data to the host
3. Restore from backup to a new volume

## Getting Started

1. Review the main `docker-compose.yml` file and identify the TODOs
2. Read the README.md in each exercise directory for specific instructions
3. Implement the required volume configurations
4. Test each exercise following the instructions provided

## Commands Reference

```bash
# Create and start containers
docker-compose up -d

# View volume list
docker volume ls

# Inspect a volume
docker volume inspect [VOLUME_NAME]

# Backup a volume
docker run --rm -v [VOLUME_NAME]:/source -v $(pwd):/backup alpine tar -czvf /backup/backup.tar.gz -C /source .

# Restore a volume
docker run --rm -v [VOLUME_NAME]:/target -v $(pwd):/backup alpine sh -c "tar -xzvf /backup/backup.tar.gz -C /target"
```

## Cleanup

When you're completely finished with all exercises, you can clean up all resources with:

```bash
# Stop all containers defined in docker-compose.yml
docker-compose down

# Remove all volumes created for this lab (WARNING: This will delete all persistent data)
docker volume rm lab02_postgres_data lab02_shared_data

# List and verify no volumes remain from this lab
docker volume ls | grep lab02
```

## Best Practices

- Use named volumes for production data persistence
- Use bind mounts during development for real-time code changes
- Always name your volumes for easier management
- Implement backup strategies for important data
- Consider volume drivers for specific storage needs

## Troubleshooting

- **Permission issues**: Check file ownership on bind mounts
- **Missing data**: Verify volume mounting path inside container
- **Performance problems**: Check volume driver and host I/O performance

## Next Steps

After completing this lab, you'll be ready to move on to LAB03-EnvironmentConfig to learn about managing application configurations across environments. 