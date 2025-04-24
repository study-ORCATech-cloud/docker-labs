# LAB02: Volume Management and Data Persistence - Solutions

This document provides reference solutions to the Docker Compose volume configurations in LAB02. These solutions are meant to be reviewed **after** you have attempted to implement the configurations yourself.

## Main Docker Compose File Solution

Here's the complete `docker-compose.yml` file with all volume configurations implemented:

```yaml
version: '3.8'

services:
  # Exercise 1: Basic Volume Persistence with PostgreSQL
  postgres-db:
    image: postgres:14
    container_name: postgres-persistence
    environment:
      POSTGRES_PASSWORD: example
      POSTGRES_USER: dbuser
      POSTGRES_DB: persistence_demo
    volumes:
      - postgres_data:/var/lib/postgresql/data
      - ./exercise1/init.sql:/docker-entrypoint-initdb.d/init.sql
    ports:
      - "5432:5432"
    networks:
      - lab02_network

  # Exercise 2: Development Environment with Bind Mounts
  webapp:
    build: ./exercise2
    container_name: webapp-dev
    volumes:
      - ./exercise2/app:/app
    ports:
      - "8080:8080"
    environment:
      - FLASK_ENV=development
      - FLASK_APP=app.py
      - FLASK_DEBUG=1
    networks:
      - lab02_network
    depends_on:
      - postgres-db

  # Exercise 3: Sharing Data Between Services
  data-producer:
    build: ./exercise3/producer
    container_name: data-producer
    volumes:
      - shared_data:/shared-data
    networks:
      - lab02_network

  data-consumer:
    build: ./exercise3/consumer
    container_name: data-consumer
    volumes:
      - shared_data:/shared-data:ro # Read-only mount
    depends_on:
      - data-producer
    networks:
      - lab02_network

  # Exercise 4: Volume Backup and Restore
  backup-service:
    image: alpine:latest
    container_name: backup-service
    volumes:
      - postgres_data:/source:ro # Source volume to backup (read-only)
      - ./exercise4/backups:/backups # Backup destination on host
    command: >
      sh -c "echo 'Backup service ready. Run backup or restore commands manually.'"
    networks:
      - lab02_network

networks:
  lab02_network:
    driver: bridge

volumes:
  postgres_data:
    name: lab02_postgres_data
  shared_data:
    name: lab02_shared_data
```

## Exercise 1: Basic Volume Persistence Solution

```yaml
# PostgreSQL service with named volume
postgres-db:
  image: postgres:14
  container_name: postgres-persistence
  environment:
    POSTGRES_PASSWORD: example
    POSTGRES_USER: dbuser
    POSTGRES_DB: persistence_demo
  volumes:
    - postgres_data:/var/lib/postgresql/data # Named volume for database files
    - ./exercise1/init.sql:/docker-entrypoint-initdb.d/init.sql # Bind mount for initialization
  ports:
    - "5432:5432"
  networks:
    - lab02_network
```

This configuration:
- Creates a named volume `postgres_data` for persistent database storage
- Mounts the initialization SQL script as a bind mount
- The volume is created as `lab02_postgres_data` with explicit naming

## Exercise 2: Development Environment Solution

```yaml
# Web application with bind mount for development
webapp:
  build: ./exercise2
  container_name: webapp-dev
  volumes:
    - ./exercise2/app:/app # Bind mount for local development files
  ports:
    - "8080:8080"
  environment:
    - FLASK_ENV=development
    - FLASK_APP=app.py
    - FLASK_DEBUG=1
  networks:
    - lab02_network
  depends_on:
    - postgres-db
```

This configuration:
- Creates a bind mount that maps the local `./exercise2/app` directory to `/app` in the container
- Allows for real-time code changes to be reflected immediately
- Sets development environment variables for Flask

## Exercise 3: Sharing Data Solution

```yaml
# Producer service with shared volume
data-producer:
  build: ./exercise3/producer
  container_name: data-producer
  volumes:
    - shared_data:/shared-data # Shared volume with read-write access
  networks:
    - lab02_network

# Consumer service with read-only access to shared volume
data-consumer:
  build: ./exercise3/consumer
  container_name: data-consumer
  volumes:
    - shared_data:/shared-data:ro # Read-only mount of the shared volume
  depends_on:
    - data-producer
  networks:
    - lab02_network
```

This configuration:
- Creates a named volume `shared_data` that both services can access
- The producer has read-write access to the volume
- The consumer has read-only access (`:ro` flag) for security
- The volume is created as `lab02_shared_data` with explicit naming

## Exercise 4: Backup and Restore Solution

```yaml
# Backup service with volume and host directory mounts
backup-service:
  image: alpine:latest
  container_name: backup-service
  volumes:
    - postgres_data:/source:ro # Read-only access to PostgreSQL data volume
    - ./exercise4/backups:/backups # Bind mount for storing backups on host
  command: >
    sh -c "echo 'Backup service ready. Run backup or restore commands manually.'"
  networks:
    - lab02_network
```

This configuration:
- Mounts the PostgreSQL data volume as read-only at `/source`
- Mounts the local `./exercise4/backups` directory at `/backups`
- Allows backup script to archive volume data to the host filesystem
- Read-only access prevents accidental modification of the database files

## Volume Definitions Solution

```yaml
volumes:
  postgres_data:
    name: lab02_postgres_data # Explicit name for easier management
  shared_data:
    name: lab02_shared_data # Explicit name for easier management
```

This configuration:
- Defines two named volumes with explicit names
- Makes volume identification easier in Docker commands
- Ensures consistent naming across different runs

## Key Learning Points

1. **Named Volumes**: Docker-managed volumes are perfect for database data that needs to persist.

2. **Bind Mounts**: Direct connections to the host filesystem enable efficient development workflows.

3. **Shared Volumes**: Multiple containers can share data through volumes, with different access levels.

4. **Read-Only Mounts**: Adding `:ro` makes volumes read-only, adding a layer of security.

5. **Backup Strategies**: Mounting volumes to backup containers enables data preservation.

6. **Explicit Naming**: Naming volumes explicitly makes management and identification easier.

## Common Questions and Answers

**Q**: When should I use named volumes versus bind mounts?  
**A**: Use named volumes for persistent application data (databases, etc.) and bind mounts for development when you need to edit files on the host.

**Q**: Do I need to create the named volumes before using docker-compose up?  
**A**: No, Docker Compose will automatically create named volumes defined in the volumes section.

**Q**: Will removing a container delete the volumes?  
**A**: No, volumes persist even when containers are removed. You need to explicitly remove volumes with `docker volume rm` or `docker-compose down -v`.

**Q**: Can I share a volume between different Docker Compose projects?  
**A**: Yes, by using external volumes that are created outside of the Docker Compose file.

**Q**: How can I see what's inside a volume?  
**A**: Mount the volume to a temporary container and explore the filesystem:
```bash
docker run --rm -it -v volume_name:/data alpine ls -la /data
``` 