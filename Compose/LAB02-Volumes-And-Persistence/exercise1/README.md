# Exercise 1: Basic Volume Persistence

This exercise demonstrates data persistence in Docker using named volumes with a PostgreSQL database.

## Overview

In this exercise, you will:
1. Implement a Docker Compose configuration with named volumes
2. Start a PostgreSQL container with a named volume
3. Verify that data is stored in the database
4. Stop and remove the container
5. Recreate the container with the same volume
6. Verify that the data persists across container restarts

## Files

- `init.sql`: SQL script that initializes the database with sample data

## Instructions

### Step 1: Configure the Docker Compose File

Before starting, add the volume configuration to the `docker-compose.yml` file:

```yaml
# TODO: Configure the postgres-db service with:
# 1. A named volume for PostgreSQL data mounted to /var/lib/postgresql/data
# 2. A bind mount for init.sql to /docker-entrypoint-initdb.d/init.sql
```

Make sure to also define the named volume in the volumes section at the bottom of the file.

### Step 2: Start the PostgreSQL Container

```bash
# Start the postgres-db service
docker-compose up -d postgres-db

# Check that the container is running
docker-compose ps
```

### Step 3: Connect to the Database and Add Data

```bash
# Connect to the PostgreSQL database
docker-compose exec postgres-db psql -U dbuser -d persistence_demo

# Inside the psql shell, you can:

# List the tables
\dt

# View the initial data
SELECT * FROM notes;

# Add a new note
INSERT INTO notes (title, content) VALUES ('My Test Note', 'This is a test note to check persistence');

# Verify the new note is added
SELECT * FROM notes;

# Exit psql
\q
```

### Step 4: Stop and Remove the Container (But Keep the Volume)

```bash
# Stop and remove the container
docker-compose stop postgres-db
docker-compose rm -f postgres-db
```

### Step 5: Verify the Named Volume Still Exists

```bash
# List all volumes
docker volume ls | grep lab02_postgres_data
```

### Step 6: Recreate the Container with the Same Volume

```bash
# Start the postgres-db service again
docker-compose up -d postgres-db
```

### Step 7: Verify Data Persistence

```bash
# Connect to the PostgreSQL database again
docker-compose exec postgres-db psql -U dbuser -d persistence_demo

# View all data including your test note
SELECT * FROM notes;

# Notice that a new timestamp entry was added automatically by the init.sql script
# This happens each time the container starts

# Exit psql
\q
```

### Step 8: Cleanup

When you're finished with this exercise, clean up the resources:

```bash
# Stop the container
docker-compose stop postgres-db

# Remove the container
docker-compose rm -f postgres-db

# If you want to remove the volume and delete all data permanently
# docker volume rm lab02_postgres_data

# Keep the volume if you plan to continue with other exercises that use it
```

## Expected Results

- The data you inserted in Step 3 should still be visible after recreating the container
- A new timestamp entry should be added each time the container is started
- This demonstrates that the data is being persisted in the named volume

## Key Learning Points

- Named volumes are managed by Docker and persist data beyond the container lifecycle
- SQL initialization scripts are only run when the volume is empty (first container creation)
- Volume persistence works transparently to the application
- Docker Compose simplifies volume management with declarative configuration 