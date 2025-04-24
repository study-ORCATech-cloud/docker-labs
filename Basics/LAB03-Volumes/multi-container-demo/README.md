# Multi-Container Volume Demo

This demo shows how Docker volumes can be shared between multiple containers to facilitate communication and data sharing.

## Implementation TODOs

To complete this multi-container demo, you'll need to:

1. **Complete the API Dockerfile**:
   - Implement all the TODO sections in the api/Dockerfile
   - Set up the proper base image, working directory, and volume configurations

2. **Create Docker volumes**:
   - Set up the required volumes for data sharing
   - Understand how each volume is used in the application

3. **Implement container commands**:
   - Build and run the API service with appropriate volume mounts
   - Set up the database and web server with correct volume configurations
   - Link the containers together and test the communication

## Architecture

This setup consists of three services:

1. **Web Server (NGINX)**: Serves static content and proxies API requests
2. **API (Flask)**: Processes requests and generates content
3. **Database (PostgreSQL)**: Stores persistent data

## Volume Usage

This demo requires you to set up three different volumes:

1. **web-content**: Shared between the API and web server
   - The API writes HTML content to this volume
   - The web server reads and serves this content

2. **api-data**: Used only by the API for its internal data

3. **db-data**: Used only by the PostgreSQL database for data persistence

## Implementation Steps

Follow these steps after completing the Dockerfile TODOs:

### Step 1: Create the Necessary Volumes

```bash
# TODO: Create three named volumes for the application
# HINT: You need web-content, api-data, and db-data
docker volume create web-content
docker volume create api-data
docker volume create db-data
```

### Step 2: Build the API Image

```bash
# TODO: Navigate to the API directory and build the image
cd api
docker build -t multi-demo-api:1.0 .
```

### Step 3: Start the PostgreSQL Database

```bash
# TODO: Run a PostgreSQL container with a named volume
# HINT: Mount db-data to /var/lib/postgresql/data in the container
docker run -d \
  --name multi-demo-db \
  -v db-data:/var/lib/postgresql/data \
  -e POSTGRES_PASSWORD=password \
  -e POSTGRES_USER=postgres \
  -e POSTGRES_DB=volumedb \
  postgres:13-alpine
```

### Step 4: Start the API Service

```bash
# TODO: Run the API container with two volume mounts:
# 1. api-data for internal data
# 2. web-content for sharing HTML with the web server
# HINT: Also link it to the database container
docker run -d \
  --name multi-demo-api \
  -v api-data:/app/data \
  -v web-content:/app/web-output \
  -e OUTPUT_DIR=/app/web-output \
  --link multi-demo-db:db \
  multi-demo-api:1.0
```

### Step 5: Start the NGINX Web Server

```bash
# TODO: Run NGINX with the web-content volume mounted to serve the API's generated HTML
# Also bind-mount the nginx.conf file for configuration
docker run -d \
  --name multi-demo-web \
  -p 8080:80 \
  -v web-content:/usr/share/nginx/html \
  -v $(pwd)/nginx/nginx.conf:/etc/nginx/conf.d/default.conf \
  --link multi-demo-api:api \
  nginx:alpine
```

## Testing the Application

Access the web interface:
```
http://localhost:8080
```

Add a new message:
```bash
curl -X POST -H "Content-Type: application/json" \
  -d '{"content": "Hello from Docker volumes!"}' \
  http://localhost:8080/api/message
```

Get all messages via API:
```bash
curl http://localhost:8080/api/messages
```

View the web interface again to see updates:
```
http://localhost:8080
```

## Demonstrating Volume Sharing

To verify that volume sharing is working correctly:

1. Add a message using the API endpoint
2. Check that the web interface shows the message (the web server reads from the shared volume)
3. Look at the volume locations on your host:
   ```bash
   docker volume inspect web-content
   ```

## Extension Tasks

After completing the basic demo, try these improvements:

1. Add a second API instance that shares the same volumes
2. Create a docker-compose.yml file to manage all containers and volumes
3. Implement a backup strategy for the database volume

## Clean Up

```bash
docker stop multi-demo-web multi-demo-api multi-demo-db
docker rm multi-demo-web multi-demo-api multi-demo-db
docker volume rm web-content api-data db-data
``` 