# Multi-Container Volume Demo

This demo shows how Docker volumes can be shared between multiple containers to facilitate communication and data sharing.

## Architecture

This setup consists of three services:

1. **Web Server (NGINX)**: Serves static content and proxies API requests
2. **API (Flask)**: Processes requests and generates content
3. **Database (PostgreSQL)**: Stores persistent data

## Volume Usage

This demo uses three different volumes:

1. **web-content**: Shared between the API and web server
   - The API writes HTML content to this volume
   - The web server reads and serves this content

2. **api-data**: Used only by the API for its internal data

3. **db-data**: Used only by the PostgreSQL database for data persistence

## How It Works

1. The API maintains internal data in the `api-data` volume
2. When new messages are added, the API generates HTML content
3. The generated HTML is written to the `web-content` volume
4. NGINX serves this content from the shared volume

## Running the Demo

Create the necessary volumes:
```bash
docker volume create web-content
docker volume create api-data
docker volume create db-data
```

Build the API image:
```bash
cd api
docker build -t multi-demo-api:1.0 .
```

Start the PostgreSQL database:
```bash
docker run -d \
  --name multi-demo-db \
  -v db-data:/var/lib/postgresql/data \
  -e POSTGRES_PASSWORD=password \
  -e POSTGRES_USER=postgres \
  -e POSTGRES_DB=volumedb \
  postgres:13-alpine
```

Start the API service:
```bash
docker run -d \
  --name multi-demo-api \
  -v api-data:/app/data \
  -v web-content:/app/web-output \
  -e OUTPUT_DIR=/app/web-output \
  --link multi-demo-db:db \
  multi-demo-api:1.0
```

Start the NGINX web server:
```bash
docker run -d \
  --name multi-demo-web \
  -p 8080:80 \
  -v web-content:/usr/share/nginx/html \
  -v $(pwd)/nginx/nginx.conf:/etc/nginx/conf.d/default.conf \
  --link multi-demo-api:api \
  nginx:alpine
```

Access the web interface:
```
http://localhost:8080
```

## Testing the App

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

View the web interface (automatically updated):
```
http://localhost:8080
```

## Volume Inspection

List all volumes:
```bash
docker volume ls
```

Inspect a shared volume:
```bash
docker volume inspect web-content
```

## Clean Up

Remove all containers:
```bash
docker stop multi-demo-web multi-demo-api multi-demo-db
docker rm multi-demo-web multi-demo-api multi-demo-db
```

Remove all volumes:
```bash
docker volume rm web-content api-data db-data
``` 