# LAB04: Secrets Management with Docker Compose - Solutions

This document provides reference solutions to the Docker Compose secrets management configurations in LAB04. These solutions are meant to be reviewed **after** you have attempted to implement the configurations yourself.

## Exercise 1: Insecure Secrets Handling (What NOT to Do)

This exercise demonstrates insecure practices that should be avoided. The `docker-compose.yml` file shows common mistakes:

```yaml
version: '3.8'

services:
  insecure-app:
    build: .
    container_name: secrets-insecure-standalone
    ports:
      - "8001:8000"
    # INSECURE: Secrets exposed in plain text environment variables
    environment:
      - APP_NAME=Insecure Secrets Demo
      - DB_USER=admin
      - DB_PASSWORD=insecure_password_123  # INSECURE: Plain text password
      - API_KEY=1234567890abcdef          # INSECURE: Plain text API key
      - JWT_SECRET=supersecrettoken       # INSECURE: Plain text token
      - DEBUG=true
```

The `Dockerfile` also demonstrates bad practices:

```dockerfile
FROM python:3.9-slim

WORKDIR /app

# Install dependencies
RUN pip install --no-cache-dir flask psycopg2-binary requests

# INSECURE: Hardcoded secrets in Dockerfile
ENV BACKUP_DB_PASSWORD="dockerfile_hardcoded_password"
ENV BACKUP_API_KEY="dockerfile_hardcoded_api_key"

# Secrets in Dockerfiles get stored in image layers
# You can see these with 'docker history image_name'

# Copy application code
COPY app.py /app/

# Expose the port the app runs on
EXPOSE 8000

# Command to run the application
CMD ["python", "app.py"]
```

### Security Issues in Exercise 1:

1. Plain text secrets in environment variables
2. Hardcoded credentials in Dockerfile
3. Secrets visible in image layers
4. Secrets potentially exposed in logs
5. No access control for secrets
6. No secrets rotation mechanism

## Exercise 2: File-Based Secrets Solution

This solution uses mounted files to securely manage secrets:

```yaml
version: '3.8'

services:
  file-secrets-app:
    build: .
    container_name: secrets-file-based-standalone
    ports:
      - "8002:8000"
    # Only non-sensitive configuration in environment variables
    environment:
      - APP_NAME=File-Based Secrets Demo
      - APP_ENV=production
      - DEBUG=false
    # Mount secrets as read-only files
    volumes:
      - ./secrets:/run/secrets:ro
    command: [ "python", "app.py" ]
```

### Creating the Secret Files:

```bash
# Create secrets directory with restricted permissions
mkdir -p secrets
chmod 700 secrets

# Create secret files with proper permissions
echo "secure_db_password_123" > secrets/db_password.txt
echo "api_key_for_external_service" > secrets/api_key.txt
echo "jwt_signing_secret_token" > secrets/jwt_secret.txt
chmod 600 secrets/*.txt  # Restrict permissions to owner only
```

### Reading Secrets in Application:

```python
# File-based secret reading function
def read_secret_file(file_path, default=''):
    """Safely read secret from file, with error handling"""
    try:
        if os.path.exists(file_path):
            with open(file_path, 'r') as file:
                return file.read().strip()
        else:
            logger.warning(f"Secret file not found: {file_path}")
            return default
    except Exception as e:
        logger.error(f"Error reading secret file {file_path}: {e}")
        return default

# Define secret paths
SECRETS_PATH = '/run/secrets'
DB_PASSWORD_FILE = os.path.join(SECRETS_PATH, 'db_password.txt')
API_KEY_FILE = os.path.join(SECRETS_PATH, 'api_key.txt')
JWT_SECRET_FILE = os.path.join(SECRETS_PATH, 'jwt_secret.txt')

# Read secrets
db_password = read_secret_file(DB_PASSWORD_FILE, 'db_password_not_found')
api_key = read_secret_file(API_KEY_FILE, 'api_key_not_found')
jwt_secret = read_secret_file(JWT_SECRET_FILE, 'jwt_secret_not_found')
```

