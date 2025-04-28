# LAB03: Environment Configuration Management - Solutions

This document provides reference solutions to the Docker Compose environment configurations in LAB03. These solutions are meant to be reviewed **after** you have attempted to implement the configurations yourself.

## Main Docker Compose File Solution

Here's the complete `docker-compose.yml` file with all environment configurations implemented:

```yaml
version: '3.8'

services:
  # Exercise 1: Basic Environment Variables
  basic-app:
    build: ./exercise1
    container_name: env-basics
    ports:
      - "${BASIC_APP_PORT:-8081}:8080"
    environment:
      - APP_NAME=Environment Demo
      - APP_ENV=${APP_ENV:-development}
      - DEBUG=${DEBUG:-true}
      - LOG_LEVEL=${LOG_LEVEL:-debug}
    networks:
      - lab03_network

  # Exercise 2: Working with .env Files
  config-app:
    build: ./exercise2
    container_name: env-config
    ports:
      - "${CONFIG_APP_PORT:-8082}:8080"
    env_file:
      - ./exercise2/.env.${ENV_NAME:-dev}
    networks:
      - lab03_network

  # Exercise 3: Multi-environment Compose Files
  # Only basic configuration here, overrides in separate files
  multi-env-app:
    build: ./exercise3
    container_name: multi-env
    ports:
      - "${MULTI_ENV_PORT:-8083}:8080"
    environment:
      - APP_NAME=Multi Environment Demo
    networks:
      - lab03_network

  # Exercise 4: Secrets Management
  secrets-app:
    build: ./exercise4
    container_name: secrets-demo
    ports:
      - "${SECRETS_APP_PORT:-8084}:8080"
    environment:
      - APP_NAME=Secrets Management Demo
      - APP_ENV=${APP_ENV:-development}
    env_file:
      - ./exercise4/.env.${ENV_NAME:-dev}
    # Docker Compose v3 secrets support
    secrets:
      - app_secret
      - db_password
    networks:
      - lab03_network

  # Database for all exercises
  postgres:
    image: postgres:14
    container_name: lab03-postgres
    environment:
      POSTGRES_PASSWORD: ${DB_PASSWORD:-example}
      POSTGRES_USER: ${DB_USER:-dbuser}
      POSTGRES_DB: ${DB_NAME:-config_demo}
    volumes:
      - postgres_data:/var/lib/postgresql/data
    ports:
      - "${DB_PORT:-5432}:5432"
    networks:
      - lab03_network

networks:
  lab03_network:
    driver: bridge

volumes:
  postgres_data:
    name: lab03_postgres_data

# Demo secrets for Exercise 4
secrets:
  app_secret:
    file: ./exercise4/secrets/app_secret.dev.txt
  db_password:
    file: ./exercise4/secrets/db_password.dev.txt
```

## Development Override File Solution

Here's the complete `docker-compose.override.yml` file with development configurations:

```yaml
version: '3.8'

# This is the docker-compose.override.yml file that will be automatically used with docker-compose.yml
# when you run docker-compose up without specifying a file

services:
  multi-env-app:
    # Define development environment overrides here
    environment:
      - DEBUG=true
      - RELOAD=true
      - LOG_LEVEL=debug
    # Development-specific volume for code reload
    volumes:
      - ./exercise3/app:/app

  secrets-app:
    # Define development environment overrides here
    environment:
      - DEBUG=true
    # Development-specific volume for code reload
    volumes:
      - ./exercise4/app:/app
    # Development secrets configuration is in the base docker-compose.yml
```

## Production Override File Solution

Here's the complete `docker-compose.prod.yml` file with production configurations:

```yaml
version: '3.8'

# This file will only be used when explicitly specified with:
# docker-compose -f docker-compose.yml -f docker-compose.prod.yml up

services:
  multi-env-app:
    # Define production environment overrides here
    environment:
      - APP_ENV=production
      - DEBUG=false
      - LOG_LEVEL=error
      - RELOAD=false
    restart: always
    deploy:
      replicas: 2
      resources:
        limits:
          cpus: '0.5'
          memory: 256M

  secrets-app:
    # Define production environment overrides here
    environment:
      - APP_ENV=production
      - DEBUG=false
    # Production environment file
    env_file:
      - ./exercise4/.env.prod
    restart: always
    # Production-specific secrets
    secrets:
      - app_secret
      - db_password
    deploy:
      replicas: 2
      resources:
        limits:
          cpus: '0.5'
          memory: 256M

  postgres:
    # Define production environment overrides here
    environment:
      POSTGRES_PASSWORD_FILE: /run/secrets/db_password_prod
    secrets:
      - db_password_prod
    restart: always
    deploy:
      resources:
        limits:
          cpus: '1.0'
          memory: 1G

# Define production-specific secrets
secrets:
  app_secret:
    file: ./exercise4/secrets/app_secret.prod.txt
  db_password:
    file: ./exercise4/secrets/db_password.prod.txt
  db_password_prod:
    file: ./exercise4/secrets/db_password.prod.txt
```

