# LAB03: Working with Docker Volumes - Solutions

This document contains solutions to the TODO exercises in LAB03. Use these solutions only after attempting to solve the problems yourself.

## Volume Demo Solutions

### Dockerfile Solution

```dockerfile
# Base image
FROM python:3.9-slim

# Working directory
WORKDIR /app

# Copy and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY app.py .

# Declare volume for persistent data
VOLUME ["/app/data"]

# Expose port
EXPOSE 5000

# Run the application
CMD ["python", "app.py"]
```

### Using Named Volumes Command Solution

```bash
# Build the image
docker build -t volume-demo:1.0 .

# Create a named volume
docker volume create demo-data

# Run with named volume
docker run -d \
  --name volume-demo-app \
  -v demo-data:/app/data \
  -p 5000:5000 \
  volume-demo:1.0
```

### Using Bind Mounts Command Solution

```bash
# Build the image
docker build -t volume-demo:1.0 .

# Run with bind mount
docker run -d \
  --name volume-demo-app \
  -v "$(pwd)/data:/app/data" \
  -p 5000:5000 \
  volume-demo:1.0
```

## Multi-Container Demo Solutions

### API Dockerfile Solution

```dockerfile
FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY app.py .

# Create volume mount points
VOLUME ["/app/data", "/app/web-output"]

EXPOSE 5000

CMD ["python", "app.py"]
```

### Container Setup Commands Solution

```bash
# Create volumes
docker volume create web-content
docker volume create api-data
docker volume create db-data

# Build API image
cd api
docker build -t multi-demo-api:1.0 .

# Start database
docker run -d \
  --name multi-demo-db \
  -v db-data:/var/lib/postgresql/data \
  -e POSTGRES_PASSWORD=password \
  -e POSTGRES_USER=postgres \
  -e POSTGRES_DB=volumedb \
  postgres:13-alpine

# Start API
docker run -d \
  --name multi-demo-api \
  -v api-data:/app/data \
  -v web-content:/app/web-output \
  -e OUTPUT_DIR=/app/web-output \
  --link multi-demo-db:db \
  multi-demo-api:1.0

# Start web server
docker run -d \
  --name multi-demo-web \
  -p 8080:80 \
  -v web-content:/usr/share/nginx/html \
  -v $(pwd)/nginx/nginx.conf:/etc/nginx/conf.d/default.conf \
  --link multi-demo-api:api \
  nginx:alpine
```

## TODO Exercise Solutions

### TODO 1: Volume Backup and Restore

```bash
# Create a named volume with data
docker volume create data-to-backup
docker run -d --name data-creator -v data-to-backup:/data alpine sh -c "echo 'important data' > /data/important.txt"

# Create a backup container and save volume to a tar file
docker run --rm -v data-to-backup:/source -v $(pwd):/backup alpine tar -czf /backup/volume-backup.tar.gz -C /source .
docker rm -f data-creator

# Delete the original volume
docker volume rm data-to-backup

# Restore volume from the backup
docker volume create data-to-backup
docker run --rm -v data-to-backup:/destination -v $(pwd):/backup alpine sh -c "tar -xzf /backup/volume-backup.tar.gz -C /destination"

# Verify data is intact
docker run --rm -v data-to-backup:/data alpine cat /data/important.txt
# Should output: important data
```

### TODO 2: Development Environment with Bind Mounts

Edit the run command for development:

```bash
# Run with live code reload using bind mount
docker run -d \
  --name volume-demo-dev \
  -v "$(pwd):/app" \
  -p 5000:5000 \
  volume-demo:1.0
```

If you want to implement a file watcher, create a simple shell script:

```bash
#!/bin/bash
# watch-and-reload.sh
while true; do
  docker exec volume-demo-dev python -c "import time; time.sleep(0.1)"
  if [ $? -ne 0 ]; then
    echo "Container not running. Starting..."
    docker start volume-demo-dev
  fi
  sleep 2
done
```

### TODO 3: Database Volume Management

```bash
# Create volume for database
docker volume create db-volume

# Start a PostgreSQL container
docker run -d \
  --name postgres-db \
  -v db-volume:/var/lib/postgresql/data \
  -e POSTGRES_PASSWORD=mysecretpassword \
  -e POSTGRES_USER=postgres \
  -p 5432:5432 \
  postgres:13

# Connect and create some data
docker exec -it postgres-db psql -U postgres -c "CREATE TABLE test (id serial PRIMARY KEY, name VARCHAR);"
docker exec -it postgres-db psql -U postgres -c "INSERT INTO test (name) VALUES ('test data');"
docker exec -it postgres-db psql -U postgres -c "SELECT * FROM test;"

# Stop and remove the container (keeping the volume)
docker stop postgres-db
docker rm postgres-db

# Start a new container with the same volume
docker run -d \
  --name postgres-db-new \
  -v db-volume:/var/lib/postgresql/data \
  -e POSTGRES_PASSWORD=mysecretpassword \
  -e POSTGRES_USER=postgres \
  -p 5432:5432 \
  postgres:13

# Verify the data is still there
docker exec -it postgres-db-new psql -U postgres -c "SELECT * FROM test;"
# Should show the row with 'test data'
```

### TODO 4: Implement docker-compose.yml

Create a `docker-compose.yml` file in the multi-container-demo directory:

```yaml
version: '3'

services:
  db:
    image: postgres:13-alpine
    volumes:
      - db-data:/var/lib/postgresql/data
    environment:
      POSTGRES_PASSWORD: password
      POSTGRES_USER: postgres
      POSTGRES_DB: volumedb
    restart: unless-stopped

  api:
    build: ./api
    volumes:
      - api-data:/app/data
      - web-content:/app/web-output
    environment:
      OUTPUT_DIR: /app/web-output
    depends_on:
      - db
    restart: unless-stopped

  web:
    image: nginx:alpine
    ports:
      - "8080:80"
    volumes:
      - web-content:/usr/share/nginx/html
      - ./nginx/nginx.conf:/etc/nginx/conf.d/default.conf
    depends_on:
      - api
    restart: unless-stopped

volumes:
  db-data:
  api-data:
  web-content:
```

Run the application with:

```bash
docker-compose up -d
```

Stop and remove everything with:

```bash
docker-compose down -v
```

## Additional Best Practices

1. **Volume Naming Conventions**:
   - Use descriptive names for your volumes (e.g., app-name_data-type)
   - Consider including version or environment in the name (e.g., myapp_db_prod)

2. **Backup Strategies**:
   - Schedule regular volume backups using cron jobs
   - Store backups in multiple locations (local and remote)

3. **Volume Drivers**:
   - Use local drivers for development
   - Consider using cloud-based volume drivers in production (e.g., AWS EBS)

4. **Security Best Practices**:
   - Don't store sensitive data in bind mounts
   - Set proper permissions on volume mount points
   - Use read-only mounts when possible (e.g., configuration files)

5. **Development Workflow**:
   - Use bind mounts for code and named volumes for data in development
   - Document all volume mappings in project documentation 