# Advanced Docker Image Management

This guide covers advanced Docker image management techniques using CLI commands.

## Overview

Effective Docker image management is crucial for:
- Maintaining a clean and efficient Docker host
- Reducing storage usage and build times
- Implementing proper versioning strategies
- Optimizing image distribution
- Ensuring security and compliance

## Basic Image Commands Review

Before diving into advanced techniques, let's review the essential commands:

```bash
# List all images
docker images
docker image ls

# Pull an image
docker pull nginx:latest

# Build an image
docker build -t myapp:1.0 .

# Remove an image
docker rmi nginx:latest
docker image rm nginx:latest

# Tag an image
docker tag myapp:1.0 myapp:latest

# Push an image
docker push myregistry/myapp:1.0
```

## Advanced Image Filtering

Docker provides powerful filtering capabilities for managing images:

```bash
# Filter by reference (repository/tag)
docker images --filter=reference=nginx:*

# Filter by label
docker images --filter=label=environment=production

# Filter dangling images (untagged)
docker images --filter=dangling=true

# Filter by time (created before/after specific image)
docker images --filter=before=nginx:1.19
docker images --filter=since=myapp:1.0

# Filter by build date
docker images --filter=before=2023-01-01
```

## Image Cleanup Strategies

### Removing Unused Images

```bash
# Remove dangling images (untagged)
docker image prune

# Remove all unused images (not just dangling)
docker image prune -a

# Remove unused images older than 24h
docker image prune -a --filter "until=24h"

# Remove images with a specific label
docker image prune -a --filter "label=environment=staging"
```

### System-Wide Cleanup

```bash
# View current disk usage
docker system df

# Detailed view of disk usage
docker system df -v

# Remove all unused data (includes images, containers, volumes, networks)
docker system prune

# Remove all unused data including volumes
docker system prune -a --volumes
```

## Image Inspection and Analysis

### Basic Image Inspection

```bash
# View detailed image information
docker inspect nginx:latest

# Format specific information
docker inspect --format='{{.Size}}' nginx:latest

# Check image layers
docker inspect --format='{{.RootFS.Layers}}' nginx:latest

# View image history (how the image was built)
docker history nginx:latest

# View image history without truncation
docker history --no-trunc nginx:latest
```

### Advanced Layer Analysis

```bash
# Compare layers between two images
diff <(docker inspect --format='{{json .RootFS.Layers}}' image1) <(docker inspect --format='{{json .RootFS.Layers}}' image2) | jq

# Identify large layers
docker history --format "{{.Size}}\t{{.CreatedBy}}" nginx:latest | sort -hr

# Count number of layers
docker inspect --format='{{len .RootFS.Layers}}' nginx:latest
```

## Image Tagging Strategies

### Semantic Versioning

```bash
# Major.Minor.Patch tagging
docker tag myapp:1.0.0 myregistry/myapp:1.0.0
docker tag myapp:1.0.0 myregistry/myapp:1.0
docker tag myapp:1.0.0 myregistry/myapp:1
docker tag myapp:1.0.0 myregistry/myapp:latest
```

### Environment-Based Tagging

```bash
# Tag by environment
docker tag myapp:$GIT_COMMIT myregistry/myapp:dev
docker tag myapp:$GIT_COMMIT myregistry/myapp:staging
docker tag myapp:$GIT_COMMIT myregistry/myapp:production
```

### Automated Tagging

```bash
# Auto tag based on git branch/commit
GIT_BRANCH=$(git rev-parse --abbrev-ref HEAD)
GIT_COMMIT=$(git rev-parse --short HEAD)
docker tag myapp:latest myregistry/myapp:$GIT_BRANCH
docker tag myapp:latest myregistry/myapp:$GIT_COMMIT
```

## Multi-Architecture Image Management

### Inspecting Image Architectures

```bash
# Check image manifest information
docker manifest inspect nginx:latest

# View supported platforms
docker manifest inspect --verbose nginx:latest | jq '.Descriptor.platform'
```

### Building Multi-Architecture Images

