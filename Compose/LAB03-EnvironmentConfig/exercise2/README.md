# Exercise 2: Working with .env Files

This exercise demonstrates how to use .env files to configure Docker Compose applications for different environments.

## Overview

In this exercise, you will:

1. Create environment-specific .env files 
2. Learn how to load and use environment variables from .env files
3. Switch between different environment configurations
4. Understand .env file precedence and best practices

## Files

- `Dockerfile`: Defines the Python environment for the web application
- `app/app.py`: Flask application that reads environment variables
- `app/templates/index.html`: HTML template that displays configuration
- `app/requirements.txt`: Python dependencies
- `.env.dev`: Development environment configuration
- `.env.prod`: Production environment configuration

## Instructions

### Step 1: Examine the .env Files

First, look at the different .env files:

```bash
# View the development .env file
cat exercise2/.env.dev

# View the production .env file
cat exercise2/.env.prod
```

Notice how the configurations differ between environments.

### Step 2: Start the Application with Development Environment

```bash
# Start the application using the development .env file (default)
docker-compose up -d config-app

# Check that the container is running
docker-compose ps config-app
```

### Step 3: Access the Development Application

Open your browser and navigate to http://localhost:8082

You should see the application running with development configuration:
- Light theme
- Debug mode enabled
- Development-specific features like profiler and mock data

### Step 4: Switch to Production Environment

Now, switch to the production environment configuration:

```bash
# Stop the development container
docker-compose stop config-app

# Set the environment to production
ENV_NAME=prod docker-compose up -d config-app

# Check that the container is running
docker-compose ps config-app
```

### Step 5: Access the Production Application

Open your browser and navigate to http://localhost:8082 again.

Notice the changes in the application:
- Dark theme
- Debug mode disabled
- Production-specific features like caching and rate limiting
- Different feature flags

### Step 6: Override Individual Environment Variables

You can also override specific variables from the .env files:

```bash
# Override a specific variable while using the production env file
ENV_NAME=prod THEME=light docker-compose up -d config-app
```

Check the application again to see the mixed configuration.

### Step 7: Using --env-file Flag

Docker Compose also allows specifying a custom .env file using the --env-file flag:

```bash
# Stop the container
docker-compose stop config-app

# Use the --env-file flag
docker-compose --env-file ./exercise2/.env.prod up -d config-app
```

### Step 8: Cleanup

When you're finished with this exercise, clean up the resources:

```bash
# Stop the container
docker-compose stop config-app

# Remove the container
docker-compose rm -f config-app
```

## How It Works

1. Docker Compose loads variables from:
   - `.env` file in the current directory (if present)
   - Environment variables defined in the shell
   - Custom .env file specified with --env-file flag
   - Values in the docker-compose.yml file

2. The `env_file` property in docker-compose.yml references these .env files:
   ```yaml
   env_file:
     - ./exercise2/.env.${ENV_NAME:-dev}
   ```

3. The `${ENV_NAME:-dev}` syntax uses the ENV_NAME variable if set, otherwise defaults to 'dev'

4. Inside the container, the Flask application loads these variables and configures itself accordingly

## Key Learning Points

- .env files are ideal for environment-specific configuration
- Variable substitution in docker-compose.yml with ${VAR:-default} syntax is powerful
- The ENV_NAME variable can be used to switch between different environment files
- The precedence is: command line > shell env vars > .env file > docker-compose.yml defaults
- Never store sensitive data like passwords or tokens in .env files that will be committed to source control 