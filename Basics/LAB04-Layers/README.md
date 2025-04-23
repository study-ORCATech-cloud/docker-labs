# LAB04: Docker Image Layers

This lab will help you understand Docker image layers, how they are created, and how to optimize them for efficiency and performance.

## Lab Overview

In this lab, you will:
- Understand the layered filesystem architecture of Docker images
- Learn how Dockerfile instructions create layers
- Analyze and inspect image layers
- Optimize Dockerfiles for better caching and smaller images
- Use multi-stage builds to reduce final image size
- Compare optimized vs non-optimized Docker images

## Learning Objectives

- Understand Docker's layered architecture
- Learn how to minimize the number and size of layers
- Master techniques for creating efficient Docker images
- Analyze image layers using Docker commands
- Implement multi-stage builds to separate build and runtime dependencies
- Apply best practices for optimizing Dockerfiles

## Prerequisites

- Docker Engine installed
- Completion of LAB01-GettingStarted, LAB02-BuildingImages, and LAB03-Volumes
- Basic understanding of Dockerfiles

## Lab Projects

This lab includes three example projects:

1. **single-stage**: A simple Python application with a basic, unoptimized Dockerfile
2. **multi-stage**: The same application with an optimized multi-stage Dockerfile
3. **analysis**: Tools and examples for analyzing Docker image layers

## Lab Tasks

### Task 1: Understanding Docker Layers

Every Docker image is made up of layers. Each instruction in a Dockerfile creates a new layer:

- `FROM`: The base layer from a parent image
- `RUN`: Creates a new layer with the results of command execution
- `COPY`/`ADD`: Creates a layer with the copied files
- `CMD`, `ENTRYPOINT`, `ENV`, `LABEL`: Do not create new layers, only metadata

Other instructions like `WORKDIR`, `EXPOSE`, and `VOLUME` also don't create separate layers, they just add metadata.

### Task 2: Build and Analyze a Basic Image

Navigate to the `single-stage` directory:

```bash
cd examples/single-stage
```

Build the image:

```bash
docker build -t layers-demo:unoptimized .
```

Analyze the layers:

```bash
docker history layers-demo:unoptimized
```

Notice how many layers are created and their sizes.

### Task 3: Optimize with Multi-stage Builds

Navigate to the `multi-stage` directory:

```bash
cd ../multi-stage
```

Build the optimized image:

```bash
docker build -t layers-demo:optimized .
```

Analyze and compare with the unoptimized version:

```bash
docker history layers-demo:optimized
docker images layers-demo:*
```

Notice the difference in size and number of layers.

### Task 4: Analyze Image Details

Navigate to the `analysis` directory:

```bash
cd ../analysis
```

Use dive tool to analyze the images:

```bash
# Install dive tool (if not available)
docker run --rm -it \
  -v /var/run/docker.sock:/var/run/docker.sock \
  wagoodman/dive:latest layers-demo:unoptimized

# Analyze the optimized image
docker run --rm -it \
  -v /var/run/docker.sock:/var/run/docker.sock \
  wagoodman/dive:latest layers-demo:optimized
```

### Task 5: Apply Layer Optimization Techniques

Below are key optimization techniques to apply in your Dockerfiles:

1. **Combine related commands** into a single RUN instruction using `&&` and `\`
2. **Use .dockerignore** to exclude unnecessary files from the build context
3. **Order instructions from least to most frequently changing**
4. **Remove unnecessary files** in the same layer they were added
5. **Use multi-stage builds** to separate build and runtime dependencies
6. **Use specific base image tags** rather than 'latest'
7. **Consider using Alpine-based images** for smaller footprints

### Task 6: Implement Advanced Multi-stage Patterns

Explore the `multi-stage` directory for examples of:
- Separating build and runtime environments
- Using the builder pattern
- Copying only necessary artifacts
- Leveraging base and target stages

## Best Practices Summary

1. **Keep layers minimal**: Combine commands, clean up within the same RUN instruction
2. **Choose appropriate base images**: Alpine or distroless for smaller images
3. **Leverage build cache**: Order Dockerfile instructions from least to most frequently changing
4. **Use multi-stage builds**: Keep build tools out of the final image
5. **Be explicit with tags**: Don't use 'latest' for reproducible builds
6. **Clean up**: Remove build dependencies and temporary files in the same layer
7. **Use .dockerignore**: Keep the build context small

## Real-World Benefits

Optimized Docker images provide many advantages:
- Faster build times and deployments
- Reduced storage and bandwidth costs
- Improved security through smaller attack surfaces
- Better development and CI/CD performance

## Clean Up

```bash
docker rmi layers-demo:unoptimized layers-demo:optimized
```

## Next Steps

Proceed to LAB05-Debugging to learn about debugging and troubleshooting Docker containers. 