### Security Improvements in Exercise 2:

1. Secrets stored in separate files with appropriate permissions
2. Files mounted as read-only in the container
3. Secrets never exposed in environment variables
4. Container runs as non-root user
5. Proper error handling for missing secrets
6. No sensitive data in logs or container inspection

## Exercise 3: Redis-Based Secrets Management Solution

This solution uses Redis as a secure secrets store with a dedicated API:

```yaml
version: '3.8'

services:
  # Redis as a secure secrets store
  secrets-store:
    image: redis:alpine
    container_name: secrets-store
    command: redis-server --requirepass "${REDIS_PASSWORD:-secretstorepwd}"
    volumes:
      - secrets-data:/data
    environment:
      - REDIS_PASSWORD=${REDIS_PASSWORD:-secretstorepwd}
    networks:
      - secrets-net
    healthcheck:
      test: [ "CMD", "redis-cli", "ping" ]
      interval: 30s
      timeout: 10s
      retries: 3

  # API to manage secrets
  secrets-api:
    build: ./secrets-api
    container_name: secrets-api
    ports:
      - "8088:8000"  # API port for managing secrets
    depends_on:
      - secrets-store
    environment:
      - REDIS_HOST=secrets-store
      - REDIS_PORT=6379
      - REDIS_PASSWORD=${REDIS_PASSWORD:-secretstorepwd}
      - API_KEY=${API_KEY:-api_key_for_secrets_manager}
    networks:
      - secrets-net

  # Main application that uses secrets
  app:
    build: .
    container_name: secrets-redis-app
    ports:
      - "8003:8000"
    depends_on:
      - secrets-api
    environment:
      # Only non-sensitive configuration here
      - APP_NAME=Redis Secrets Demo
      - APP_ENV=production
      - SECRETS_API_URL=http://secrets-api:8000
      - SECRETS_API_KEY=${API_KEY:-api_key_for_secrets_manager}
    networks:
      - secrets-net
    healthcheck:
      test: [ "CMD", "curl", "-f", "http://localhost:8000/health" ]
      interval: 30s
      timeout: 10s
      retries: 3
      start_period: 20s

networks:
  secrets-net:
    driver: bridge

volumes:
  secrets-data:
```

### Initializing the Secrets Store:

```bash
# Script to populate Redis with initial secrets
#!/bin/bash
# Create some default secrets
echo "Setting up default secrets..."

# API Key for accessing the secrets API
API_KEY="${API_KEY:-api_key_for_secrets_manager}"

# Function to create a secret
create_secret() {
    local name=$1
    local value=$2
    
    echo "Creating/updating secret: ${name}"
    curl -s -X POST \
      -H "Content-Type: application/json" \
      -H "X-API-Key: $API_KEY" \
      -d "{\"name\":\"$name\",\"value\":\"$value\"}" \
      http://localhost:8088/secrets
}

# Create default secrets
create_secret "db_password" "redis_secret_db_password_example"
create_secret "api_key" "redis_secret_api_key_example_12345"
create_secret "jwt_secret" "redis_secret_jwt_token_example_67890"
```

### Accessing Secrets from the Application:

```python
# Function to retrieve secrets from the API
def get_secret(secret_name):
    """Retrieve a secret from the secrets API service"""
    try:
        api_url = os.environ.get('SECRETS_API_URL', 'http://secrets-api:8000')
        api_key = os.environ.get('SECRETS_API_KEY', '')
        
        headers = {'X-API-Key': api_key}
        response = requests.get(f"{api_url}/secrets/{secret_name}", headers=headers)
        
        if response.status_code == 200:
            return response.json().get('value', '')
        else:
            logger.error(f"Failed to retrieve secret {secret_name}: {response.status_code}")
            return ''
    except Exception as e:
        logger.error(f"Error retrieving secret {secret_name}: {e}")
        return ''

# Get secrets from the API
db_password = get_secret('db_password')
api_key = get_secret('api_key')
jwt_secret = get_secret('jwt_secret')
```

