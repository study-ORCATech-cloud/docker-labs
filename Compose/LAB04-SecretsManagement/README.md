# LAB04: Secrets Management with Docker Compose

This lab focuses on securely managing sensitive information in your Docker Compose applications using Docker secrets and other secure alternatives.

## Learning Objectives

- Understand different methods for handling secrets in Docker Compose
- Implement Docker native secrets in Swarm mode
- Create secure alternatives for Docker Compose standalone mode
- Learn best practices for storing sensitive information
- Prevent secrets leakage in logs, environment variables, and images
- Implement secrets rotation strategies

## Prerequisites

- Docker Engine installed
- Docker Compose v2 installed
- Basic understanding of Docker concepts
- Completion of previous labs recommended, especially LAB03-EnvironmentConfig

## Secrets Management Concepts

Sensitive information like passwords, API keys, and certificates require careful handling:

1. **Docker Secrets**: Native Docker mechanism for securely providing sensitive data to containers
2. **File-based secrets**: Using external files referenced in Docker Compose
3. **Environment variable files**: Using .env files with restricted permissions
4. **External secrets managers**: Integrating with dedicated tools like HashiCorp Vault
5. **Runtime-only secrets**: Providing secrets during container startup without persisting them

## Lab Exercises

### Exercise 1: Understanding Secrets Management Challenges

This exercise demonstrates common pitfalls in handling sensitive information and why proper secrets management matters.

1. Examine insecure ways secrets are commonly stored
2. Understand the risks and vulnerabilities
3. Learn detection methods for secrets exposure

### Exercise 2: Using File-Based Secrets

Create a secure application that loads sensitive information from external files.

1. Set up a web application with secrets stored as files
2. Mount secrets into the container
3. Configure proper permissions and security

### Exercise 3: External Secret Management Tools

Learn to use external secrets management tools that work with Docker Compose.

1. Set up a simple secrets manager container
2. Configure services to retrieve secrets at runtime
3. Implement secret rotation and management
4. Access secrets securely from applications

### Exercise 4: Creating Secure Alternatives for Compose

When external secrets managers are not an option, implement secure alternatives for Docker Compose standalone mode.

1. Implement a secrets management utility
2. Use environment variables securely
3. Keep secrets out of Docker images and source control
4. Set up a complete web application with secure secrets handling

## Files Included

- `docker-compose.yml` - Base configuration for all exercises
- `/exercise1` - Examples of insecure secrets handling
- `/exercise2` - File-based secrets implementation
- `/exercise3` - External secrets management implementation with Redis
- `/exercise4` - Secure Compose alternatives

## Project Structure

```
LAB04-SecretsManagement/
├── exercise1/
│   ├── Dockerfile
│   ├── app.py
│   └── docker-compose.yml
├── exercise2/
│   ├── Dockerfile
│   ├── app.py
│   ├── docker-compose.yml
│   └── secrets/
│       ├── db_password.txt
│       └── api_key.txt
├── exercise3/
│   ├── Dockerfile
│   ├── app.py
│   ├── docker-compose.yml
│   ├── init-secrets.sh
│   └── secrets/
│       └── api_key.txt
├── exercise4/
│   ├── Dockerfile
│   ├── app.py
│   ├── docker-compose.yml
│   ├── secrets-manager.py
│   └── templates/
│       └── index.html
├── docker-compose.yml
└── README.md
```

## Lab Steps

### Step 1: Common Secrets Management Mistakes

Let's first explore Exercise 1 to understand the problems with insecure secrets handling:

```bash
cd exercise1
docker compose up --build
```

This starts a container that demonstrates common mistakes:
- Hardcoded credentials in source code
- Secrets in environment variables
- Secrets in Docker image layers
- Exposed secrets in logs

Access the web app at http://localhost:8001 to see how these secrets are exposed.

### Step 2: File-Based Secrets

Move to Exercise 2 to implement file-based secrets:

```bash
cd ../exercise2
docker compose up --build
```

This application:
- Loads database credentials and API keys from mounted files
- Uses appropriate file permissions
- Keeps secrets out of environment variables and logs

Access the web app at http://localhost:8002 to see the secure implementation.

### Step 3: External Secret Management

For Exercise 3, we'll use a lightweight secrets management approach with Redis:

```bash
cd ../exercise3
docker compose up --build
```

Once the containers are running, initialize the secrets:

```bash
# Create the api_key.txt file in the secrets directory first
echo "swarm_api_key_t0ps3cr3t" > secrets/api_key.txt

# Set the API_KEY environment variable and run the init script
export API_KEY=$(cat secrets/api_key.txt)
./init-secrets.sh
```

This will:
1. Start a Redis instance as a secure secrets store
2. Run a secrets management API service
3. Deploy an application that retrieves secrets securely at runtime

Access the web app at http://localhost:8003 to explore this implementation.

### Step 4: Secure Alternatives for Docker Compose

Finally, let's implement a secure solution for standard Compose mode:

```bash
cd ../exercise4
docker compose up --build
```

This application demonstrates:
- A custom secrets manager utility
- Runtime-only secrets injection
- Secure handling of sensitive information
- Complete separation of secrets from configuration

Access the web app at http://localhost:8004 to see our most comprehensive implementation.

## Commands Reference

```bash
# Create a secret file with proper permissions
echo "my_secure_password" > secret.txt && chmod 600 secret.txt

# List all running containers including the secrets manager
docker compose ps

# Retrieve a secret from the Redis secrets store (Exercise 3)
docker compose exec secrets-api redis-cli -h secrets-store get db_password

# Run a container with secrets mounted
docker compose up -d app

# View environment variables without exposing secrets
docker compose exec app env | grep -v PASSWORD
```

## Best Practices

- Never hardcode sensitive values in source code or Dockerfiles
- Don't store unencrypted secrets in source control
- Use Docker secrets when in Swarm mode
- For standalone Compose, use file-based secrets with proper permissions
- Consider external secret management solutions for production
- Implement the principle of least privilege
- Rotate secrets regularly
- Monitor for exposed secrets in logs and environment variables

## Security Considerations

- **File permissions**: Secret files should have restricted permissions (0400 or 0600)
- **User context**: Run containers as non-root users
- **Ephemeral secrets**: Clear secrets from memory when no longer needed
- **Layered security**: Don't rely on a single security measure
- **Auditing**: Regularly audit your applications for secrets exposure
- **Encryption**: Use encryption for secrets at rest and in transit

## Cleanup

When you're completely finished with all exercises, you can clean up all resources with:

```bash
# For all exercises
cd ../exercise1
docker compose down
cd ../exercise2
docker compose down
cd ../exercise3
docker compose down
cd ../exercise4
docker compose down

# Remove all containers that might still be running
docker ps -a -q --filter "name=secrets" | xargs -r docker rm -f

# Remove volumes if created
docker volume prune -f

# Verify all containers are removed
docker ps -a
```

## Troubleshooting

- **Permission denied**: Check file permissions on secret files
- **Secret not found**: Verify the secret exists in the store or file path is correct
- **Cannot access secret**: Ensure the container has proper access
- **Redis connection refused**: Check if the secrets-store container is running

## Next Steps

After completing this lab, you'll be ready to move on to LAB05-ScalingServices to learn about scaling Docker Compose applications. 