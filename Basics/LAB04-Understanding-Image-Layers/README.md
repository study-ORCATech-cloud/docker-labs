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

## Important Instructions

This lab is designed for hands-on learning. You are expected to:
- Implement solutions yourself rather than copying from external sources
- Write your own code for each TODO item in the exercises
- Document your analysis and findings in your own words
- Test your implementations to see the effects of your optimizations

The goal is to develop your skills in creating efficient Docker images by understanding the underlying principles of Docker's layered architecture.

## Lab Projects

This lab includes three example projects:

1. **single-stage**: A simple Python application with a basic, unoptimized Dockerfile that you'll improve
2. **multi-stage**: The same application with a template for implementing multi-stage builds
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

Navigate to the `single-stage` directory and explore it:

```bash
cd single-stage
```

TODO:
1. Review the `Dockerfile` and identify inefficient practices
2. Build the unoptimized image:
   ```bash
   docker build -t layers-demo:unoptimized .
   ```
3. Analyze the layers:
   ```bash
   docker history layers-demo:unoptimized
   ```
4. Complete the TODOs in the `Dockerfile` to optimize it - implement your own solutions!
5. Build your optimized version and compare results:
   ```bash
   docker build -t layers-demo:optimized-by-you .
   docker history layers-demo:optimized-by-you
   docker images layers-demo:*
   ```

### Task 3: Optimize with Multi-stage Builds

Navigate to the `multi-stage` directory:

```bash
cd ../multi-stage
```

TODO:
1. Review the multi-stage `Dockerfile` template and understand the included TODOs
2. Implement your own solutions for each TODO item - don't just copy from examples
3. Build your optimized image:
   ```bash
   docker build -t layers-demo:multi-stage .
   ```
4. Compare with the single-stage versions:
   ```bash
   docker history layers-demo:multi-stage
   docker images layers-demo:*
   ```

### Task 4: Analyze Image Details

Navigate to the `analysis` directory:

```bash
cd ../analysis
```

TODO:
1. Review the `Dockerfile` with intentional inefficiencies
2. Create your own `layer_analysis.md` file to document your findings
3. Build the unoptimized image:
   ```bash
   docker build -t analysis-demo:unoptimized .
   ```
4. Use the provided tools to analyze the image layers:
   - For Windows: `layer-analysis-windows.bat analysis-demo:unoptimized`
   - For Linux/Mac: `./dive-commands.sh analysis-demo:unoptimized`
5. Create your own optimized version in `Dockerfile.optimized`
6. Compare both images to measure your improvements

### Task 5: Apply Layer Optimization Techniques

Below are key optimization techniques to apply in your Dockerfiles:

1. **Combine related commands** into a single RUN instruction using `&&` and `\`
2. **Use .dockerignore** to exclude unnecessary files from the build context
3. **Order instructions from least to most frequently changing**
4. **Remove unnecessary files** in the same layer they were added
5. **Use multi-stage builds** to separate build and runtime dependencies
6. **Use specific base image tags** rather than 'latest'
7. **Consider using Alpine-based images** for smaller footprints

TODO:
- Implement each of these techniques in your optimized Dockerfiles
- Document the impact of each optimization

### Task 6: Implement Advanced Multi-stage Patterns

Explore the `multi-stage` directory and implement:
- Separation of build and runtime environments
- Using the builder pattern properly
- Copying only necessary artifacts
- Implementing proper security practices (non-root user, etc.)

TODO:
- Enhance your multi-stage Dockerfile to include security best practices
- Experiment with different base images (full, slim, alpine) and compare

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
docker rmi layers-demo:unoptimized layers-demo:optimized-by-you layers-demo:multi-stage
docker rmi analysis-demo:unoptimized analysis-demo:optimized
```

## Next Steps

Proceed to LAB05-Debugging to learn about debugging and troubleshooting Docker containers. 