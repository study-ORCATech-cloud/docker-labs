# LAB02: Building Docker Images - Solutions

This document contains solutions to the TODO exercises in LAB02. Use these solutions only after attempting to solve the problems yourself.

## Simple Flask App Solutions

### Dockerfile Solution

```dockerfile
# Base image for Python Flask application
FROM python:3.9-slim

# Set the working directory
WORKDIR /app

# Copy and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY app.py .

# Expose the application port
EXPOSE 5000

# Command to run the application
CMD ["python", "app.py"]
```

### App.py Hostname Endpoint Solution

Add this function to app.py:

```python
@app.route('/hostname')
def hostname():
    return jsonify({"hostname": socket.gethostname()})
```

## Python API Service Solutions

### Dockerfile Multi-stage Build Solution

```dockerfile
# Build stage
FROM python:3.9 AS builder

WORKDIR /app

# Copy only requirements first for better caching
COPY requirements.txt .
RUN pip wheel --no-cache-dir --no-deps --wheel-dir /app/wheels -r requirements.txt

# Final stage
FROM python:3.9-slim

# Create a non-root user for security
RUN useradd -m appuser

# Set working directory
WORKDIR /app

# Copy wheels from build stage and install dependencies
COPY --from=builder /app/wheels /wheels
RUN pip install --no-cache /wheels/*

# Copy application code
COPY app.py .

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    ENVIRONMENT=production

# Switch to non-root user
USER appuser

# Expose the application port
EXPOSE 8000

# Health check
HEALTHCHECK --interval=30s --timeout=3s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:8000/health || exit 1

# Command to run the application
CMD ["python", "app.py"]
```

### App.py Debug Mode Solution

Add this code after the API_KEY definition:

```python
# Debug mode configuration
DEBUG_MODE = os.environ.get('DEBUG_MODE', 'False').lower() == 'true'

if DEBUG_MODE:
    logger.setLevel(logging.DEBUG)
    logger.debug("Debug mode enabled")
```

### App.py Security Feature Solution (Rate Limiting)

First, add the imports at the top:

```python
from functools import wraps
from flask import Flask, jsonify, request, abort
import time
from collections import defaultdict
```

Then add the rate limiting implementation:

```python
# Simple rate limiting implementation
request_history = defaultdict(list)
RATE_LIMIT = 5  # Maximum requests
RATE_PERIOD = 60  # Per minute

def rate_limit(func):
    @wraps(func)
    def decorated_function(*args, **kwargs):
        client_ip = request.remote_addr
        current_time = time.time()
        
        # Remove requests older than the rate period
        request_history[client_ip] = [timestamp for timestamp in request_history[client_ip] 
                                     if current_time - timestamp < RATE_PERIOD]
        
        # Check if client has hit the rate limit
        if len(request_history[client_ip]) >= RATE_LIMIT:
            logger.warning(f"Rate limit exceeded for {client_ip}")
            return jsonify({"error": "Rate limit exceeded. Try again later."}), 429
        
        # Add the current request timestamp
        request_history[client_ip].append(current_time)
        
        return func(*args, **kwargs)
    return decorated_function

# Apply rate limiting to data endpoint
@app.route('/api/data')
@rate_limit
def get_data():
    # Existing implementation...
```

## TODO Exercise Solutions

### TODO 1: Optimize the Simple Flask App

#### Optimized Dockerfile with Alpine and Healthcheck

```dockerfile
FROM python:3.9-alpine

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY app.py .

EXPOSE 5000

HEALTHCHECK --interval=30s --timeout=3s --start-period=5s --retries=3 \
    CMD wget --no-verbose --tries=1 --spider http://localhost:5000/health || exit 1

CMD ["python", "app.py"]
```

#### Container Hostname Endpoint

```python
@app.route('/hostname')
def hostname():
    return jsonify({
        "hostname": socket.gethostname(),
        "container_id": socket.gethostname()[:12]  # First 12 chars of container ID
    })
```

### TODO 2: Secure the Python API Service

#### User Creation and Permissions

```dockerfile
# Create a dedicated user with minimal permissions
RUN addgroup --system appgroup && \
    adduser --system --ingroup appgroup --no-create-home --disabled-password appuser && \
    mkdir -p /app/logs && \
    chown -R appuser:appgroup /app

# Set working directory and permissions
WORKDIR /app
RUN chown -R appuser:appgroup /app

# Later in the Dockerfile
USER appuser
```

#### Debug Mode Environment Variable

```python
# Debug mode configuration from environment variable
DEBUG_MODE = os.environ.get('DEBUG_MODE', 'False').lower() == 'true'
app.debug = DEBUG_MODE

if DEBUG_MODE:
    logger.setLevel(logging.DEBUG)
    logger.warning("⚠️ Debug mode is enabled! This should not be used in production.")
```

### TODO 3: Multi-stage Build Benefits

Improvements from using multi-stage builds:

1. **Size reduction**: Example for simple-flask-app:
   - Without multi-stage: ~120MB
   - With multi-stage: ~60MB

2. **Security improvements**:
   - Build tools and development dependencies are not included in the final image
   - Smaller attack surface due to fewer packages
   - Ability to use distroless or minimal base images in the final stage

3. **Build performance**: Separating build dependencies allows for better caching and faster rebuilds.

### TODO 4: CI/CD Pipeline Configuration

Example GitHub Actions workflow file (.github/workflows/docker-build.yml):

```yaml
name: Docker Build and Push

on:
  push:
    branches: [ main ]
  pull_request:
    branches: [ main ]

jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - name: Checkout code
        uses: actions/checkout@v2

      - name: Set up Docker Buildx
        uses: docker/setup-buildx-action@v1

      - name: Login to DockerHub
        uses: docker/login-action@v1
        with:
          username: ${{ secrets.DOCKERHUB_USERNAME }}
          password: ${{ secrets.DOCKERHUB_TOKEN }}

      - name: Build and test simple-flask-app
        uses: docker/build-push-action@v2
        with:
          context: ./simple-flask-app
          push: false
          load: true
          tags: simple-flask-app:test
          
      - name: Test the flask application
        run: |
          docker run -d -p 5000:5000 --name flask-test simple-flask-app:test
          sleep 5
          curl http://localhost:5000/health || exit 1
          docker stop flask-test

      - name: Security scan with Trivy
        uses: aquasecurity/trivy-action@master
        with:
          image-ref: simple-flask-app:test
          format: 'table'
          exit-code: '1'
          severity: 'CRITICAL'

      - name: Build and push if successful
        uses: docker/build-push-action@v2
        with:
          context: ./simple-flask-app
          push: ${{ github.event_name != 'pull_request' }}
          tags: yourusername/simple-flask-app:latest
```

## Additional Best Practices

1. **Layer optimization**:
   ```dockerfile
   # Bad: Many separate RUN commands
   RUN apt-get update
   RUN apt-get install -y package1
   RUN apt-get install -y package2
   
   # Good: Combined into one layer
   RUN apt-get update && \
       apt-get install -y \
       package1 \
       package2 && \
       rm -rf /var/lib/apt/lists/*
   ```

2. **Non-root containers**:
   - Always run containers as non-root users in production
   - Use USER instruction to switch to non-privileged user
   - Apply principle of least privilege

3. **Minimal base images**:
   - Use Alpine or slim variants for smaller images
   - Consider distroless images for production 