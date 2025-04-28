# LAB07: Private Registry with Nexus - Solutions

This document provides solutions and explanations for LAB07 focusing on setting up a private Docker registry using Sonatype Nexus and working with Docker images in a private registry context.

## Part 1: Nexus Repository Setup

### 1.1 Docker Compose Configuration

The `docker-compose.yaml` file sets up Nexus as a private Docker registry:

```yaml
version: '3.8'

services:
  nexus:
    image: sonatype/nexus3:latest
    container_name: nexus
    restart: unless-stopped
    ports:
      - "8081:8081"  # Nexus web UI
      - "8082:8082"  # Docker registry port
    volumes:
      - nexus-data:/nexus-data
    environment:
      - NEXUS_SECURITY_RANDOMPASSWORD=false  # Sets default admin password to 'admin123'

volumes:
  nexus-data:
    driver: local
```

Key points:
- Using the official Sonatype Nexus 3 image
- Exposing port 8081 for the Nexus UI and 8082 for the Docker registry
- Using a named volume (`nexus-data`) for persistent storage
- Setting `NEXUS_SECURITY_RANDOMPASSWORD=false` to use a predictable password

### 1.2 Starting Nexus

After creating the `docker-compose.yaml` file, you start Nexus with:

```bash
docker-compose up -d
```

This launches Nexus in detached mode with a persistent volume for data storage.

### 1.3 Creating a Docker Repository in Nexus

