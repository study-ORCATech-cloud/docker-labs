# LAB08: Dockerfile Best Practices - Solutions

This document provides solutions to the exercises in LAB08. Only consult these solutions after attempting to solve the problems yourself.

## Task 2: Base Image Selection

### Comparing Base Images

| Base Image | Image Size | Startup Time | Security Concerns | Use Case |
|------------|------------|--------------|-------------------|----------|
| `ubuntu:20.04` | ~73MB | Slower | Larger attack surface | Full OS features needed |
| `debian:buster-slim` | ~27MB | Medium | Medium attack surface | Good balance of features and size |
| `alpine:3.15` | ~5MB | Fast | Smallest attack surface, but musl libc compatibility issues | Minimal images, simple applications |
| `distroless/base` | ~20MB | Fast | Minimal attack surface, no shell access | Production, security-focused applications |

### Building and Testing Base Images

```bash
# Build each example
docker build -t base-ubuntu -f Dockerfile.ubuntu .
docker build -t base-debian -f Dockerfile.debian .
docker build -t base-alpine -f Dockerfile.alpine .
docker build -t base-distroless -f Dockerfile.distroless .

# Check image sizes
docker images | grep base-

# Run simple benchmark (startup time)
time docker run --rm base-ubuntu /bin/echo "Hello from Ubuntu"
time docker run --rm base-debian /bin/echo "Hello from Debian"
time docker run --rm base-alpine /bin/echo "Hello from Alpine"
time docker run --rm base-distroless /bin/echo "Hello from Distroless"
```

### Base Image Recommendation

1. **Alpine Linux (`alpine:3.15`)**: 
   - **Best for**: Small utilities, simple applications, where image size is critical
   - **When to avoid**: Applications with complex dependencies or glibc requirements

2. **Slim Debian (`debian:buster-slim`)**: 
   - **Best for**: Most applications that need glibc compatibility
   - **When to avoid**: Extremely size-constrained environments

3. **Distroless (`distroless/base`)**: 
   - **Best for**: Production deployments of compiled applications
   - **When to avoid**: Debugging scenarios or when shell access is needed

4. **Ubuntu (`ubuntu:20.04`)**: 
   - **Best for**: Complex applications needing specific Ubuntu packages
   - **When to avoid**: Simple applications or where image size is a concern

## Task 3: Multi-stage Builds

### Comparing Single-stage and Multi-stage Builds

Single-stage example image size: ~350MB
Multi-stage example image size: ~85MB

### Refactoring Single-stage to Multi-stage (Node.js Example)

```dockerfile
# Stage 1: Build stage
FROM node:14 AS build

WORKDIR /app

# Copy package files and install dependencies
COPY package*.json ./
RUN npm install

# Copy source code and build
COPY . .
RUN npm run build

# Stage 2: Production stage
FROM node:14-alpine

WORKDIR /app

# Copy only production dependencies
COPY --from=build /app/package*.json ./
RUN npm install --only=production

# Copy built application from build stage
COPY --from=build /app/dist ./dist

# Set user to non-root
USER node

# Start the application
CMD ["node", "dist/index.js"]
```

### Further Optimizing Multi-stage Builds

```dockerfile
# Stage 1: Build stage
FROM node:14-alpine AS build

WORKDIR /app

# Copy package files and install dependencies
COPY package*.json ./
RUN npm ci

# Copy source code and build
COPY . .
RUN npm run build

# Stage 2: Production stage
FROM node:14-alpine AS production

# Set working directory
WORKDIR /app

# Install production dependencies
COPY package*.json ./
RUN npm ci --only=production

# Copy built assets from build stage
COPY --from=build /app/dist ./dist

# Create non-root user and set permissions
RUN addgroup -g 1001 -S nodejs && \
    adduser -S nodejs -u 1001 && \
    chown -R nodejs:nodejs /app

# Switch to non-root user
USER nodejs

# Expose port and define command
EXPOSE 3000
CMD ["node", "dist/index.js"]
```

## Task 4: Layer Optimization

### Analyzing Layers

Command to view layer sizes:
```bash
docker history layer-unoptimized
```

### Refactored Dockerfile with Optimized Layers

```dockerfile
# Original problematic Dockerfile
FROM ubuntu:20.04

RUN apt-get update
RUN apt-get install -y python3
RUN apt-get install -y python3-pip
RUN apt-get install -y curl
RUN pip3 install flask
RUN pip3 install requests
RUN pip3 install redis
RUN mkdir -p /app/data
RUN mkdir -p /app/logs
RUN mkdir -p /app/config
COPY . /app
RUN rm -rf /app/temp
RUN rm -rf /var/lib/apt/lists/*

WORKDIR /app
CMD ["python3", "app.py"]
```

