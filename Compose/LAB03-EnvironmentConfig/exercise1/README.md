# Exercise 1: Basic Environment Variables

This exercise demonstrates how to configure and use environment variables in a Docker Compose application.

## Overview

In this exercise, you will:

1. Configure environment variables in docker-compose.yml
2. Learn how to access environment variables in Python code
3. See how to override environment variables at runtime
4. Understand environment variable precedence

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

### Step 1: Start the Application with Default Settings

```bash
# Start the application with default environment variables
docker-compose up -d basic-app

# Check that the container is running
docker-compose ps basic-app
```

### Step 2: Access the Application

Open your browser and navigate to http://localhost:8081

You should see the Environment Variables Demo with the default configuration.

### Step 3: View Environment Variables in the Container

```bash
# View all environment variables in the container
docker-compose exec basic-app env | grep -E 'APP_|DEBUG|LOG_LEVEL'

# Check the application configuration endpoint
curl http://localhost:8081/config
```

### Step 4: Override Environment Variables

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

### Step 5: Change Environment Variables Permanently

Edit the docker-compose.yml file to change environment variables permanently:

```yaml
basic-app:
  build: ./exercise1
  container_name: env-basics
  ports:
    - "${BASIC_APP_PORT:-8081}:8080"
  environment:
    - APP_NAME=Modified App Name
    - APP_ENV=${APP_ENV:-development}
    - DEBUG=${DEBUG:-true}
    - LOG_LEVEL=${LOG_LEVEL:-debug}
```

Then restart the service:

```bash
docker-compose up -d basic-app
```

### Step 6: Cleanup

When you're finished with this exercise, clean up the resources:

```bash
# Stop the container
docker-compose stop basic-app

# Remove the container
docker-compose rm -f basic-app
```

## How It Works

1. Docker Compose reads environment variables from:
   - Your shell environment
   - .env file (if present)
   - Values specified in the docker-compose.yml file
   - Command line overrides

2. Environment variables are passed to the container at runtime

3. The application code reads environment variables and configures itself accordingly

## Key Learning Points

- Environment variables provide a way to configure applications without changing code
- Docker Compose makes it easy to specify and override environment variables
- Environment variables should be used for configuration that changes between environments
- Docker Compose supports variable substitution using ${VARIABLE:-default} syntax 