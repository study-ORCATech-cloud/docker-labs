# Exercise 4: Secrets Management

This exercise demonstrates how to manage sensitive information securely using Docker secrets.

## Overview

In this exercise, you will:

1. Configure Docker secrets in your Docker Compose files
2. Implement different secrets for development and production
3. Use secrets in your applications securely
4. Understand best practices for handling sensitive configuration

## Files

- `Dockerfile`: Defines the container environment
- `app/`: Contains the application code
- `secrets/`: Directory containing the secret files
  - `app_secret.dev.txt`: Development application secret
  - `app_secret.prod.txt`: Production application secret
  - `db_password.dev.txt`: Development database password
  - `db_password.prod.txt`: Production database password

## Instructions

### Step 1: Configure the Base Compose File

First, open the main `docker-compose.yml` file and locate the TODO sections for the `secrets-app` service and the secrets definition at the bottom. Implement the base configuration:

```yaml
# TODO: Configure environment variables for the secrets-app service
# HINT: Include APP_NAME and APP_ENV variables

# TODO: Configure the service to use an environment file
# HINT: Use env_file directive to point to ./exercise4/.env.${ENV_NAME:-dev}

# TODO: Configure secrets for the service
# HINT: Reference the app_secret and db_password secrets defined below
```

And at the bottom of the file:

```yaml
# TODO: Configure Docker secrets for the secrets-app service
# HINT: Define file-based secrets for app_secret and db_password
```

Your task is to:
1. Define the environment variables section
2. Configure the env_file directive
3. Add the secrets section referencing the secrets below
4. Define the secrets using files from the secrets directory

### Step 2: Configure the Development Overrides

Open the `docker-compose.override.yml` file and locate the TODO sections for the `secrets-app` service and the secrets definition at the bottom. Implement the development-specific overrides:

```yaml
# TODO: Add development-specific configuration for secrets-app
# HINT: Configure development mode, logging, and debugging options

# TODO: Replace the secrets for development environment
# HINT: Use the development secrets files
```

Add development-specific environment variables and configurations.

### Step 3: Configure the Production Overrides

Open the `docker-compose.prod.yml` file and locate the TODO sections for the `secrets-app` service and the secrets definition at the bottom. Implement the production-specific overrides:

```yaml
# TODO: Add production-specific configuration for secrets-app
# HINT: Disable debugging, set production mode, adjust resource limits

# TODO: Configure production-specific secrets for the service
# HINT: Use the production secrets files in ./exercise4/secrets/ directory
```

Add production-specific environment variables and configurations.

### Step 4: Start with Default Environment (Development)

```bash
# Start with development configuration
docker-compose up -d secrets-app

# Check the running container
docker-compose ps secrets-app
```

### Step 5: Verify Development Secrets

```bash
# View the secrets mounted in the container
docker-compose exec secrets-app ls -la /run/secrets/

# Check the application configuration endpoint
curl http://localhost:8084/config
```

Note: The secrets are mounted as files in the container at `/run/secrets/`.

### Step 6: Switch to Production Environment

```bash
# Stop the development container
docker-compose stop secrets-app

# Start with production configuration
docker-compose -f docker-compose.yml -f docker-compose.prod.yml up -d secrets-app

# Check the running container
docker-compose ps secrets-app
```

### Step 7: Verify Production Secrets

```bash
# View the secrets mounted in the container
docker-compose -f docker-compose.yml -f docker-compose.prod.yml exec secrets-app ls -la /run/secrets/

# Check the application configuration endpoint
curl http://localhost:8084/config
```

### Step 8: Understanding Secret Access in Applications

In your applications, secrets are accessed as files:

```python
# Example Python code to read a secret
def read_secret(secret_name):
    try:
        with open(f'/run/secrets/{secret_name}', 'r') as secret_file:
            return secret_file.read().strip()
    except IOError:
        return None

app_secret = read_secret('app_secret')
db_password = read_secret('db_password')
```

### Step 9: Cleanup

When you're finished with this exercise, clean up the resources:

```bash
# Stop and remove the container
docker-compose -f docker-compose.yml -f docker-compose.prod.yml down
```

## How Docker Secrets Work

1. Docker secrets are stored as files in the container at `/run/secrets/`
2. In Docker Compose, secrets are defined in the `secrets` section
3. Services reference secrets using the `secrets` property
4. Different environments can use different secret files
5. Applications read secrets by accessing the corresponding files

## Best Practices for Secrets Management

- Never store secrets in Docker images
- Don't hardcode secrets in application code
- Use Docker secrets or a dedicated secrets management service
- Different environments should have different secrets
- Keep production secrets separate from development secrets
- Rotate secrets regularly in production
- Limit access to production secrets

## Key Learning Points

- Docker Compose provides a simple secrets management system
- Secrets are stored as files within the container
- Applications need to read secrets from the mounted files
- Different environments need different secrets
- The secrets mechanism works with Docker Compose override files 