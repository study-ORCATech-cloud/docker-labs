# Simple Flask Application

This is a basic Flask web application designed to demonstrate simple Docker containerization concepts.

## Features

- Basic web interface that confirms the app is running
- Health check endpoint
- Containerized using Docker

## Implementation TODOs

To complete this project, you'll need to:

1. **Complete the Dockerfile**: 
   - Open the `Dockerfile` in this directory and implement all the TODO sections
   - Choose an appropriate base image
   - Set up the working directory
   - Install dependencies
   - Copy the application code
   - Configure the port and runtime command

2. **Enhance the Flask application**:
   - Implement the TODO in `app.py` to add a hostname endpoint
   - The endpoint should return the container hostname

## Docker Commands

Once you've implemented the TODOs, build and run the application:

```bash
# Build the image
docker build -t simple-flask-app:1.0 .

# Run the container
docker run -d -p 5000:5000 --name flask-demo simple-flask-app:1.0

# Test the application
curl http://localhost:5000
curl http://localhost:5000/health
curl http://localhost:5000/hostname  # After you implement this endpoint
```

## Expected Dockerfile Structure

Your completed Dockerfile should follow this structure:
1. Specify a base image
2. Set a working directory
3. Copy and install dependencies
4. Copy application code
5. Expose the port
6. Set the command

## Extension Tasks

After completing the basic TODOs, try these additional improvements:

1. Modify the Dockerfile to use Alpine instead of slim for a smaller image
2. Add a HEALTHCHECK instruction to the Dockerfile
3. Compare the image sizes between different base images
4. Add environment variables to configure the application 