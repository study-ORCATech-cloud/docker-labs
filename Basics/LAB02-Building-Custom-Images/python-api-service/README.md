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

## Implementation TODOs

To complete this project, you need to:

1. **Implement the multi-stage Dockerfile**:
   - Complete all the TODO sections in the `Dockerfile`
   - Create a proper build stage for dependencies
   - Implement a secure final stage with non-root user
   - Add necessary environment variables
   - Configure healthchecks

2. **Enhance the Flask application**:
   - Implement the debug mode feature based on environment variable
   - Add a new security feature as specified in the TODO comment

## API Endpoints

- `/health` - Health check endpoint
- `/api/data` - Protected endpoint requiring API key
- `/api/echo` - Echo endpoint that returns posted JSON data

## Docker Commands

After implementing the TODOs, build and run the service:

```bash
# Build the image
docker build -t python-api-service:1.0 .

# Run the container with environment variables
docker run -d -p 8000:8000 \
  -e API_KEY="demo-key" \
  -e LOG_LEVEL="info" \
  -e DEBUG_MODE="false" \
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

## Expected Multi-stage Dockerfile Structure

Your completed Dockerfile should implement:

1. **Build stage**:
   - Proper base image
   - Working directory setup
   - Dependencies preparation (using pip wheel)

2. **Final stage**:
   - Smaller base image
   - Non-root user creation
   - Working directory setup
   - Copying and installing dependencies from build stage
   - Application code copying
   - Environment variable configuration
   - User switching
   - Port exposure
   - Healthcheck
   - Run command

## Docker Best Practices to Implement

1. **Security**:
   - Use non-root user
   - Specify exact package versions
   - Minimize image layers and size

2. **Performance**:
   - Optimize layer caching
   - Use multi-stage builds
   - Minimize image size

3. **Maintainability**:
   - Clear documentation
   - Environment variable configuration
   - Health checks for monitoring

## Extension Tasks

After completing the basic TODOs, try these additional improvements:

1. Implement rate limiting for all API endpoints
2. Add additional environment variables to configure timeouts or other behavior
3. Implement a proper logging to a volume mount
4. Create a docker-compose.yml to run this service with a database 