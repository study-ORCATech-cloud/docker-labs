# LAB08: Dockerfile Best Practices

This lab teaches how to write efficient, secure, and maintainable Dockerfiles for production-ready applications.

## Lab Overview

In this lab, you will:
- Learn Docker image optimization techniques
- Understand multi-stage builds
- Implement security best practices in Dockerfiles
- Reduce image size and layer count
- Apply caching strategies for faster builds
- Create maintainable and standardized Dockerfiles
- Practice refactoring problematic Dockerfiles

## Important Note

**This lab is designed for hands-on learning:**
- Implement all TODOs in the example directories yourself before checking solutions
- Consult the `solutions.md` file *only after* attempting to solve the problems yourself
- Focus on understanding the principles behind each optimization
- All code examples in this lab use Python for consistency

## Learning Objectives

- Master Docker image optimization techniques
- Implement multi-stage builds for efficient images
- Apply security best practices to Docker images
- Understand Docker build cache optimization
- Structure Dockerfiles for maintainability
- Implement CI/CD considerations for Docker builds
- Compare and analyze different Dockerfile strategies

## Prerequisites

- Docker Engine installed
- Completion of LAB01-LAB07
- Basic understanding of Linux command line
- Familiarity with container concepts

## Important Instructions

This lab is designed for hands-on learning. You are expected to:
- Implement solutions yourself for each task
- Analyze and compare different Dockerfile approaches
- Work through the exercises systematically
- Document your findings regarding optimization and best practices

Do not look for ready-made solutions online - the goal is to develop your Dockerfile optimization skills by working through the issues yourself.

## Lab Projects

This lab includes a series of examples in the `examples` directory demonstrating various Dockerfile patterns and anti-patterns.

## Lab Tasks

### Task 1: Understanding Dockerfile Best Practices

Review the key best practices for writing efficient Dockerfiles:

1. **Keep images small**
   - Use appropriate base images
   - Remove unnecessary files
   - Combine related commands

2. **Leverage build cache effectively**
   - Order instructions from least to most frequently changing
   - Use .dockerignore files
   - Understand how the build cache works

3. **Write maintainable Dockerfiles**
   - Document your Dockerfile with comments
   - Use consistent formatting
   - Follow a standard structure

4. **Secure your images**
   - Run as non-root users
   - Use specific version tags
   - Scan for vulnerabilities

### Task 2: Base Image Selection

Navigate to the `examples/base-images` directory:

```bash
cd examples/base-images
```

TODO:
1. Compare the provided examples of different base images
2. Build each example and note the image size
3. Run a simple benchmark test on each to compare performance
4. Consider the security implications of each base image choice
5. Create a recommendation for when to use each type of base image

### Task 3: Multi-stage Builds

Navigate to the `examples/multi-stage` directory:

```bash
cd ../multi-stage
```

TODO:
1. Analyze the provided single-stage and multi-stage examples
2. Build both examples and compare the resulting image sizes
3. Refactor the single-stage example to use multi-stage builds
4. Optimize the multi-stage example further to reduce size
5. Create your own multi-stage build for a language of your choice

### Task 4: Layer Optimization

Navigate to the `examples/layer-optimization` directory:

```bash
cd ../layer-optimization
```

TODO:
1. Analyze the provided Dockerfile with multiple layers
2. Use `docker history` to understand the impact of each instruction
3. Refactor the Dockerfile to reduce the number of layers
4. Compare the build time and final size before and after optimization
5. Document the best practices you applied

### Task 5: Caching Dependencies

Navigate to the `examples/caching-dependencies` directory:

```bash
cd ../caching-dependencies
```

TODO:
1. Build the provided Dockerfile and observe the build time
2. Make a small change to the application code and rebuild, noting the build time
3. Refactor the Dockerfile to better leverage the Docker build cache
4. Test your optimized Dockerfile by making the same small change
5. Document the improvements in build time

### Task 6: Security Best Practices

Navigate to the `examples/security` directory:

```bash
cd ../security
```

TODO:
1. Review the provided Dockerfile with security issues
2. Identify all security problems in the Dockerfile
3. Refactor the Dockerfile to address all security concerns
4. Create a checklist of security best practices for Dockerfiles
5. Scan your optimized image for vulnerabilities using a scanning tool

### Task 7: Environment-specific Dockerfiles

Navigate to the `examples/environments` directory:

```bash
cd ../environments
```

TODO:
1. Review the provided Dockerfile examples for development, testing, and production
2. Identify the key differences between environment-specific Dockerfiles
3. Create an improved strategy for managing environment-specific differences
4. Implement a solution using build arguments and/or multi-stage builds
5. Document your approach and its advantages

### Task 8: CI/CD Considerations

Navigate to the `examples/ci-cd` directory:

```bash
cd ../ci-cd
```

TODO:
1. Review the provided CI/CD configuration for Docker builds
2. Identify potential issues and optimization opportunities
3. Implement improvements for faster CI/CD builds
4. Consider caching strategies specific to CI/CD environments
5. Create a document with best practices for Docker in CI/CD

### Task 9: Real-world Application Refactoring

Navigate to the `examples/real-world` directory:

```bash
cd ../real-world
```

TODO:
1. Analyze the provided real-world application Dockerfile
2. Apply all best practices you've learned to refactor it
3. Compare before and after: image size, build time, security, maintainability
4. Document all the improvements you made
5. Create a presentation explaining your optimization strategy

### Task 10: Creating a Dockerfile Style Guide

TODO:
1. Create a comprehensive Dockerfile style guide based on what you've learned
2. Include sections on:
   - Formatting and structure
   - Base image selection
   - Layer optimization
   - Security best practices
   - Environment-specific considerations
   - Documentation requirements
3. Create a template Dockerfile that follows your style guide
4. Apply your style guide to all examples from previous tasks
5. Share your style guide with your team for feedback

## Testing Your Understanding

After completing the lab exercises, you should be able to:
- Apply Dockerfile best practices to real-world applications
- Optimize Docker images for size, security, and build time
- Create efficient multi-stage builds
- Implement proper caching strategies
- Detect and fix common Dockerfile anti-patterns
- Create standardized and maintainable Dockerfiles

## Lab Cleanup

Clean up all containers, images, and volumes created during this lab:

```bash
# Stop all running containers
docker stop $(docker ps -q)

# Remove all containers
docker rm $(docker ps -a -q)

# Remove images created for this lab (if needed)
docker rmi $(docker images -q "lab08*")

# Remove any volumes created for this lab (if needed)
docker volume prune -f
```

## Additional Resources

- [Docker Official Best Practices](https://docs.docker.com/develop/develop-images/dockerfile_best-practices/)
- [Dive Tool for Exploring Docker Images](https://github.com/wagoodman/dive)
- [Hadolint - Dockerfile Linter](https://github.com/hadolint/hadolint)
- [Docker Security Best Practices](https://docs.docker.com/engine/security/security/)
- [Multi-stage Build Documentation](https://docs.docker.com/develop/develop-images/multistage-build/) 