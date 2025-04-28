# Single-Stage Build Exercise

This directory contains a Flask application with an unoptimized Dockerfile that creates many unnecessary layers. Your task is to optimize it by reducing the number of layers and improving the overall Docker image efficiency.

## The Application

This is a simple Python Flask application that:
- Generates random plots using matplotlib
- Creates dataframes using pandas
- Provides API endpoints for status and information

## The Problem

The provided Dockerfile has several inefficiencies:

1. **Too many layers**: Each RUN command creates a separate layer, increasing the image size
2. **Inefficient dependency installation**: Dependencies are installed one by one
3. **Development dependencies**: Production image includes development-only packages
4. **No cleanup**: Temporary files and build tools are not removed properly

## Exercise Tasks

Your task is to optimize the Dockerfile by implementing solutions for each of the TODOs in the file. You must write the code yourself - do not simply copy solutions from elsewhere. The goal is to:

1. Reduce the number of layers
2. Combine related operations
3. Efficiently install dependencies
4. Clean up temporary files
5. Use proper commands for running the application

## TODO Tasks

1. **Install system dependencies efficiently**: 
   - Replace the multiple RUN commands with a single, efficient RUN instruction
   - Include proper cleanup in the same instruction

2. **Install Python dependencies efficiently**: 
   - Implement a better approach using requirements.txt
   - Use appropriate flags for optimization

3. **Optimize directory creation and permissions**:
   - Implement a solution that combines these operations into a single layer

4. **Handle development packages appropriately**:
   - Consider if and how these should be included in a production image
   - Implement an appropriate solution

5. **Use an efficient application server**:
   - Implement a production-ready solution for running the Flask application

## Testing Your Implementation

After implementing your optimizations, test your work:

1. Build the optimized image:
```bash
docker build -t single-stage-demo:optimized .
```

2. Run a container:
```bash
docker run -d -p 5000:5000 --name single-stage-container single-stage-demo:optimized
```

3. Test the API:
```bash
curl http://localhost:5000/status
curl http://localhost:5000/info
```

## Analyzing Image Layers

After building your image, analyze the layers to see the improvements:

```bash
docker history single-stage-demo:optimized
```

Compare it with the unoptimized version (if you build that first):

```bash
docker history single-stage-demo:unoptimized
```

## Clean Up

Remove the container and image:

```bash
docker stop single-stage-container
docker rm single-stage-container
docker rmi single-stage-demo:optimized
``` 