```dockerfile
# Optimized Dockerfile
FROM ubuntu:20.04

WORKDIR /app

# Combine package installation and cleanup in one layer
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        python3 \
        python3-pip \
        curl && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Install all Python dependencies in one layer
COPY requirements.txt .
RUN pip3 install --no-cache-dir -r requirements.txt

# Create directory structure in one layer
RUN mkdir -p data logs config

# Copy application code
COPY . .

# Clean up in the same layer as the copy
RUN rm -rf temp

# Set command
CMD ["python3", "app.py"]
```

### Layer Optimization Best Practices

1. **Combine related commands** using `&&` to reduce layers
2. **Use `--no-install-recommends`** when installing packages
3. **Clean up in the same layer** where files are created
4. **Use `.dockerignore`** to avoid copying unnecessary files
5. **Order instructions** from least to most frequently changing

## Task 5: Caching Dependencies

### Original Dockerfile with Poor Caching

```dockerfile
FROM node:14

WORKDIR /app

# Copy everything at once
COPY . .

# Install dependencies after copying everything
RUN npm install

# Build the application
RUN npm run build

# Expose port and define command
EXPOSE 3000
CMD ["npm", "start"]
```

### Refactored Dockerfile with Improved Caching

```dockerfile
FROM node:14

WORKDIR /app

# Copy dependency files first
COPY package.json package-lock.json ./

# Install dependencies
RUN npm ci

# Copy the rest of the application code
COPY . .

# Build the application
RUN npm run build

# Expose port and define command
EXPOSE 3000
CMD ["npm", "start"]
```

### Caching Best Practices

1. **Order instructions from least to most frequently changing**
2. **Copy dependency files separately** before copying application code
3. **Use lock files** (`package-lock.json`, `yarn.lock`, etc.) for deterministic builds
4. **Use `npm ci` instead of `npm install`** for more reliable builds
5. **Use `.dockerignore` to exclude** `node_modules` and other build artifacts

## Task 6: Security Best Practices

### Original Dockerfile with Security Issues

```dockerfile
FROM ubuntu:latest

# Install dependencies
RUN apt-get update && \
    apt-get install -y nginx python3 curl

# Copy application files
COPY . /app/

# Set up web server
RUN chmod 777 /app
RUN echo "daemon off;" >> /etc/nginx/nginx.conf

# Add credentials for service access
ENV DB_PASSWORD="super_secret_password"
ENV API_KEY="1234567890abcdef"

# Install dependencies from the web
RUN curl -s https://example.com/install.sh | bash

# Open ports
EXPOSE 80 22 3306

# Start as root
CMD ["nginx", "-c", "/etc/nginx/nginx.conf"]
```

### Refactored Secure Dockerfile

```dockerfile
# Use specific version tag
FROM ubuntu:20.04

# Create non-root user
RUN groupadd -r webuser && useradd -r -g webuser webuser

# Install dependencies with version pinning
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        nginx=1.18.* \
        python3=3.8.* \
        curl=7.68.* && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Set up web server
RUN echo "daemon off;" >> /etc/nginx/nginx.conf && \
    chown -R webuser:webuser /var/lib/nginx

# Create app directory with proper permissions
WORKDIR /app
COPY --chown=webuser:webuser . .
RUN chmod -R 755 /app

# Verify integrity of external scripts instead of piping to bash
COPY install_verification.sh .
RUN chmod +x install_verification.sh && ./install_verification.sh

# Use secrets management instead of environment variables
# For local development, use --secret flag with docker build
# For production, use Docker Swarm secrets or Kubernetes secrets

# Only expose necessary ports
EXPOSE 80

# Drop privileges and run as non-root
USER webuser

# Use CMD as an array
CMD ["nginx", "-c", "/etc/nginx/nginx.conf"]
```

### Security Checklist

1. **Use specific version tags** for base images
2. **Run containers as non-root users**
3. **Remove unnecessary packages** and tools
4. **Don't store secrets in Dockerfiles or images**
5. **Verify integrity of downloaded files**
6. **Minimize exposed ports**
7. **Use multi-stage builds** to reduce attack surface
8. **Scan images for vulnerabilities**
9. **Set appropriate file permissions**
10. **Keep base images updated**

## Task 7: Environment-specific Dockerfiles

### Improved Strategy for Environment Management

Using build args and multi-stage builds:

```dockerfile
# Base stage with common dependencies
FROM node:14-alpine AS base

WORKDIR /app

COPY package*.json ./
RUN npm ci

COPY . .

# Development stage
FROM base AS development

ENV NODE_ENV=development
RUN npm install --only=development

CMD ["npm", "run", "dev"]

# Testing stage
FROM base AS testing

ENV NODE_ENV=test
RUN npm install --only=development

CMD ["npm", "test"]

# Production stage
FROM base AS production

ENV NODE_ENV=production

# Additional production optimizations
RUN npm run build && \
    npm prune --production && \
    npm cache clean --force

USER node

CMD ["npm", "start"]
```

### Building for Different Environments

```bash
# Build for development
docker build --target development -t myapp:dev .

# Build for testing
docker build --target testing -t myapp:test .

# Build for production
docker build --target production -t myapp:prod .
```

## Task 8: CI/CD Considerations

### Improved CI/CD Configuration (GitHub Actions Example)

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

      - name: Cache Docker layers
        uses: actions/cache@v2
        with:
          path: /tmp/.buildx-cache
          key: ${{ runner.os }}-buildx-${{ github.sha }}
          restore-keys: |
            ${{ runner.os }}-buildx-

      - name: Build and export
        uses: docker/build-push-action@v2
        with:
          context: .
          push: false
          load: true
          tags: myapp:test
          cache-from: type=local,src=/tmp/.buildx-cache
          cache-to: type=local,dest=/tmp/.buildx-cache-new

      - name: Run tests
        run: docker run --rm myapp:test npm test

      - name: Login to DockerHub
        if: github.event_name != 'pull_request'
        uses: docker/login-action@v1
        with:
          username: ${{ secrets.DOCKERHUB_USERNAME }}
          password: ${{ secrets.DOCKERHUB_TOKEN }}

      - name: Build and push
        if: github.event_name != 'pull_request'
        uses: docker/build-push-action@v2
        with:
          context: .
          push: true
          tags: myuser/myapp:latest
          target: production
          cache-from: type=local,src=/tmp/.buildx-cache
          cache-to: type=local,dest=/tmp/.buildx-cache-new

      # Move cache
      - name: Move cache
        run: |
          rm -rf /tmp/.buildx-cache
          mv /tmp/.buildx-cache-new /tmp/.buildx-cache
```

### CI/CD Best Practices

1. **Use Docker BuildKit** for faster builds
2. **Implement layer caching** between CI runs
3. **Run tests in a container** to ensure consistency
4. **Use multi-stage builds** with separate targets for test and production
5. **Leverage build arguments** for environment-specific configurations
6. **Use specific tags** and consider adding git SHA for traceability
7. **Implement security scanning** in your pipeline
8. **Use a registry proxy/cache** for frequently used base images
9. **Optimize for parallel builds** when working with multiple services
10. **Consider using Docker Buildx** for multi-platform builds

## Task 9: Real-world Application Refactoring

### Original Problematic Dockerfile

```dockerfile
FROM ubuntu:latest

RUN apt-get update
RUN apt-get install -y python3 python3-pip nginx supervisor
RUN pip3 install django gunicorn psycopg2-binary redis pillow
RUN pip3 install pytest pytest-django coverage

COPY . /app/
WORKDIR /app

RUN python3 manage.py collectstatic --noinput
RUN chmod +x /app/entrypoint.sh

EXPOSE 8000

CMD ["/app/entrypoint.sh"]
```

### Optimized Dockerfile

```dockerfile
# Stage 1: Build stage
FROM python:3.9-slim-buster AS builder

WORKDIR /app

# Install build dependencies
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        gcc \
        python3-dev \
        libpq-dev && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirements*.txt ./
RUN pip wheel --no-cache-dir --wheel-dir /app/wheels -r requirements.txt

# Stage 2: Test stage
FROM python:3.9-slim-buster AS test

WORKDIR /app

# Copy wheels from builder stage
COPY --from=builder /app/wheels /app/wheels
COPY requirements*.txt ./

# Install dependencies
RUN pip install --no-cache-dir --no-index --find-links=/app/wheels -r requirements.txt
RUN pip install --no-cache-dir pytest pytest-django coverage

# Copy application code
COPY . .

# Run tests
RUN pytest

# Stage 3: Production stage
FROM python:3.9-slim-buster AS production

WORKDIR /app

# Install runtime dependencies
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        nginx \
        supervisor && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Copy wheels from builder stage and install dependencies
COPY --from=builder /app/wheels /app/wheels
COPY requirements.txt ./
RUN pip install --no-cache-dir --no-index --find-links=/app/wheels -r requirements.txt

# Copy application code
COPY . .