## Exercise 1: Basic Environment Variables Solution

For the `basic-app` service in `docker-compose.yml`:

```yaml
basic-app:
  build: ./exercise1
  container_name: env-basics
  ports:
    - "${BASIC_APP_PORT:-8081}:8080"
  environment:
    - APP_NAME=Environment Demo
    - APP_ENV=${APP_ENV:-development}
    - DEBUG=${DEBUG:-true}
    - LOG_LEVEL=${LOG_LEVEL:-debug}
  networks:
    - lab03_network
```

This configuration:
- Sets a fixed APP_NAME as "Environment Demo"
- Uses variable substitution with defaults for APP_ENV, DEBUG, and LOG_LEVEL
- The port mapping also uses variable substitution with a default of 8081

## Exercise 2: .env Files Solution

For the `config-app` service in `docker-compose.yml`:

```yaml
config-app:
  build: ./exercise2
  container_name: env-config
  ports:
    - "${CONFIG_APP_PORT:-8082}:8080"
  env_file:
    - ./exercise2/.env.${ENV_NAME:-dev}
  networks:
    - lab03_network
```

This configuration:
- Uses an env_file directive to load variables from a file
- The file path includes variable substitution: `.env.${ENV_NAME:-dev}`
- When ENV_NAME is not set, it defaults to "dev", loading `.env.dev`
- When ENV_NAME is set to "prod", it will load `.env.prod`

## Exercise 3: Multi-environment Compose Files Solution

### Base Configuration (docker-compose.yml)

```yaml
multi-env-app:
  build: ./exercise3
  container_name: multi-env
  ports:
    - "${MULTI_ENV_PORT:-8083}:8080"
  environment:
    - APP_NAME=Multi Environment Demo
  networks:
    - lab03_network
```

### Development Overrides (docker-compose.override.yml)

```yaml
multi-env-app:
  environment:
    - DEBUG=true
    - RELOAD=true
    - LOG_LEVEL=debug
  volumes:
    - ./exercise3/app:/app
```

### Production Overrides (docker-compose.prod.yml)

```yaml
multi-env-app:
  environment:
    - APP_ENV=production
    - DEBUG=false
    - LOG_LEVEL=error
    - RELOAD=false
  restart: always
  deploy:
    replicas: 2
    resources:
      limits:
        cpus: '0.5'
        memory: 256M
```

## Exercise 4: Secrets Management Solution

### Base Configuration (docker-compose.yml)

```yaml
secrets-app:
  build: ./exercise4
  container_name: secrets-demo
  ports:
    - "${SECRETS_APP_PORT:-8084}:8080"
  environment:
    - APP_NAME=Secrets Management Demo
    - APP_ENV=${APP_ENV:-development}
  env_file:
    - ./exercise4/.env.${ENV_NAME:-dev}
  secrets:
    - app_secret
    - db_password
  networks:
    - lab03_network

# ...at the bottom of the file...
secrets:
  app_secret:
    file: ./exercise4/secrets/app_secret.dev.txt
  db_password:
    file: ./exercise4/secrets/db_password.dev.txt
```

### Production Overrides (docker-compose.prod.yml)

```yaml
secrets-app:
  environment:
    - APP_ENV=production
    - DEBUG=false
  env_file:
    - ./exercise4/.env.prod
  restart: always
  secrets:
    - app_secret
    - db_password
  # ...

# ...at the bottom of the file...
secrets:
  app_secret:
    file: ./exercise4/secrets/app_secret.prod.txt
  db_password:
    file: ./exercise4/secrets/db_password.prod.txt
  db_password_prod:
    file: ./exercise4/secrets/db_password.prod.txt
```

## Key Learning Points

1. **Environment Variables**: Docker Compose supports both fixed environment values and variable substitution with defaults using the `${VAR:-default}` syntax.

2. **.env Files**: Using `env_file` directive allows loading multiple environment variables from a file, simplifying environment switching.

3. **Compose File Overrides**: 
   - `docker-compose.yml` - Base configuration for all environments
   - `docker-compose.override.yml` - Automatically applied for development
   - Other override files like `docker-compose.prod.yml` must be explicitly specified

4. **Secrets Management**: 
   - Secrets are mounted as files at `/run/secrets/` in the container
   - Each service specifies which secrets it needs
   - Different environments can use different secret files
   - Applications read secrets from the mounted files

5. **Variable Precedence**:
   - Command-line variables override everything
   - Environment variables override .env file and compose file
   - .env file overrides compose file defaults

6. **Best Practices**:
   - Store common configuration in the base compose file
   - Use override files for environment-specific settings
   - Never commit sensitive information to source control
   - Use different secrets for different environments 