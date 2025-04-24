# LAB04-Layers: Solutions

**INSTRUCTOR NOTE: This file contains complete solutions and should NOT be shared with students. It is for instructor reference only. Students should work through the exercises themselves without seeing these solutions in advance.**

This file contains solutions to the exercises in LAB04-Layers. Students should attempt to solve the exercises on their own before referring to these solutions.

## Single-Stage Dockerfile Solution

Here's an optimized solution for the single-stage Dockerfile:

```dockerfile
FROM python:3.9-slim

# Set a working directory
WORKDIR /app

# Install system dependencies efficiently (combines multiple RUN commands)
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    gcc \
    g++ \
    build-essential && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Install Python dependencies efficiently (using requirements.txt)
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the application code 
COPY app.py .

# Create necessary directories and set permissions in one layer
RUN mkdir -p /app/data && \
    chmod 755 /app/app.py

# Set environment variables (metadata, not a layer)
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

# Install development packages in a separate environment only if needed
# For production, these packages should be omitted entirely
# For development, consider using a bind mount instead
RUN pip install --no-cache-dir \
    pytest==7.3.1 \
    black==23.3.0 \
    flake8==6.0.0

# Expose the port (metadata, not a layer)
EXPOSE 5000

# Use gunicorn for production-ready application server
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "app:app"]
```

## Multi-Stage Dockerfile Solution

Here's an optimized solution for the multi-stage Dockerfile:

```dockerfile
# Build stage with a descriptive name
FROM python:3.9-slim AS builder

# Set working directory
WORKDIR /app

# Install system dependencies efficiently in a single layer
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    gcc \
    g++ \
    build-essential && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Copy only requirements first to leverage Docker caching
COPY requirements.txt .

# Install all Python dependencies with wheels for later use
RUN pip wheel --no-cache-dir --no-deps --wheel-dir /app/wheels -r requirements.txt

# Final runtime stage
FROM python:3.9-slim AS runtime

WORKDIR /app

# Install only runtime dependencies (no build tools needed)
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    libgomp1 && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Create a non-root user for security
RUN useradd -m appuser && \
    mkdir -p /app/data && \
    chown -R appuser:appuser /app

# Copy wheels from builder stage and install dependencies
COPY --from=builder /app/wheels /wheels
RUN pip install --no-cache-dir --no-index --find-links=/wheels/ /wheels/* && \
    rm -rf /wheels

# Copy application code from builder stage (or directly if not built)
COPY app.py .

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

# Switch to non-root user for security
USER appuser

# Expose port
EXPOSE 5000

# Use gunicorn for production-ready application server
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "app:app"]
```

## Analysis Dockerfile Issues and Improvements

Here's a solution to the Dockerfile analysis exercise:

### 1. Base Image Choice
- **Issue**: Using `ubuntu:latest` as the base image.
- **Improvement**: Use `python:3.9-slim` instead, which is smaller and already includes Python.

### 2. Multiple RUN Commands
- **Issue**: Each package is installed in a separate RUN command, creating many layers.
- **Improvement**: Combine all apt-get commands into a single RUN instruction.

### 3. Dependency Installation
- **Issue**: Python packages are installed individually without pinned versions.
- **Improvement**: Use a requirements.txt file and install all dependencies with a single command.

### 4. File Copying Approach
- **Issue**: Copying everything with `COPY . /app/` happens late in the Dockerfile.
- **Improvement**: Copy only what's needed and do it earlier to leverage Docker caching.

### 5. Unnecessary Operations
- **Issue**: Installing nodejs and npm which might not be needed.
- **Improvement**: Only install what's necessary for the application.

### 6. Cleanup Approach
- **Issue**: Cleaning in a separate RUN command after files were already added.
- **Improvement**: Combine installation and cleanup in the same RUN instruction.

### 7. Command Choice
- **Issue**: Using plain Python to run a Flask app in production.
- **Improvement**: Use Gunicorn or uwsgi for production-ready WSGI server.

## Optimized Analysis Dockerfile

```dockerfile
FROM python:3.9-slim

WORKDIR /app

# Use a .dockerignore file to exclude unnecessary files
COPY requirements.txt .

# Combine all installation and cleanup in one layer
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    gcc && \
    pip install --no-cache-dir -r requirements.txt && \
    apt-get purge -y gcc && \
    apt-get autoremove -y && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Copy only the necessary application files
COPY app.py .

# Create directory if needed in the same layer as any other file operations
RUN mkdir -p /app/data

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

EXPOSE 5000

# Use gunicorn for production
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "app:app"]
```

## Key Learning Points

1. **Layer Efficiency**: Each Dockerfile instruction that modifies the filesystem creates a new layer. Multiple instructions can be combined to reduce the number of layers.

2. **Caching Strategy**: Docker uses a caching mechanism during builds. Order your instructions from least to most likely to change for optimal caching.

3. **Multi-stage Builds**: Use multi-stage builds to separate build-time dependencies from runtime dependencies, resulting in smaller final images.

4. **Layer Size Management**: 
   - The size of a layer is cumulative with all previous layers
   - Operations that create and delete files in different layers will not reduce the image size
   - Always clean up temporary files in the same RUN instruction they were created

5. **Security Best Practices**:
   - Use specific base image tags instead of 'latest'
   - Run containers as non-root users
   - Remove unnecessary tools and packages
   - Reduce the attack surface with smaller images