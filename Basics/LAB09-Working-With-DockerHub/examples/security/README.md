# Docker Hub Security Features and Best Practices

This directory contains examples and instructions for using Docker Hub's security features and implementing Docker image security best practices.

## Docker Hub Security Features

Docker Hub offers several security features:

1. **Vulnerability Scanning**: Automatically scan images for known vulnerabilities
2. **Access Controls**: Limit who can push or pull images
3. **Image Signing**: Verify image authenticity (Docker Content Trust)
4. **Two-Factor Authentication**: Secure your Docker Hub account
5. **Webhooks**: Notify third-party services of image updates
6. **Docker Certified Images**: Official trusted images

## Enabling Vulnerability Scanning

Vulnerability scanning identifies security issues in your Docker images:

1. Log in to Docker Hub
2. Navigate to your repository
3. Click on "Settings" in the left sidebar
4. Enable "Scan on Push"

Note: Docker Hub's free tier may have limitations on scanning features. Check the current offering.

## Understanding Vulnerability Reports

Docker Hub displays vulnerability information for each image:

1. Navigate to your repository
2. Click on a specific tag
3. View the "Security" tab
4. Review vulnerabilities by severity (Critical, High, Medium, Low)

## Common Docker Image Vulnerabilities

The following issues are commonly found in Docker images:

1. **Outdated base images**: Using old versions with known vulnerabilities
2. **Excessive packages**: Unnecessarily large attack surface
3. **Vulnerable dependencies**: Libraries with security flaws
4. **Insecure configurations**: Poor permissions or exposed secrets
5. **Running as root**: Unnecessary privileges

## Fixing Vulnerabilities

### 1. Updating Base Images

```dockerfile
# VULNERABLE: Using an old Ubuntu version
FROM ubuntu:18.04

# SECURE: Using a newer version
FROM ubuntu:22.04

# BETTER: Using a minimal base image
FROM alpine:3.17
```

### 2. Minimizing Installed Packages

```dockerfile
# VULNERABLE: Installing unnecessary packages
RUN apt-get update && apt-get install -y package1 package2 package3 package4 ...

# SECURE: Installing only what's needed with cleanup
RUN apt-get update && \
    apt-get install --no-install-recommends -y package1 package2 && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*
```

### 3. Updating Dependencies

For Python applications:
```
# requirements.txt - VULNERABLE
flask==1.0.0
requests==2.20.0

# requirements.txt - SECURE
flask==2.3.3
requests==2.31.0
```

### 4. Non-Root User

```dockerfile
# VULNERABLE: Running as root (default)

# SECURE: Creating and using a non-root user
RUN addgroup --system app && \
    adduser --system --group app

USER app
```

### 5. Removing Secrets from Images

```dockerfile
# VULNERABLE: Hardcoding secrets
ENV API_KEY="my-secret-key"

# SECURE: Using build arguments (provide at build time)
ARG API_KEY
ENV API_KEY=$API_KEY

# BETTER: Using runtime secrets or environment variables
# (provide when running the container)
```

## Image Scanning Tools

In addition to Docker Hub scanning, you can use these tools:

1. **Trivy**: `trivy image yourusername/yourimage:tag`
2. **Clair**: A self-hosted scanning solution
3. **Snyk**: Integrates with CI/CD pipelines
4. **Docker Scout**: `docker scout cves yourusername/yourimage:tag`

## Docker Content Trust

Docker Content Trust provides image signing and verification:

```bash
# Enable Docker Content Trust
export DOCKER_CONTENT_TRUST=1

# Push a signed image
docker push yourusername/yourimage:latest

# Pull a signed image (will verify signature)
docker pull yourusername/yourimage:latest
```

## Sample Vulnerable Application

This directory includes:

- `vulnerable-app/`: An application with intentional vulnerabilities
- `secure-app/`: The fixed, secure version of the same application

## TODO

Complete the following tasks:
1. Enable vulnerability scanning for your Docker Hub repository
2. Analyze the scan results for the provided vulnerable image
3. Fix the vulnerabilities identified in the image
4. Implement security best practices for Docker images
5. Document the security features of Docker Hub and their limitations
6. Create a file called `security_notes.md` with your findings and fixes 