# Set up Nginx and Supervisor
COPY docker/nginx.conf /etc/nginx/sites-available/default
COPY docker/supervisor.conf /etc/supervisor/conf.d/

# Collect static files
RUN python manage.py collectstatic --noinput

# Create non-root user
RUN useradd -ms /bin/bash appuser && \
    chown -R appuser:appuser /app

# Set permissions
RUN chmod +x /app/entrypoint.sh

# Change to non-root user
USER appuser

# Expose application port
EXPOSE 8000

# Start services
CMD ["/app/entrypoint.sh"]
```

### Improvements Made

1. **Multi-stage build** to separate build, test, and runtime environments
2. **Specific Python base image** instead of Ubuntu
3. **Optimized dependency installation** with wheels
4. **Combined RUN instructions** to reduce layers
5. **Proper dependency caching** by copying requirements files first
6. **Non-root user** for security
7. **Separate build dependencies** from runtime dependencies
8. **Added automated testing** stage
9. **Organized configuration files** in a docker directory
10. **Reduced image size** by ~65%

## Task 10: Dockerfile Style Guide

### Dockerfile Style Guide Template

```markdown
# Dockerfile Style Guide

## General Principles

- Keep images small, secure, and maintainable
- Optimize for build speed and caching
- Follow the principle of least privilege
- Document non-obvious decisions with comments

## Formatting

- Use 4-space indentation for readability
- Group related instructions together
- Add blank lines between logical sections
- Keep line length reasonable (≤80 characters when possible)

## Structure

### Standard Order of Instructions

1. `FROM` - Start with the base image
2. `LABEL` - Add metadata (maintainer, version, etc.)
3. `ARG` - Define build-time variables (before ENV)
4. `ENV` - Set environment variables
5. `WORKDIR` - Set working directory
6. `RUN` - Install dependencies and set up environment
7. `COPY` - Copy application code and files
8. `RUN` - Build/compile application if needed
9. `USER` - Switch to non-root user
10. `EXPOSE` - Document ports application uses
11. `VOLUME` - Declare persistent volumes
12. `HEALTHCHECK` - Define container health check
13. `CMD` or `ENTRYPOINT` - Startup command

### Common Patterns

#### Multi-stage builds

```dockerfile
FROM builder AS build
...
FROM base AS final
COPY --from=build ...
```

#### Layer Optimization

```dockerfile
RUN command1 && \
    command2 && \
    command3
```

## Base Image Selection

- Use official images when possible
- Prefer slim or alpine variants when appropriate
- Always use specific version tags
- Consider distroless for production

## Security Best Practices

- Run as non-root user
- Use multi-stage builds to minimize attack surface
- Remove unnecessary packages and tools
- Don't store secrets in the image
- Scan images for vulnerabilities regularly
- Set appropriate file permissions

## Cache Optimization

- Order instructions from least to most frequently changing
- Copy dependency files before application code
- Use .dockerignore to exclude unnecessary files
- Leverage BuildKit cache mounts for package managers

## Documentation Requirements

- Add a comment block at the top explaining the image purpose
- Document exposed ports and volumes
- Add comments for non-obvious instructions
- Include example usage in comments

## Environment-specific Considerations

- Use build arguments for environment differences
- Consider using separate Dockerfiles for dev/test/prod
- Don't include development tools in production images
```

### Template Dockerfile Example

```dockerfile
# Purpose: Application server for MyApp
# Usage:   docker build -t myapp:1.0 .
#          docker run -p 8080:8080 myapp:1.0

# Build stage
FROM node:14-alpine AS build

WORKDIR /app

# Install dependencies
COPY package*.json ./
RUN npm ci

# Copy and build application
COPY . .
RUN npm run build

# Production stage
FROM node:14-alpine

# Metadata
LABEL maintainer="team@example.com"
LABEL version="1.0"
LABEL description="MyApp application server"

# Create app directory
WORKDIR /app

# Set environment variables
ENV NODE_ENV=production
ENV PORT=8080

# Install production dependencies
COPY package*.json ./
RUN npm ci --only=production && \
    npm cache clean --force

# Copy built application from build stage
COPY --from=build /app/dist ./dist

# Create and use non-root user
RUN addgroup -g 1001 -S nodejs && \
    adduser -S nodejs -u 1001 && \
    chown -R nodejs:nodejs /app

USER nodejs

# Document exposed ports
EXPOSE 8080

# Health check
HEALTHCHECK --interval=30s --timeout=5s --start-period=5s --retries=3 \
    CMD wget -q -O - http://localhost:8080/health || exit 1

# Start command
CMD ["node", "dist/server.js"]