```bash
# Create and use a multi-architecture builder
docker buildx create --name mybuilder --use

# Build and push multi-arch image
docker buildx build --platform linux/amd64,linux/arm64 -t myregistry/myapp:latest --push .
```

## Image Storage and Distribution Optimization

### Content-Addressable Storage

Docker uses content-addressable storage, meaning identical layers are stored only once:

```bash
# View shared layers
docker inspect --format='{{json .RootFS.Layers}}' $(docker images -q) | jq
```

### Optimizing Image Size

```bash
# Find the top 10 largest images
docker images --format "{{.Repository}}:{{.Tag}} {{.Size}}" | sort -rn -k2 | head -10

# Export image to a tarball
docker save -o myapp.tar myapp:latest

# Import an image from a tarball
docker load -i myapp.tar
```

## Registry Interaction

### Authentication

```bash
# Log in to a registry
docker login registry.example.com

# Log in with credentials
docker login -u username -p password registry.example.com

# View current authentication configuration
cat ~/.docker/config.json
```

### Registry Operations

```bash
# List tags for an image in a registry
curl -X GET https://registry.example.com/v2/myapp/tags/list | jq

# Delete an image from a registry (if the registry supports it)
curl -X DELETE https://registry.example.com/v2/myapp/manifests/$(curl -I -H "Accept: application/vnd.docker.distribution.manifest.v2+json" https://registry.example.com/v2/myapp/manifests/mytag | grep Docker-Content-Digest | awk '{print $2}' | tr -d '\r')
```

## Automated Image Management

### Scheduled Cleanup

```bash
# Create a cron job for regular cleanup
echo "0 2 * * * docker image prune -a --force --filter 'until=168h'" | sudo tee -a /etc/crontab
```

### Pulling Updated Images

```bash
# Check for and pull updates
docker-compose pull && docker-compose up -d
```

## Image Security

### Vulnerability Scanning

```bash
# Scan an image for vulnerabilities
docker scout cves nginx:latest

# Get a security overview
docker scout quickview nginx:latest
```

### Image Signing

```bash
# Sign an image with Docker Content Trust
export DOCKER_CONTENT_TRUST=1
docker push myregistry/myapp:latest
```

## TODO Tasks

1. Implement a comprehensive image cleanup strategy:
   - Create a command to identify all unused images
   - Define criteria for determining which images to keep
   - Implement safe cleanup of unnecessary images

2. Develop an image tagging convention:
   - Define a consistent tagging strategy (e.g., semantic versioning)
   - Create a process for managing latest vs. specific version tags
   - Document your tagging convention

3. Create a layer analysis tool:
   - Identify the largest layers in your images
   - Compare layers between different versions of the same image
   - Find opportunities to reduce image size

4. Build a multi-architecture image:
   - Set up a buildx environment
   - Create an image that works on multiple architectures
   - Test the image on different platforms

5. Implement a registry management system:
   - Define policies for how long to keep images
   - Create a cleanup mechanism for old images in your registry
   - Set up periodic vulnerability scanning

6. Automate image updates:
   - Create a system to check for base image updates
   - Implement automatic rebuilds when dependencies change
   - Set up notifications for new image versions

7. Develop an image inventory system:
   - Track which images are used in production
   - Document the purpose and contents of each image
   - Map image dependencies

8. Implement image security practices:
   - Enable Docker Content Trust for signing images
   - Perform regular vulnerability scans
   - Create policies for addressing security issues

9. Optimize image build and distribution:
   - Implement build caching strategies
   - Configure registry mirroring
   - Set up distribution across multiple regions

10. Document your image management workflow:
    - Create a reference guide for common tasks
    - Define standard operating procedures for image lifecycle management
    - Set up monitoring for image storage and usage

## Additional Resources

- [Docker Image Command Reference](https://docs.docker.com/engine/reference/commandline/image/)
- [Docker Tag Strategy](https://docs.docker.com/develop/dev-best-practices/)
- [Docker Content Trust](https://docs.docker.com/engine/security/trust/)
- [Docker BuildKit and BuildX](https://docs.docker.com/build/buildkit/)
- [Docker Scout for Security Scanning](https://docs.docker.com/scout/) 