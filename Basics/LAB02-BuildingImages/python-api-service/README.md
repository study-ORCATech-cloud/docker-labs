# Python API Service

A more advanced Python API service that demonstrates Docker best practices for production-ready containers.

## Features

- Multi-stage build for smaller final image
- Non-root user for security
- Proper handling of environment variables
- Healthcheck implementation
- Structured logging with configurable levels
- API key authentication
- Containerized using Docker with best practices

## API Endpoints

- `/health` - Health check endpoint
- `/api/data` - Protected endpoint requiring API key
- `/api/echo` - Echo endpoint that returns posted JSON data

## Docker Commands

Build the image:
```bash
docker build -t python-api-service:1.0 .
```

Run the container with environment variables:
```bash
docker run -d -p 8000:8000 \
  -e API_KEY="demo-key" \
  -e LOG_LEVEL="info" \
  --name api-service \
  python-api-service:1.0
```

Test the application:
```bash
# Health check
curl http://localhost:8000/health

# Authenticated endpoint (will fail without key)
curl http://localhost:8000/api/data

# Authenticated endpoint (with key)
curl -H "X-API-KEY: demo-key" http://localhost:8000/api/data

# Echo endpoint
curl -X POST -H "Content-Type: application/json" \
  -d '{"message": "Hello Docker"}' \
  http://localhost:8000/api/echo
```

## Advanced Dockerfile Concepts

This example demonstrates several Docker best practices:

1. **Multi-stage builds** - Separates build dependencies from runtime dependencies
2. **Non-root user** - Improves security by not running as root
3. **Layer optimization** - Orders commands for better caching
4. **Environment variables** - Configures application behavior at runtime
5. **Healthchecks** - Allows Docker to monitor application health
6. **Minimal image size** - Uses slim base image and removes unnecessary files

## Security Best Practices

- Running as non-root user
- Not storing sensitive data in the image
- Using environment variables for configuration
- Implementing proper authentication
- Using specific image tags rather than 'latest'
- Keeping dependencies up to date with specific versions 