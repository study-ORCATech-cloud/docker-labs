# Dependency Caching Example

This directory demonstrates how to leverage Docker's build cache for faster build times, especially for dependency installation.

## The Problem with Poor Caching

When Docker builds an image, it can reuse cached layers if nothing has changed. However, poor practices can invalidate the cache unnecessarily, leading to:
- Longer build times
- Repeated downloads of dependencies
- Wasted resources
- Slower development and CI/CD pipelines

## Project Structure

- `app.py`: A simple Flask application
- `requirements.txt`: Python dependencies
- `Dockerfile`: An unoptimized Dockerfile that doesn't leverage caching

## Task: Optimize Build Cache Usage

The goal is to improve the Dockerfile to better leverage Docker's build cache by:
1. Ordering instructions from least to most frequently changing
2. Copying and installing dependencies before copying application code
3. Using multi-stage builds where appropriate

## Instructions

1. Build the unoptimized image and note the build time:
   ```bash
   time docker build -t cache-demo:unoptimized .
   ```

2. Make a small change to `app.py` (e.g., modify a message) and rebuild:
   ```bash
   time docker build -t cache-demo:unoptimized .
   ```
   - Notice how all layers after the COPY instruction are rebuilt

3. Refactor the Dockerfile to:
   - Copy only `requirements.txt` first
   - Install dependencies
   - Then copy the rest of the application

4. Build your optimized version:
   ```bash
   time docker build -t cache-demo:optimized -f Dockerfile.optimized .
   ```

5. Make the same small change to `app.py` and rebuild:
   ```bash
   time docker build -t cache-demo:optimized -f Dockerfile.optimized .
   ```
   - Observe how the dependency installation step uses the cache

6. Compare build times with and without cache optimization

## Best Practices

- **Order from least to most changing**: Place rarely changing operations first
- **Copy dependency files first**: Copy `package.json`, `requirements.txt`, etc. before app code
- **Install dependencies before copying app code**: So changes to app code don't invalidate dependency cache
- **Use specific base image tags**: Don't use 'latest' to ensure consistent builds
- **Consider multi-stage builds**: Separate build-time dependencies from runtime

## TODO

Complete the following tasks:
1. Refactor the Dockerfile to better leverage Docker's build cache
2. Copy dependency files first (requirements.txt) before copying application code
3. Install dependencies before copying the rest of the application
4. Use pip's cache directory mounting if available in your environment
5. Consider using multi-stage builds if there are build dependencies
6. Measure and document the build time improvements 