# Layer Optimization Example

This directory demonstrates how to optimize Docker image layers for improved efficiency and performance.

## The Problem with Too Many Layers

Each instruction in a Dockerfile creates a new layer:
- `RUN`, `COPY`, and `ADD` all create new layers
- Excessive layers can lead to larger images and slower build times
- Each layer adds metadata overhead

## Project Structure

- `app.py`: A Flask application with Redis dependency
- `requirements.txt`: Python dependencies
- `Dockerfile`: An unoptimized Dockerfile with many layers

## Task: Optimize Dockerfile Layers

The goal is to reduce the number of layers in the Dockerfile by:
1. Combining related commands
2. Using proper layer caching techniques
3. Cleaning up temporary files properly
4. Ordering instructions efficiently

## Instructions

1. Analyze the unoptimized `Dockerfile`
   - Count the number of layers it creates
   - Identify inefficient practices

2. Build the unoptimized image:
   ```bash
   docker build -t layer-demo:unoptimized .
   ```

3. Analyze the layer structure:
   ```bash
   docker history layer-demo:unoptimized
   ```

4. Refactor the Dockerfile to:
   - Combine related RUN commands using `&&`
   - Use `--no-install-recommends` flag for apt-get
   - Clean up temporary files in the same layer they were created
   - Order instructions from least to most frequently changing

5. Build your optimized version:
   ```bash
   docker build -t layer-demo:optimized .
   ```

6. Compare the results:
   ```bash
   docker history layer-demo:optimized
   docker images layer-demo:*
   ```

## Best Practices

- **Combine related commands**: Use `&&` to chain commands within a single RUN instruction
- **Clean up in same layer**: Remove files in the same instruction that created them
- **Use .dockerignore**: Prevent unnecessary files from being copied into the image
- **Order instructions properly**: Place rarely changing instructions first

## TODO

Complete the following tasks in the Dockerfile:
1. Refactor the Dockerfile to reduce the number of layers
2. Combine related commands with && to reduce layer count
3. Use --no-install-recommends when installing packages
4. Clean up temporary files in the same layer they were created
5. Order instructions from least to most frequently changing 