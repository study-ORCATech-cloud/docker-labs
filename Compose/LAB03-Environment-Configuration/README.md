# LAB03: Environment Configuration Management

This lab focuses on managing application configurations across different environments using Docker Compose.

## Learning Objectives

- Understand environment variable management in Docker Compose
- Implement multiple environment configurations
- Work with .env files and variable substitution
- Configure secrets and sensitive information
- Master Docker Compose override files for different environments

## Prerequisites

- Docker Engine installed
- Docker Compose v2 installed
- Basic understanding of Docker concepts
- Completion of previous labs recommended

## Important Instructions

This lab is designed for hands-on learning. You are expected to:
- Implement Docker Compose environment configurations yourself
- Follow the TODOs in the provided YAML files
- Test different environment configurations
- Document your findings about how Docker environment management works

## Environment Configuration Concepts

Docker Compose provides several ways to manage environment configuration:

1. **Environment variables** in docker-compose.yml
2. **.env files** for default values
3. **Environment-specific compose files** (docker-compose.override.yml)
4. **Command-line arguments** for overriding values
5. **Docker secrets** for sensitive information

## Lab Structure

This lab contains multiple Docker Compose files with TODO comments where you'll need to implement various environment configurations. The lab is structured to support all exercises:

```
LAB03-EnvironmentConfig/
│
├── docker-compose.yml         # Base configuration with TODOs
├── docker-compose.override.yml # Development overrides with TODOs
├── docker-compose.prod.yml    # Production overrides with TODOs
│
├── exercise1/                 # Basic environment variables
│   ├── README.md              # Instructions for exercise 1
│   └── ...                    # Exercise files
│
├── exercise2/                 # Working with .env files
│   ├── README.md              # Instructions for exercise 2
│   ├── dot.env.dev            # Development environment file
│   └── dot.env.prod           # Production environment file
│
├── exercise3/                 # Multi-environment setup
│   ├── README.md              # Instructions for exercise 3
│   └── ...                    # Exercise files
│
└── exercise4/                 # Secrets management 
    ├── README.md              # Instructions for exercise 4
    ├── secrets/               # Secret files directory
    └── ...                    # Exercise files
```

## Lab Exercises

### Exercise 1: Basic Environment Variables

In this exercise, you'll learn how to configure and use environment variables in a web application.

1. Configure environment variables in docker-compose.yml
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

1. Use Docker secrets for sensitive information
2. Implement different secrets for different environments
3. Follow best practices for sensitive data

## Getting Started

1. Review the main `docker-compose.yml` file and identify the TODOs
2. Read the README.md in each exercise directory for specific instructions
3. Implement the required environment configurations
4. Test each exercise following the instructions provided

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

## Cleanup

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