### Security Improvements in Exercise 3:

1. Centralized secrets management with Redis
2. API layer for secret access with authentication
3. Network isolation for the secrets store
4. Ability to rotate secrets without restarting services
5. Password-protected Redis instance
6. Persistent volume for Redis data
7. Health checks for all services

## Exercise 4: Custom Secrets Manager Solution

This solution uses a dedicated secrets manager for local decryption:

```yaml
version: '3.8'

services:
  # Application with custom secrets management
  secure-app:
    build: .
    container_name: secrets-secure-app
    ports:
      - "8004:8000"
    environment:
      - APP_NAME=Secure Secrets Manager Demo
      - APP_ENV=production
      - SECRETS_DIR=/app/secrets
    volumes:
      - ./secrets:/app/secrets:ro  # Read-only mount for encrypted secrets
    networks:
      - secrets-net
    healthcheck:
      test: [ "CMD", "curl", "-f", "http://localhost:8000/health" ]
      interval: 30s
      timeout: 10s
      retries: 3
      start_period: 20s
    command: [ "python", "secrets_manager.py", "--run", "app.py" ]

networks:
  secrets-net:
    driver: bridge
```

### Custom Secrets Manager:

The secrets manager runs before the main application and decrypts secrets for use at runtime:

```python
# Key features of the secrets manager:
# 1. Loads encrypted secrets at runtime
# 2. Decrypts secrets using a master key (from environment or key file)
# 3. Exposes secrets to the application through in-memory storage
# 4. Never writes decrypted secrets to disk
# 5. Cleans up secrets when the application exits

def main():
    # Parse command line arguments
    parser = argparse.ArgumentParser(description='Secrets Manager')
    parser.add_argument('--run', help='Application to run after loading secrets')
    parser.add_argument('--init', action='store_true', help='Initialize secrets directory')
    parser.add_argument('--rotate', help='Rotate the specified secret')
    args = parser.parse_args()

    # Initialize secrets directory if requested
    if args.init:
        initialize_secrets_directory()
        return

    # Rotate a specific secret if requested
    if args.rotate:
        rotate_secret(args.rotate)
        return

    # Load and decrypt secrets
    load_secrets()

    # Run the specified application if provided
    if args.run:
        run_application(args.run)
```

### Security Improvements in Exercise 4:

1. Encrypted secrets at rest
2. Secrets loaded into memory only, never written to disk
3. Master key separation from encrypted secrets
4. Application runs with decrypted secrets in memory only
5. Support for secrets rotation
6. Custom secrets management without external dependencies
7. Cleanup of secrets when the application exits

## Best Practices Summary

1. **Never hardcode secrets** in source code, Dockerfiles, or Docker Compose files
2. **Don't use environment variables** for sensitive information when possible
3. **Keep secrets out of logs** and container inspection
4. **Use file-based secrets** with proper permissions as a minimum
5. **Consider a secrets manager** for more complex applications
6. **Encrypt secrets at rest** whenever possible
7. **Implement secrets rotation** mechanisms
8. **Follow the principle of least privilege** for accessing secrets
9. **Audit your secrets handling** regularly
10. **Use different secrets** for development, testing, and production

## Common Questions and Answers

**Q**: Why are environment variables insecure for secrets?  
**A**: Environment variables are visible through Docker inspect commands, can be accidentally logged, and are exposed to all processes in the container.

**Q**: How do I securely provide secrets in Docker Swarm mode?  
**A**: Use Docker's native secrets management with `docker secret create` and the `secrets` section in the Compose file.

**Q**: What's the easiest way to secure secrets in standalone Docker Compose?  
**A**: Use file-based secrets mounted as read-only volumes with proper file permissions.

**Q**: How can I rotate secrets without downtime?  
**A**: Use a dedicated secrets manager like in Exercise 3 or 4, which allows updating secrets without restarting containers.

**Q**: What should I do if my application requires environment variables for secrets?  
**A**: Use a wrapper script that loads secrets from files and sets them as environment variables just before starting the application, like in Exercise 4. 