# Exercise 3: Multi-environment Compose Files

This exercise demonstrates how to configure different environments using multiple Docker Compose files.

## Overview

In this exercise, you will:

1. Set up a base Docker Compose configuration
2. Configure development overrides with docker-compose.override.yml
3. Create production overrides with docker-compose.prod.yml
4. Learn how Docker Compose merges configuration files

## Files

- `Dockerfile`: Defines the container environment
- `app/`: Contains the application code
- `docker-compose.yml`: Base Docker Compose configuration (shared between environments)
- `docker-compose.override.yml`: Development-specific overrides (used by default)
- `docker-compose.prod.yml`: Production-specific overrides (must be explicitly specified)

## Instructions

### Step 1: Configure the Base Compose File

First, open the main `docker-compose.yml` file and locate the TODO section for the `multi-env-app` service. Implement the base configuration:

```yaml
# TODO: Configure basic environment (development) settings here
# HINT: Production settings will be in docker-compose.prod.yml
```

Your task is to define the environment section with a basic application name that will be used in both environments.

### Step 2: Configure the Development Overrides

Open the `docker-compose.override.yml` file and locate the TODO section for the `multi-env-app` service. Implement the development-specific overrides:

```yaml
# TODO: Add development-specific configuration overrides for multi-env-app
# HINT: Include development-specific environment variables like DEBUG=true
```

Add development-specific environment variables like:
- DEBUG mode enabled
- Development log level
- Any other development-specific settings

### Step 3: Configure the Production Overrides

Open the `docker-compose.prod.yml` file and locate the TODO section for the `multi-env-app` service. Implement the production-specific overrides:

```yaml
# TODO: Add production-specific configuration for multi-env-app
# HINT: Disable debugging, set log level, and add production-specific settings
```

Add production-specific environment variables and configuration like:
- Set APP_ENV to production
- Disable DEBUG mode
- Set stricter log level
- Add production-specific deployment settings (restart policy, etc.)

### Step 4: Start with Default Environment (Development)

When you run Docker Compose without specifying an override file, it automatically uses docker-compose.override.yml:

```bash
# Start with development configuration
docker-compose up -d multi-env-app

# Check the running container
docker-compose ps multi-env-app
```

### Step 5: Check Development Environment Settings

```bash
# View the environment variables in the container
docker-compose exec multi-env-app env | grep -E 'APP_|DEBUG|LOG_LEVEL'

# Access the application and observe development features
curl http://localhost:8083/config
```

### Step 6: Switch to Production Environment

To use the production configuration, you need to explicitly specify both the base and the production compose files:

```bash
# Stop the development container
docker-compose stop multi-env-app

# Start with production configuration
docker-compose -f docker-compose.yml -f docker-compose.prod.yml up -d multi-env-app

# Check the running container
docker-compose ps multi-env-app
```

### Step 7: Check Production Environment Settings

```bash
# View the environment variables in the container
docker-compose -f docker-compose.yml -f docker-compose.prod.yml exec multi-env-app env | grep -E 'APP_|DEBUG|LOG_LEVEL'

# Access the application and observe production features
curl http://localhost:8083/config
```

### Step 8: Understanding Configuration Merging

Docker Compose merges configuration files in the order they're specified, with later files overriding values in earlier files.

To see how the configurations are merged:

```bash
# View the merged development configuration
docker-compose config

# View the merged production configuration
docker-compose -f docker-compose.yml -f docker-compose.prod.yml config
```

### Step 9: Cleanup

When you're finished with this exercise, clean up the resources:

```bash
# Stop and remove the container
docker-compose -f docker-compose.yml -f docker-compose.prod.yml down
```

## How Docker Compose File Merging Works

1. Docker Compose always loads the base `docker-compose.yml` file
2. By default, it automatically merges `docker-compose.override.yml` if present
3. You can specify additional override files with `-f` flags
4. Configuration values are merged with later files taking precedence
5. Some settings (like environment variables) are completely replaced rather than merged

## Key Learning Points

- Use a base compose file for common configuration
- Create environment-specific override files for different environments
- Let the default override be development for easier local development
- Explicitly specify production overrides when deploying
- Docker Compose merging follows specific rules
- Use compose file version 3.4+ for the best override experience 