# LAB10: Compose Networking - Solutions

This document provides solutions and explanations for LAB10, focusing on networking using Docker Compose.

## Part 1: Basic Networking

### 1.1 Docker Compose Configuration

The `docker-compose.yml` file sets up basic networking services:

```yaml
version: '3.8'

services:
  web:
    build:
      context: ./app
      dockerfile: Dockerfile
    ports:
      - "8000:8000"
    environment:
      - REDIS_HOST=redis
      - REDIS_PORT=6379
    volumes:
      - ./app:/app
    depends_on:
      - redis

  redis:
    image: redis:6.2-alpine
    ports:
      - "6379:6379"
    volumes:
      - redis-data:/data

volumes:
  redis-data:
```

Key points:
- Building the web service from the `app` directory
- Mapping port 8000 to container port 8000
- Setting `REDIS_HOST` to `redis` and `REDIS_PORT` to `6379`
- Using a named volume for Redis data

### 1.2 Starting the Services

Start the services with:

```bash
docker-compose up -d
```

This launches the services in detached mode.

## Part 2: Multi-Tier Networking

### 2.1 Docker Compose Configuration

Configure the frontend and backend services:

```yaml
frontend:
  build:
    context: ./frontend
    dockerfile: Dockerfile
  ports:
    - "8000:8000"
  environment:
    - BACKEND_HOST=backend
    - BACKEND_PORT=8000
  networks:
    - frontend-network

backend:
  build:
    context: ./backend
    dockerfile: Dockerfile
  environment:
    - MONGO_HOST=db
    - MONGO_PORT=27017
    - MONGO_DB=networkdemo
  networks:
    - frontend-network
    - backend-network

networks:
  frontend-network:
    driver: bridge
  backend-network:
    driver: bridge
```

### 2.2 Starting the Services

Start the services with:

```bash
docker-compose up -d frontend backend
```

## Part 3: Service Discovery

### 3.1 Docker Compose Configuration

Configure the client and API services:

```yaml
client:
  build:
    context: ./client
    dockerfile: Dockerfile
  ports:
    - "8000:8000"
  environment:
    - API_HOST=api
    - API_ALIAS=api-service
    - API_PORT=8000
  networks:
    - app-network

api-1:
  build:
    context: ./api
    dockerfile: Dockerfile
  environment:
    - INSTANCE_ID=001
  networks:
    app-network:
      aliases:
        - api
        - api-service
```

### 3.2 Starting the Services

Start the services with:

```bash
docker-compose up -d client api-1
```

## Part 4: Microservices Networking

### 4.1 Docker Compose Configuration

Configure the gateway and services:

```yaml
gateway:
  build:
    context: ./gateway
    dockerfile: Dockerfile
  ports:
    - "8080:8080"
  environment:
    - USERS_SERVICE_HOST=users-service
    - USERS_SERVICE_PORT=8000
    - PRODUCTS_SERVICE_HOST=products-service
    - PRODUCTS_SERVICE_PORT=8000
  networks:
    - gateway-network

users-service:
  build:
    context: ./users-service
    dockerfile: Dockerfile
  environment:
    - MONGO_HOST=db-service
    - MONGO_PORT=27017
    - MONGO_DB=microservices
  networks:
    - gateway-network
    - service-network
    - db-network
```

### 4.2 Starting the Services

Start the services with:

```bash
docker-compose up -d gateway users-service
```

## Cleanup

- Remember to clean up resources after completing the lab to avoid unnecessary charges or resource usage.
- Use `docker-compose down` to stop and remove containers, networks, and volumes created by the `docker-compose up` command. 