# Multi-Stage Build Exercise

This directory contains an example of how to implement multi-stage builds with Docker. Multi-stage builds are a powerful feature that allows you to:

- Create smaller and more secure images
- Separate build-time dependencies from runtime dependencies
- Simplify your build process

## What is a Multi-stage Build?

A multi-stage build uses multiple `FROM` statements in your Dockerfile. Each `FROM` statement begins a new build stage that can be used to:

1. Build your application with all required build tools
2. Copy only the built artifacts to a clean, minimal runtime image
3. Leave behind build tools, temporary files, and other artifacts

## The Application

This directory contains a simple Python Flask application that:
- Generates random plots with matplotlib
- Creates and manipulates dataframes with pandas
- Serves API endpoints for status and information

## Exercise Tasks

Your task is to complete the multi-stage Dockerfile by implementing the TODOs in the file. You must write the code yourself, not just copy from examples. The goal is to:

1. Create a build stage that compiles all required dependencies
2. Create a runtime stage that contains only what's needed to run the application
3. Properly copy artifacts between stages
4. Set up security best practices such as using a non-root user

## TODO Tasks

1. **Create a proper build stage**: Give your build stage a descriptive name and use an appropriate base image.

2. **Optimize system dependency installation**: Replace the inefficient multiple RUN commands with a single efficient command.

3. **Install Python dependencies efficiently**: Replace the inefficient approach with a better one using requirements.txt.

4. **Create an optimized runtime stage**: Use a smaller base image and only include runtime dependencies.

5. **Copy only necessary artifacts**: Copy only what's needed from the build stage.

6. **Implement security best practices**: Create a non-root user, set proper permissions, etc.

7. **Use an efficient command to run the application**: Choose the appropriate command for a production Flask application.

## Testing Your Implementation

After implementing your solutions, test your work:

1. Build your multi-stage image:
```bash
docker build -t multi-stage-demo:optimized .
```

2. Run the container:
```bash
docker run -d -p 5000:5000 --name multi-stage-container multi-stage-demo:optimized
```

3. Test the API:
```bash
curl http://localhost:5000/status
curl http://localhost:5000/info
```

## Image Size Comparison

After building your image, compare its size with the single-stage version:
```bash
docker images | grep demo
```

## Clean Up

Remove the container and image:
```bash
docker stop multi-stage-container
docker rm multi-stage-container
docker rmi multi-stage-demo:optimized
``` 