# Exercise 1: Basic Environment Variables

This exercise demonstrates how to configure and use environment variables in a Docker Compose application.

## Overview

In this exercise, you will:

1. Configure environment variables in docker-compose.yml
2. Learn how Docker passes environment variables to containers
3. See how to override environment variables at runtime
4. Understand environment variable precedence in Docker Compose

## Files

- `Dockerfile`: Defines the Python environment for the web application
- `app/app.py`: Flask application that reads environment variables
- `app/templates/index.html`: HTML template that displays the configuration
- `app/requirements.txt`: Python dependencies

## Environment Variables Used

| Variable | Default | Description |
|----------|---------|-------------|
| APP_NAME | Environment Variables Demo | The name of the application |
| APP_ENV | development | The environment (development, production, etc.) |
| DEBUG | true | Enable or disable debug mode |
| LOG_LEVEL | debug | Logging level (debug, info, warning, error) |
| BASIC_APP_PORT | 8081 | Port to expose the application |

## Instructions

### Step 1: Configure Environment Variables in Docker Compose

First, open the `docker-compose.yml` file and locate the TODO section for the `basic-app` service. You need to implement the environment variables configuration.

```yaml
# TODO: Configure environment variables for the basic-app service
# HINT: Define APP_NAME, APP_ENV, DEBUG, and LOG_LEVEL variables
# HINT: Use both hardcoded values and variable substitution ${VAR:-default}
```

Your task is to define the environment section with the following:
- A fixed APP_NAME value (like "Environment Demo")
- APP_ENV using variable substitution with a default value
- DEBUG with variable substitution and a default
- LOG_LEVEL with variable substitution and a default

### Step 2: Start the Application with Default Settings

After implementing the environment section in docker-compose.yml:

```bash
# Start the application with default environment variables
docker-compose up -d basic-app

# Check that the container is running
docker-compose ps basic-app
```

### Step 3: Access the Application

Open your browser and navigate to http://localhost:8081

You should see the Environment Variables Demo with the default configuration.

### Step 4: View Environment Variables in the Container

```bash
# View all environment variables in the container
docker-compose exec basic-app env | grep -E 'APP_|DEBUG|LOG_LEVEL'

# Check the application configuration endpoint
curl http://localhost:8081/config
```

### Step 5: Override Environment Variables

You can override environment variables in several ways:

1. In the docker-compose.yml file (edit and restart)
2. Using environment variables on your system
3. Command-line overrides

Try overriding a variable at runtime:

```bash
# Override the APP_NAME and DEBUG variables
docker-compose run -e APP_NAME="Custom App Name" -e DEBUG=false basic-app python -c "import os; print(f'APP_NAME: {os.environ.get(\"APP_NAME\")}'); print(f'DEBUG: {os.environ.get(\"DEBUG\")}')"

# Start the service with a custom environment variable
docker-compose stop basic-app
APP_ENV=testing docker-compose up -d basic-app

# Check the new environment
docker-compose exec basic-app env | grep APP_ENV
```

### Step 6: Change Environment Variables Permanently

Edit the docker-compose.yml file to change environment variables permanently by modifying your implementation in the environment section.

Then restart the service:

```bash
docker-compose up -d basic-app
```

### Step 7: Cleanup

When you're finished with this exercise, clean up the resources:

```bash
# Stop the container
docker-compose stop basic-app

# Remove the container
docker-compose rm -f basic-app
```

## How Docker Compose Environment Variables Work

1. Docker Compose reads environment variables from (in order of precedence):
   - Command line overrides (`-e` flag)
   - Your shell environment
   - .env file (if present)
   - Values specified in the docker-compose.yml file

2. Environment variables are passed to the container at runtime

3. The application code reads environment variables and configures itself accordingly

## Key Learning Points

- Environment variables provide a way to configure applications without changing code
- Docker Compose makes it easy to specify and override environment variables
- Environment variables should be used for configuration that changes between environments
- Docker Compose supports variable substitution using ${VARIABLE:-default} syntax
- Variables in the compose file follow a specific precedence order 