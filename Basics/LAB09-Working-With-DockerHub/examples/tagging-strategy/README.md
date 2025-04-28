# Docker Image Tagging Strategies

This directory contains examples and instructions for implementing effective Docker image tagging strategies.

## Understanding Tagging

Docker image tags help identify different versions or variants of an image:

```
username/repository:tag
```

While you can use any tag name, following consistent strategies helps manage images effectively.

## Semantic Versioning

Semantic Versioning (SemVer) is a widely adopted versioning scheme with the format:

```
MAJOR.MINOR.PATCH
```

- **MAJOR**: Incompatible API changes
- **MINOR**: Add functionality in a backward-compatible manner
- **PATCH**: Backward-compatible bug fixes

### Implementation in Docker

```bash
docker build -t username/myapp:1.0.0 .  # Initial version
docker build -t username/myapp:1.0.1 .  # Bug fix
docker build -t username/myapp:1.1.0 .  # New features
docker build -t username/myapp:2.0.0 .  # Breaking changes
```

## Hierarchical Tagging

You can create a tag hierarchy to simplify pulling the right version:

```bash
docker build -t username/myapp:1.2.3 .
docker tag username/myapp:1.2.3 username/myapp:1.2
docker tag username/myapp:1.2.3 username/myapp:1
```

A consumer can choose specificity:
- `username/myapp:1.2.3` - Exact version
- `username/myapp:1.2` - Latest patch in 1.2.x
- `username/myapp:1` - Latest minor and patch in 1.x.x

## The `latest` Tag

The `latest` tag is special but often misunderstood:
- It's the default tag when none is specified
- It doesn't automatically update when new versions are pushed
- It should generally point to the most recent stable version

```bash
# Build and tag a specific version
docker build -t username/myapp:1.2.3 .

# Also tag it as latest
docker tag username/myapp:1.2.3 username/myapp:latest

# Push both tags
docker push username/myapp:1.2.3
docker push username/myapp:latest
```

## Environment-specific Tags

For CI/CD pipelines, consider environment-specific tags:

```bash
docker build -t username/myapp:1.2.3 .
docker tag username/myapp:1.2.3 username/myapp:dev
docker tag username/myapp:1.2.3 username/myapp:staging
docker tag username/myapp:1.2.3 username/myapp:prod
```

This allows deployment scripts to always pull from the same tag:
```bash
# In production deployment script
docker pull username/myapp:prod
```

## Git-based Tagging

Link Docker tags to Git references:

```bash
# By branch
docker build -t username/myapp:main .

# By commit hash (short)
docker build -t username/myapp:$(git rev-parse --short HEAD) .

# By git tag
docker build -t username/myapp:$(git describe --tags) .
```

## Variant Tagging

Indicate image variants:

```bash
username/myapp:1.2.3-alpine   # Alpine-based
username/myapp:1.2.3-slim     # Slim variant
username/myapp:1.2.3-python3.9 # Specific Python version
```

## Immutable vs. Mutable Tags

- **Immutable tags** never change (e.g., version numbers, commit hashes)
- **Mutable tags** may point to different images over time (e.g., `latest`, `stable`, environment tags)

Best practice is to use both:
1. Always tag with immutable identifiers
2. Use mutable tags as convenient references

## Sample Application

This directory includes a simple versioned application:
- `app.py`: A simple Python API with version information
- `requirements.txt`: Python dependencies
- `Dockerfile`: Instructions to build the image

## TODO

Complete the following tasks:
1. Implement semantic versioning for the provided application
   - Build a v1.0.0 image
   - Make a small change and build a v1.0.1 image
   - Make a feature addition and build a v1.1.0 image
2. Create multiple tagged versions of the same image
   - Implement the hierarchical tagging scheme (1.2.3, 1.2, 1)
3. Use the `latest` tag appropriately
   - Ensure it points to your newest stable version
4. Implement environment-specific tags
   - Tag your image with dev, staging, and prod tags
5. Document your tagging strategy in `tagging_strategy.md`
   - Explain your approach and its benefits
   - Provide example commands for your strategy 