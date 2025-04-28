# Docker Security Scanning from CLI

This guide covers Docker security scanning tools and best practices using the command line interface.

## Overview

Docker provides several CLI tools and techniques to scan container images for vulnerabilities and ensure the security of your containerized applications. In this module, you will learn:

- How to use Docker Scout for security scanning
- Techniques for integrating scanning into CI/CD pipelines
- Methods for automating security checks
- Best practices for container security
- Approaches for remediation and mitigation

## Docker Scout

Docker Scout is an integrated security scanning tool that helps identify vulnerabilities in your container images.

### Basic Scanning Commands

```bash
# Install Docker Scout plugin (if not already installed)
docker extension install docker/scout-extension

# Analyze an image for vulnerabilities
docker scout cves alpine:latest

# Get a quick vulnerability overview
docker scout quickview nginx:latest

# Compare two images
docker scout compare nginx:1.21 nginx:1.22
```

### Detailed Analysis

```bash
# Get detailed vulnerability information
docker scout cves --format json nginx:latest

# Filter by severity
docker scout cves --only-severity critical,high nginx:latest

# Show recommendations for remediation
docker scout recommendations nginx:latest

# Export results to a file
docker scout cves --format sarif nginx:latest > nginx-scan.sarif
```

### Continuous Scanning

```bash
# Scan an image before pushing
docker scout cves myapp:latest --exit-code

# Set a policy for acceptable vulnerabilities
docker scout policy set --min-severity high
docker scout policy evaluate myapp:latest
```

## Trivy Integration

Trivy is a popular open-source security scanner that can be used alongside Docker.

### Basic Trivy Commands

```bash
# Install Trivy (if not already installed)
# Example for Ubuntu/Debian:
apt-get install -y trivy

# Scan an image
trivy image nginx:latest

# Scan with severity filtering
trivy image --severity HIGH,CRITICAL nginx:latest

# Output results in different formats
trivy image --format json --output results.json nginx:latest
```

### Advanced Trivy Usage

```bash
# Scan and fail on specific severity
trivy image --exit-code 1 --severity CRITICAL nginx:latest

# Ignore unfixed vulnerabilities
trivy image --ignore-unfixed nginx:latest

# Scan with custom policy
trivy image --config trivy-policy.yaml nginx:latest
```

## Scanning in CI/CD Pipelines

### Example Pipeline Integration

```bash
# Example script for CI/CD pipeline
#!/bin/bash

# Build the image
docker build -t myapp:${CI_COMMIT_SHA} .

# Run security scan
docker scout cves myapp:${CI_COMMIT_SHA} --exit-code

# If scan passes, tag and push
if [ $? -eq 0 ]; then
  docker tag myapp:${CI_COMMIT_SHA} myregistry/myapp:latest
  docker push myregistry/myapp:latest
else
  echo "Security scan failed. Image contains critical vulnerabilities."
  exit 1
fi
```

### Customizing Scan Policies

Define custom policies based on your security requirements:

```bash
# Create a policy file (trivy-policy.yaml)
cat > trivy-policy.yaml << EOF
ignore:
  - id: CVE-2023-12345
    reason: "Not applicable to our environment"
    until: 2023-12-31
  - id: CVE-2023-67890
    reason: "Mitigated by network controls"
severity:
  - CRITICAL
  - HIGH
EOF

# Use the policy file
trivy image --config trivy-policy.yaml myapp:latest
```

## Runtime Security Checks

### Docker Bench Security

Docker Bench Security is a script that checks for dozens of common best practices around deploying Docker containers in production.

```bash
# Clone the Docker Bench Security repository
git clone https://github.com/docker/docker-bench-security.git
cd docker-bench-security

# Run the security checks
./docker-bench-security.sh

# Run specific tests
./docker-bench-security.sh -t container
```

### Docker Socket Security

```bash
# Check Docker socket permissions
ls -la /var/run/docker.sock
# Should show: srw-rw---- 1 root docker 0 ... /var/run/docker.sock

# Verify Docker group membership
groups $(whoami) | grep docker
```

## Image Hardening and Best Practices

### Minimal Base Images

```bash
# Use minimal base images in your Dockerfile
FROM alpine:latest
# Or
FROM scratch
```

### Non-Root Users

```bash
# Create and use non-root user in your Dockerfile
RUN addgroup -S appgroup && adduser -S appuser -G appgroup
USER appuser
```

### Remove Unnecessary Tools

```bash
# Alpine example: install temporarily needed packages, then remove them
RUN apk add --no-cache --virtual .build-deps gcc make \
    && pip install --no-cache-dir -r requirements.txt \
    && apk del .build-deps
```

## Automated Security Workflows

