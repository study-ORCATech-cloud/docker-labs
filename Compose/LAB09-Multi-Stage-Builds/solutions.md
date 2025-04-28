# LAB09: Multi-Stage Builds - Solutions

This document provides solutions and explanations for LAB09, focusing on multi-stage builds using Docker Compose.

## Part 1: Basic Multi-Stage Builds

### 1.1 Docker Compose Configuration

The `docker-compose.yml` file sets up basic multi-stage build services:

```yaml
version: '3.8'

services:
  exercise1-app:
    build:
      context: ./exercise1
      dockerfile: Dockerfile
    ports:
      - "8000:8000"
    environment:
      - APP_ENV=demo
    networks:
      - multistage-net

networks:
  multistage-net:
    driver: bridge
```

Key points:
- Building the app service from the `exercise1` directory
- Mapping port 8000 to container port 8000
- Setting `APP_ENV` to `demo`
- Connecting to the `multistage-net` network

### 1.2 Starting the Services

Start the services with:

```bash
docker-compose up -d
```

This launches the services in detached mode.

## Part 2: Advanced Dependency Management

### 2.1 Docker Compose Configuration

Configure the `exercise2` app service with build arguments:

```yaml
exercise2-app:
  build:
    context: ./exercise2
    dockerfile: Dockerfile
    args:
      - BUILD_ENV=development
  ports:
    - "8010:8000"
  environment:
    - APP_ENV=development
  networks:
    - multistage-net
```

### 2.2 Starting the Service

Start the service with:

```bash
docker-compose up -d exercise2-app
```

## Part 3: Production-Grade Python Application

### 3.1 Development Configuration

Configure the development app service:

```yaml
exercise3-app-dev:
  build:
    context: ./exercise3
    dockerfile: Dockerfile
    target: development
  ports:
    - "8020:8000"
  environment:
    - FLASK_ENV=development
    - FLASK_DEBUG=1
  volumes:
    - ./exercise3/app:/app
  networks:
    - multistage-net
```

### 3.2 Production Configuration

Configure the production app service:

```yaml
exercise3-app-prod:
  build:
    context: ./exercise3
    dockerfile: Dockerfile
    target: production
  ports:
    - "8021:8000"
  environment:
    - FLASK_ENV=production
    - FLASK_DEBUG=0
  networks:
    - multistage-net
```

### 3.3 Starting the Services

Start both development and production services with:

```bash
docker-compose up -d exercise3-app-dev exercise3-app-prod
```

## Part 4: Real-World Microservices Application

### 4.1 Web Service Configuration

Configure the web service:

```yaml
exercise4-web:
  build:
    context: ./exercise4/web-service
    dockerfile: Dockerfile
    target: development
  ports:
    - "8030:8000"
  environment:
    - API_URL=http://exercise4-api:5000
  depends_on:
    - exercise4-api
  networks:
    - multistage-net
```

### 4.2 API Service Configuration

Configure the API service:

```yaml
exercise4-api:
  build:
    context: ./exercise4/api-service
    dockerfile: Dockerfile
    target: development
  ports:
    - "8031:5000"
  environment:
    - DB_HOST=exercise4-db
    - DB_PORT=5432
    - DB_USER=postgres
    - DB_PASSWORD=postgres
    - DB_NAME=appdb
  depends_on:
    - exercise4-db
  networks:
    - multistage-net
```

### 4.3 Database Service Configuration

Configure the database service:

```yaml
exercise4-db:
  image: postgres:14-alpine
  environment:
    - POSTGRES_USER=postgres
    - POSTGRES_PASSWORD=postgres
    - POSTGRES_DB=appdb
  volumes:
    - postgres_data:/var/lib/postgresql/data
  networks:
    - multistage-net
```

### 4.4 Starting the Microservices

Start the microservices with:

```bash
docker-compose up -d exercise4-web exercise4-api exercise4-db
```

## Cleanup

- Remember to clean up resources after completing the lab to avoid unnecessary charges or resource usage.
- Use `docker-compose down` to stop and remove containers, networks, and volumes created by the `docker-compose up` command. 