# Exercise 3: Multi-environment Compose Files

This exercise demonstrates how to use multiple Docker Compose files to manage different environment configurations.

## Overview

In this exercise, you will:

1. Use a base docker-compose.yml file for common configuration
2. Learn how docker-compose.override.yml is automatically used for development
3. Create a production-specific compose file
4. Merge multiple compose files for different environments

## Files

- `Dockerfile`: Defines the Python environment for the web application
- `app/app.py`: Flask application that reads environment variables
- `app/templates/index.html`: HTML template that displays configuration
- `app/requirements.txt`: Python dependencies
- `../../docker-compose.yml`: Base configuration for all services
- `../../docker-compose.override.yml`: Development-specific overrides
- `../../docker-compose.prod.yml`: Production-specific configuration

## Instructions

### Step 1: Examine the Compose Files

First, look at the different compose files:

```bash
# View the base compose file
cat docker-compose.yml

# View the development overrides (automatically applied)
cat docker-compose.override.yml

# View the production configuration
cat docker-compose.prod.yml
```

Notice how:
- The base compose file defines common settings
- The override file adds development-specific settings
- The production file adds production-specific settings

### Step 2: Start the Application with Default (Development) Configuration

```bash
# Start the application with default configuration (base + override)
docker-compose up -d multi-env-app

# Check that the container is running
docker-compose ps multi-env-app
```

### Step 3: Access the Development Application

Open your browser and navigate to http://localhost:8083

You should see the application running with development configuration:
- Debug mode enabled
- Development-specific features
- Bind mount for real-time code changes

### Step 4: View the Compose Configuration

You can see the combined (merged) compose configuration:

```bash
# View the merged configuration
docker-compose config
```

Notice how the override settings have been automatically applied.

### Step 5: Launch with Production Configuration

Now, switch to production configuration:

```bash
# Stop the development container
docker-compose stop multi-env-app

# Use the production compose file explicitly
docker-compose -f docker-compose.yml -f docker-compose.prod.yml up -d multi-env-app

# Check that the container is running
docker-compose ps multi-env-app
```

### Step 6: Access the Production Application

Open your browser and navigate to http://localhost:8083 again.

Notice the changes in the application:
- Debug mode disabled
- Production-specific settings
- No bind mount (code changes won't be reflected)
- Replicas might be set to 2 (though this is handled by swarm/kubernetes in real production)

### Step 7: View the Production Configuration

```bash
# View the production merged configuration
docker-compose -f docker-compose.yml -f docker-compose.prod.yml config
```

Notice how the production settings override the base settings.

### Step 8: Cleanup

When you're finished with this exercise, clean up the resources:

```bash
# If you're using the development configuration
docker-compose stop multi-env-app
docker-compose rm -f multi-env-app

# If you're using the production configuration
docker-compose -f docker-compose.yml -f docker-compose.prod.yml stop multi-env-app
docker-compose -f docker-compose.yml -f docker-compose.prod.yml rm -f multi-env-app
```

## How It Works

1. Docker Compose merges multiple configuration files in the order they are specified:
   - Later files override values from earlier files
   - The base `docker-compose.yml` provides default configuration
   - `docker-compose.override.yml` is automatically applied if present
   - Other files like `docker-compose.prod.yml` must be explicitly specified

2. The merging process is intelligent:
   - Simple values are replaced
   - Lists (like ports) are replaced
   - Mappings (like environment variables) are merged

## Key Learning Points

- Using multiple compose files helps organize environment-specific settings
- The `docker-compose.override.yml` file is automatically used for development
- Production settings can be kept separate with a specific compose file
- Merging is done with the `-f` flag to specify multiple files
- The order of files matters - later files override earlier ones 