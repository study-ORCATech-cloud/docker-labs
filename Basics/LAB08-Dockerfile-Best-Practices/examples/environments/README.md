# Environment-specific Dockerfiles

This directory demonstrates how to create and manage Dockerfiles for different environments (development, testing, production).

## The Challenge of Multiple Environments

Different environments have different requirements:
- **Development**: Fast rebuild times, debugging tools, hot reloading
- **Testing**: Test dependencies, consistent test environment, coverage tools
- **Production**: Security, performance, minimal size, robustness

## Project Structure

- `app.py`: A Flask application that uses environment variables for configuration
- `requirements.txt`: Common Python dependencies
- `Dockerfile.development`: Dockerfile optimized for development workflow
- `Dockerfile.production`: Dockerfile optimized for production deployment

## Task: Optimize Environment-specific Dockerfiles

The goal is to improve how we handle environment-specific differences in Docker builds by:
1. Identifying what should be different per environment
2. Creating a strategy for managing these differences
3. Implementing it using best practices

## Instructions

1. Review the environment-specific Dockerfiles:
   ```bash
   cat Dockerfile.development
   cat Dockerfile.production
   ```

2. Build and run the development version:
   ```bash
   docker build -t env-demo:dev -f Dockerfile.development .
   docker run -p 8080:8080 env-demo:dev
   ```

3. Build and run the production version:
   ```bash
   docker build -t env-demo:prod -f Dockerfile.production .
   docker run -p 8080:8080 env-demo:prod
   ```

4. Compare the differences in:
   - Base images
   - Environment variables
   - User permissions
   - Runtime commands
   - Debugging capabilities

5. Improve the environment strategy by implementing:
   - A single Dockerfile with build arguments
   - Multi-stage builds with shared components
   - More appropriate environment-specific configurations
   - Better secret management

## Best Practices

- **Use build arguments** for environment-specific values
- **Create a robust default** that works in all environments
- **Keep differences minimal** between environments to reduce maintenance
- **Use multi-stage builds** to share common setup steps
- **Avoid duplicating code** in different Dockerfiles
- **Don't hardcode secrets** in any Dockerfile

## TODO

Complete the following tasks:
1. Review the provided Dockerfile examples for development and production
2. Identify the key differences between environment-specific Dockerfiles
3. Create an improved strategy for managing environment-specific differences
4. Implement a solution using build arguments and/or multi-stage builds
5. Document your approach and its advantages 