Through the Nexus UI (http://localhost:8081):

1. Log in with default credentials:
   - Username: `admin`
   - Password: `admin123`

2. Navigate to Administration → Repositories → Create Repository

3. Select "Docker (hosted)" and configure:
   ```
   Name: docker-hosted
   HTTP: Enabled on port 8082
   Allow anonymous pull: Enabled (for testing; disable in production)
   ```

4. Save the configuration

## Part 2: Docker Configuration for Insecure Registry

### 2.1 Docker Desktop Configuration (Windows/Mac)

Modify Docker Desktop settings to allow the insecure registry:

1. In Docker Desktop settings, edit the Docker Engine configuration to include:
   ```json
   {
     "insecure-registries": ["localhost:8082"],
     // other existing settings...
   }
   ```

2. Apply and restart Docker Desktop

### 2.2 Linux Configuration

For Linux systems, edit the daemon configuration file:

```bash
sudo nano /etc/docker/daemon.json
```

Add or modify:
```json
{
  "insecure-registries": ["localhost:8082"]
}
```

Then restart Docker: `sudo systemctl restart docker`

## Part 3: Building and Pushing Images

### 3.1 Dockerfile for Flask Application

The `Dockerfile` for our simple Flask application:

```Dockerfile
FROM python:3.12-slim

RUN useradd -m app

WORKDIR /app

COPY . .

RUN pip install --no-cache-dir -r requirements.txt

USER app

ENV PYTHONPATH=/app

ENTRYPOINT ["python3", "-u", "/app/src/main.py"]
```

Key best practices:
- Using a slim base image to minimize size
- Creating a non-root user for security
- Copying only necessary files
- Using `--no-cache-dir` to reduce image size
- Setting proper environment variables
- Using ENTRYPOINT for a consistent startup command

### 3.2 Flask Application Code

The Flask application (`src/main.py`) provides:

```python
import os
from flask import Flask, jsonify

app = Flask(__name__)

PORT = os.environ.get("PORT", "5000")

@app.route("/liveness", methods=["GET"])
def liveness():
    return jsonify({"message": "liveness OK"}), 200

@app.route("/readiness", methods=["GET"])
def readiness():
    return jsonify({"message": "readiness OK"}), 200

@app.route("/welcome", methods=["GET"])
def get_message():
    return jsonify({"message": "Welcome to docker private reg example"}), 200

@app.route("/welcomeFail", methods=["GET"])
def get_message_fail():
    return jsonify({"message": "This is a failure"}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=PORT)
```

This implements:
- Environment variable configuration
- Health check endpoints (liveness/readiness)
- Standard welcome endpoint
- Test failure endpoint for testing error handling

### 3.3 Building the Image

Build the local image with:

```bash
docker build -t service1:1.0 .
```

### 3.4 Tagging for the Private Registry

Tag the image for the private registry with:

```bash
docker tag service1:1.0 localhost:8082/service1:1.0
```

### 3.5 Logging in to the Registry

Authenticate to the private registry:

```bash
docker login localhost:8082
```

Using Nexus credentials:
- Username: `admin`
- Password: `admin123`

### 3.6 Pushing to the Registry

Push the tagged image to the private registry:

```bash
docker push localhost:8082/service1:1.0
```

## Part 4: Running the Application from the Private Registry

### 4.1 Docker Compose for Deployment

The `docker-compose-service1.yaml` file for running the service from the private registry:

```yaml
version: '3.8'

services:
  service1:
    image: localhost:8082/service1:1.0
    ports:
      - "5000:5000"
    environment:
      - PORT=5000
```

### 4.2 Deploying the Service

Deploy the service with:

```bash
docker-compose -f docker-compose-service1.yaml -p service1 up
```

This pulls the image from the private registry and runs it with the specified configuration.

### 4.3 Testing the Deployed Service

Test the running service with:

```bash
curl http://localhost:5000/welcome
curl http://localhost:5000/liveness
curl http://localhost:5000/readiness
```

## Part 5: Advanced Topics

### 5.1 Implementing Registry Security

For a production environment, enhance security with:

1. **HTTPS/TLS Configuration**:
   Configure Nexus with proper TLS certificates to enable HTTPS.

2. **Role-Based Access Control**:
   Create specific roles and users with least privilege access:
   ```
   Administration → Security → Roles → Create role
   Administration → Security → Users → Create user
   ```

3. **Repository Access Policies**:
   Set specific access policies for each repository:
   ```
   Administration → Repositories → Select repository → Security
   ```

### 5.2 Working with Registry Authentication in CI/CD

For CI/CD pipelines, use authentication with:

1. **Using Docker Login in CI/CD**:
   ```yaml
   - name: Login to private registry
     run: |
       echo "$REGISTRY_PASSWORD" | docker login localhost:8082 -u $REGISTRY_USERNAME --password-stdin
   ```

2. **Using Docker Credentials Helper**:
   ```bash
   docker-credential-helper store
   ```

### 5.3 Efficient Image Management

Best practices for managing images:

1. **Image Tagging Strategy**:
   - Use semantic versioning
   - Use build numbers or git hashes
   - Example: `myapp:1.2.3-build.456`

2. **Image Cleanup Policies**:
   In Nexus, configure cleanup policies:
   ```
   Administration → Cleanup Policies → Create
   ```

3. **Image Layering Optimization**:
   - Order Dockerfile commands for optimal caching
   - Group related commands in a single RUN statement

## Troubleshooting

### Common Issues and Solutions

1. **Cannot push to registry**:
   - Verify insecure registry configuration
   - Check network connectivity
   - Confirm credentials are correct

2. **Certificate issues**:
   - Add certificates to Docker trust store
   - Verify certificate validity and chain

3. **Permission denied errors**:
   - Check user roles and permissions in Nexus
   - Verify repository access settings

4. **Performance issues**:
   - Configure Nexus JVM settings for better performance
   - Use proxying and caching

## Best Practices Summary

1. **Security**: 
   - Always use HTTPS in production
   - Implement proper authentication and authorization
   - Run containers as non-root users

2. **Performance**:
   - Use efficient image layering
   - Implement cleanup policies
   - Configure appropriate resource limits

3. **Reliability**:
   - Ensure data persistence with volumes
   - Implement backup strategies
   - Configure high availability

4. **Organization**:
   - Use consistent naming conventions
   - Implement proper tagging strategies
   - Document registry usage and policies 