### Scheduled Scans

```bash
# Create a script for scheduled scanning
cat > scan-images.sh << 'EOF'
#!/bin/bash
IMAGES=$(docker image ls --format "{{.Repository}}:{{.Tag}}" | grep -v "<none>")
DATE=$(date +%Y-%m-%d)

for img in $IMAGES; do
  echo "Scanning $img..."
  docker scout cves --format json "$img" > "scans/${img//\//_}_${DATE}.json"
done
EOF
chmod +x scan-images.sh

# Set up a cron job
echo "0 2 * * * /path/to/scan-images.sh" | crontab -
```

### Vulnerability Monitoring

```bash
# Create a vulnerability monitoring script
cat > monitor-vulns.sh << 'EOF'
#!/bin/bash
IMAGES=$(docker image ls --format "{{.Repository}}:{{.Tag}}" | grep -v "<none>")
DATE=$(date +%Y-%m-%d)

for img in $IMAGES; do
  echo "Checking $img for critical vulnerabilities..."
  CRIT_COUNT=$(docker scout cves --format json "$img" | jq '.vulnerabilities[] | select(.severity == "critical") | .vulnerability_id' | wc -l)
  if [ $CRIT_COUNT -gt 0 ]; then
    echo "[ALERT] $img contains $CRIT_COUNT critical vulnerabilities!" | mail -s "Security Alert: $img" security@example.com
  fi
done
EOF
chmod +x monitor-vulns.sh
```

## Image Signing and Verification

### Content Trust

```bash
# Enable Docker Content Trust
export DOCKER_CONTENT_TRUST=1

# Push a signed image
docker push myregistry/myapp:latest

# Verify a signed image
docker trust inspect --pretty myregistry/myapp:latest
```

### Key Management

```bash
# Generate signing keys
docker trust key generate my-signing-key

# Add a signer to a repository
docker trust signer add --key my-signing-key.pub my-signer myregistry/myapp
```

## Advanced Security Analysis

### Layer Analysis

```bash
# Analyze which layer introduced vulnerabilities
docker history --no-trunc myapp:latest > history.txt
docker scout cves --format json myapp:latest > vulns.json

# Correlate the two to find which build step introduced vulnerabilities
```

### Base Image Recommendations

```bash
# Find a more secure base image
docker scout recommendations --alternate-base-image --only-fixed alpine:latest
```

## TODO Tasks

1. Set up a basic security scanning workflow:
   - Install Docker Scout or Trivy
   - Create a script to scan your local images
   - Generate reports in different formats (JSON, HTML)
   - Document your scanning process

2. Integrate security scanning in a sample CI/CD pipeline:
   - Create a script that builds and scans an image
   - Implement policy enforcement based on vulnerability severity
   - Set up notifications for security issues
   - Document the integration process

3. Implement automated vulnerability monitoring:
   - Create a scheduled job to scan images regularly
   - Set up alerting for new critical vulnerabilities
   - Track vulnerability trends over time
   - Document your monitoring approach

4. Perform a Docker Bench Security assessment:
   - Run Docker Bench Security on your environment
   - Address the high-priority findings
   - Create an action plan for medium and low findings
   - Document your remediation steps

5. Harden a sample container image:
   - Choose a minimal base image
   - Implement non-root user execution
   - Remove unnecessary tools and packages
   - Document the hardening techniques you applied

6. Set up image signing and verification:
   - Configure Docker Content Trust
   - Create signing keys
   - Implement signed image verification
   - Document your signing workflow

7. Develop a vulnerability management policy:
   - Define acceptable vulnerability levels
   - Create a process for addressing vulnerabilities
   - Implement a vulnerability exception process
   - Document your policy and procedures

8. Perform base image analysis:
   - Compare security profiles of different base images
   - Identify the most secure options for your needs
   - Document your findings and recommendations

9. Implement security monitoring in a development workflow:
   - Create pre-commit hooks for security scanning
   - Set up development environment scanning
   - Implement a feedback loop for security findings
   - Document your developer security workflow

10. Create a comprehensive security reporting dashboard:
    - Collect scanning results from multiple sources
    - Generate consolidated security reports
    - Implement trend analysis and visualization
    - Document your reporting approach

## Additional Resources

- [Docker Scout Documentation](https://docs.docker.com/scout/)
- [Trivy Documentation](https://aquasecurity.github.io/trivy/)
- [Docker Bench Security](https://github.com/docker/docker-bench-security)
- [Docker Content Trust](https://docs.docker.com/engine/security/trust/)
- [CIS Docker Benchmark](https://www.cisecurity.org/benchmark/docker)
- [OWASP Docker Security Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Docker_Security_Cheat_Sheet.html) 