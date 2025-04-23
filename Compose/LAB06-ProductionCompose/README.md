# LAB06: Production-Ready Docker Compose

This lab demonstrates how to create production-ready Docker Compose configurations that incorporate best practices for security, performance, and reliability.

## Learning Objectives

- Configure Docker Compose for production environments
- Implement resource limits and health checks
- Set up environment separation (dev/staging/prod)
- Optimize container configurations for security
- Configure restart policies and update strategies
- Implement proper logging configuration

## Prerequisites

- Docker Engine and Docker Compose v2 installed
- Familiarity with basic Docker Compose concepts
- Completed previous labs or equivalent knowledge

## Lab Structure

1. Basic Production Setup
2. Environment Separation
3. Resource Management
4. Health Checks and Reliability
5. Security Best Practices
6. Logging Configuration
7. Production Deployment Example

## Part 1: Basic Production Setup

### Project Structure

First, let's create our project structure:

```
LAB06-ProductionCompose/
├── app/
│   ├── app.py
│   ├── requirements.txt
│   └── templates/
│       └── index.html
├── docker-compose.yml
├── docker-compose.prod.yml
├── docker-compose.override.yml
└── .env.prod
```

### Instructions

1. Clone or navigate to this directory
2. Review the Docker Compose files and understand their organization
3. Build and run the application with different configurations
4. Observe the differences between development and production environments

## Part 2: Environment Separation

Docker Compose allows for easy environment separation using multiple compose files:

1. **Base configuration** (`docker-compose.yml`): Contains common configuration shared across environments
2. **Development overrides** (`docker-compose.override.yml`): Automatically applied when running `docker compose up`
3. **Production overrides** (`docker-compose.prod.yml`): Applied with explicit flag

To run in development mode:
```bash
docker compose up
```

To run in production mode:
```bash
docker compose -f docker-compose.yml -f docker-compose.prod.yml up -d
```

## Part 3: Resource Management

The production configuration includes:

- Memory limits to prevent container memory leaks
- CPU limits to ensure fair resource sharing
- Proper restart policies for automatic recovery
- Reserved resources for critical services

## Part 4: Health Checks and Reliability

Health checks ensure services are actually functioning properly, not just running:

```yaml
healthcheck:
  test: ["CMD", "curl", "-f", "http://localhost:5000/health"]
  interval: 30s
  timeout: 10s
  retries: 3
  start_period: 40s
```

## Part 5: Security Best Practices

Security considerations implemented:

- Read-only filesystem where possible
- Dropped unnecessary capabilities
- Non-root user execution
- Limited network exposure
- Defined resource limits to prevent DoS
- Proper secrets management

## Part 6: Logging Configuration

Production applications need proper logging configuration:

```yaml
logging:
  driver: "json-file"
  options:
    max-size: "10m"
    max-file: "3"
```

## Part 7: Production Deployment Example

In this example, we'll deploy a Python Flask application with Redis in a production-ready configuration.

## Cleanup

To clean up resources after completing the lab:

```bash
# If using development configuration
docker compose down -v --remove-orphans

# If using production configuration
docker compose -f docker-compose.yml -f docker-compose.prod.yml down -v --remove-orphans
```

## Best Practices Review

1. ✅ Use multiple compose files for environment separation
2. ✅ Set resource limits for all containers
3. ✅ Implement health checks for all services
4. ✅ Configure proper restart policies
5. ✅ Run containers with limited privileges
6. ✅ Use read-only filesystems where possible
7. ✅ Configure proper logging with rotation
8. ✅ Use environment files (.env) for configuration
9. ✅ Be explicit about exposed ports (internal:external)
10. ✅ Implement appropriate update strategies 