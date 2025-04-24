# LAB06: Production-Ready Docker Compose - Solutions

This document provides solutions and explanations for LAB06 focusing on production-ready Docker Compose configurations.

## Basic Production Setup

### docker-compose.yml (Base Configuration)

The base configuration includes common elements shared across environments:

```yaml
version: '3.8'

services:
  web:
    build: ./app
    image: lab06-web:latest
    depends_on:
      - redis
    networks:
      - app-network
    ports:
      - "5000:5000"
    environment:
      - REDIS_HOST=redis
      - REDIS_PORT=6379

  redis:
    image: redis:6.2-alpine
    networks:
      - app-network
    volumes:
      - redis-data:/data

networks:
  app-network:
    driver: bridge

volumes:
  redis-data:
```

## Environment Separation

### docker-compose.override.yml (Development Configuration)

This file is automatically applied when running `docker compose up` without additional flags:

```yaml
version: '3.8'

services:
  web:
    build:
      context: ./app
      dockerfile: Dockerfile
    volumes:
      - ./app:/app  # For live code reloading
    ports:
      - "5000:5000"
    environment:
      - APP_ENV=development
      - FLASK_DEBUG=1
    command: python app.py  # Use Flask's built-in development server

  redis:
    ports:
      - "6379:6379"  # Expose port for development debugging
```

### docker-compose.prod.yml (Production Configuration)

Applied with the specific command: `docker compose -f docker-compose.yml -f docker-compose.prod.yml up -d`

```yaml
version: '3.8'

services:
  web:
    build:
      context: ./app
      dockerfile: Dockerfile
      args:
        - APP_ENV=production
    image: lab06-web:prod
    env_file: env.prod
    environment:
      - APP_ENV=production
    deploy:
      replicas: 2
      resources:
        limits:
          cpus: '0.50'
          memory: 256M
        reservations:
          cpus: '0.25'
          memory: 128M
      restart_policy:
        condition: any
        delay: 5s
        max_attempts: 3
        window: 120s
    healthcheck:
      test: [ "CMD", "curl", "-f", "http://localhost:5000/health" ]
      interval: 30s
      timeout: 10s
      retries: 3
      start_period: 40s
    logging:
      driver: "json-file"
      options:
        max-size: "10m"
        max-file: "3"
    command: gunicorn --workers=4 --bind=0.0.0.0:5000 app:app
    read_only: true
    security_opt:
      - no-new-privileges:true
    volumes:
      - type: volume
        source: app-logs
        target: /app/logs
        read_only: false

  redis:
    command: redis-server --appendonly yes --requirepass ${REDIS_PASSWORD}
    deploy:
      resources:
        limits:
          cpus: '0.30'
          memory: 128M
        reservations:
          cpus: '0.10'
          memory: 64M
      restart_policy:
        condition: any
        delay: 5s
        max_attempts: 3
        window: 120s
    healthcheck:
      test: [ "CMD", "redis-cli", "ping" ]
      interval: 30s
      timeout: 10s
      retries: 3
      start_period: 20s
    logging:
      driver: "json-file"
      options:
        max-size: "10m"
        max-file: "3"
    read_only: true
    tmpfs:
      - /var/run
      - /tmp

volumes:
  app-logs:
  redis-data:
```

### Environment Variables (env.prod)

Production environment variables are stored in a separate file:

```
APP_ENV=production
REDIS_HOST=redis
REDIS_PORT=6379
REDIS_PASSWORD=complex_password_here
PORT=5000
FLASK_DEBUG=0
GUNICORN_WORKERS=4
GUNICORN_THREADS=2
GUNICORN_TIMEOUT=30
GUNICORN_KEEP_ALIVE=2
```

## Key Production Considerations

### 1. Resource Management
- **Memory limits**: Prevent container memory leaks with `deploy.resources.limits.memory`
- **CPU limits**: Ensure fair resource sharing with `deploy.resources.limits.cpus`
- **Resource reservations**: Guarantee minimum resources with `deploy.resources.reservations`

### 2. Health Checks
- **Application health**: Use application `/health` endpoint to verify functionality
- **Redis health**: Use `redis-cli ping` to verify database responsiveness
- **Configurable parameters**: Adjust `interval`, `timeout`, `retries`, and `start_period` as needed

### 3. Security Hardening
- **Read-only filesystem**: Set `read_only: true` where possible
- **No new privileges**: Use `security_opt: - no-new-privileges:true`
- **Non-root user**: Run the application as a regular user (configured in Dockerfile)
- **Limited network exposure**: Only expose necessary ports
- **Secure Redis**: Use password protection in production

### 4. Logging Configuration
- **JSON file driver**: Use structured logging with `logging.driver: "json-file"`
- **Log rotation**: Prevent disk space issues with `max-size` and `max-file` options
- **Centralized logging**: Consider adding a logging service in production

### 5. High Availability
- **Restart policies**: Configure automatic recovery with `deploy.restart_policy`
- **Multiple replicas**: Scale services with `deploy.replicas`
- **Update strategies**: Configure rolling updates to prevent downtime

## Common Issues and Solutions

1. **Issue**: Redis connection fails in production
   - **Solution**: Verify Redis password is properly set in environment variables and command

2. **Issue**: Application can't write logs in production
   - **Solution**: Ensure the logs volume is properly mounted with write permissions

3. **Issue**: Container memory usage keeps growing
   - **Solution**: Set appropriate memory limits and fix potential memory leaks

4. **Issue**: Application crashes after deployment
   - **Solution**: Implement proper health checks and restart policies

5. **Issue**: File changes in production don't take effect
   - **Solution**: Remember that bind mounts are for development only; rebuild images for production

## Best Practices Summary

1. **Environment separation**: Use different compose files for different environments
2. **Resource constraints**: Always set resource limits in production
3. **Health checks**: Implement health checks for all services
4. **Proper logging**: Configure log rotation to prevent disk space issues
5. **Security first**: Use read-only filesystems and drop unnecessary privileges
6. **High availability**: Configure restart policies and update strategies
7. **Storage management**: Use named volumes for persistent data
8. **Configuration management**: Use environment files for configuration
9. **Resource efficiency**: Use multi-stage builds to reduce image sizes
10. **Monitoring readiness**: Implement proper health and metrics endpoints 