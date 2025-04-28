# Multi-stage Builds Example

This directory demonstrates how to use multi-stage builds to create more efficient and secure Docker images.

## What are Multi-stage Builds?

Multi-stage builds allow you to:
- Use multiple FROM statements in your Dockerfile
- Selectively copy artifacts from one stage to another
- Minimize the final image size by including only what's necessary for runtime

## Project Structure

- `app.py`: A simple Flask application
- `requirements.txt`: Python dependencies
- `Dockerfile.single-stage`: A basic, unoptimized single-stage build
- `Dockerfile.multi-stage`: A template for implementing a multi-stage build

## Task: Implement a Multi-stage Build

The goal is to optimize the Docker image by:
1. Creating a build stage for installing dependencies
2. Creating a runtime stage with only the necessary components
3. Reducing the final image size
4. Improving security by running as a non-root user

## Instructions

1. Review the unoptimized `Dockerfile.single-stage`
2. Build and test it:
   ```bash
   docker build -t flask-app:single-stage -f Dockerfile.single-stage .
   docker run -p 8080:8080 flask-app:single-stage
   ```

3. Implement the multi-stage build by completing the TODOs in `Dockerfile.multi-stage`
4. Build and test your multi-stage version:
   ```bash
   docker build -t flask-app:multi-stage -f Dockerfile.multi-stage .
   docker run -p 8080:8080 flask-app:multi-stage
   ```

5. Compare the size and layer count of both images:
   ```bash
   docker images flask-app
   docker history flask-app:single-stage
   docker history flask-app:multi-stage
   ```

## TODO

Complete the following tasks:
1. Identify problems with the single-stage Dockerfile
2. Implement a solution using multi-stage builds
3. Ensure the final image is as small as possible
4. Implement security best practices 
5. Document the benefits and improvements achieved 