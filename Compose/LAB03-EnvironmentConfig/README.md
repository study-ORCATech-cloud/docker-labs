# LAB03: Environment Configuration Management

This lab focuses on managing application configurations across different environments using Docker Compose.

## Learning Objectives

- Understand environment variable management in Docker Compose
- Implement multiple environment configurations
- Work with .env files and variable substitution
- Configure secrets and sensitive information
- Override default environment settings

## Prerequisites

- Docker Engine installed
- Docker Compose v2 installed
- Basic understanding of Docker concepts
- Completion of previous labs recommended

## Environment Configuration Concepts

Docker Compose provides several ways to manage environment configuration:

1. **Environment variables** in docker-compose.yml
2. **.env files** for default values
3. **Environment-specific compose files** (docker-compose.override.yml)
4. **Command-line arguments** for overriding values
5. **Docker secrets** for sensitive information

## Lab Exercises

### Exercise 1: Basic Environment Variables

In this exercise, you'll learn how to configure and use environment variables in a web application.

1. Define environment variables in docker-compose.yml
2. Access environment variables in application code
3. Override environment variables at runtime

### Exercise 2: Working with .env Files

Create different environment configurations using .env files.

1. Create development and production .env files
2. Use variable substitution in docker-compose.yml
3. Switch between environments

### Exercise 3: Multi-environment Compose Files

Set up different compose files for different environments.

1. Create a base docker-compose.yml
2. Add docker-compose.override.yml for development
3. Create docker-compose.prod.yml for production
4. Learn how to merge compose files

### Exercise 4: Secrets Management

Learn how to handle sensitive configurations securely.

1. Use external secrets providers
2. Implement different secrets for different environments
3. Best practices for sensitive data

## Files Included

- `docker-compose.yml` - Base configuration for all exercises
- `docker-compose.override.yml` - Development overrides
- `docker-compose.prod.yml` - Production configuration
- `/exercise1` - Basic environment variable examples
- `/exercise2` - .env file implementations
- `/exercise3` - Multi-environment setup
- `/exercise4` - Secrets management examples

## Commands Reference

```bash
# Start with default (development) settings
docker-compose up -d

# Use a specific environment file
docker-compose --env-file .env.prod up -d

# Use a specific compose file
docker-compose -f docker-compose.yml -f docker-compose.prod.yml up -d

# View environment variables in a running container
docker-compose exec app env

# Override an environment variable at runtime
docker-compose run -e DEBUG=true app
```

## Final Cleanup

When you're completely finished with all exercises, you can clean up all resources with:

```bash
# Stop all containers defined in docker-compose.yml
docker-compose down

# Remove any volumes if created for this lab
docker volume prune -f

# Verify all containers are removed
docker-compose ps
```

## Best Practices

- Never hardcode sensitive values in Docker images or compose files
- Use .env files for development, but not for production secrets
- Consider using a secrets management service for production
- Keep environment-specific settings in separate files
- Document required environment variables

## Troubleshooting

- **Variable not found**: Verify the variable is defined in the correct place
- **Configuration precedence**: Remember that command-line overrides compose files, which override .env files
- **Multiline values**: Use YAML multiline syntax for complex environment values
- **Container not picking up changes**: Rebuild the container after changing the Dockerfile or source code