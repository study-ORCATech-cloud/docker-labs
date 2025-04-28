# Volume Demo Application

This application demonstrates Docker volume concepts using a simple Flask API that reads and writes data to a persistent volume.

## Implementation TODOs

To complete this demo, you'll need to:

1. **Complete the Dockerfile**:
   - Implement all the TODO sections in the Dockerfile
   - Set up the proper base image, working directory, and volume configuration

2. **Understand the existing code**:
   - Examine app.py to understand how it uses the /app/data directory
   - Note how the application writes and reads files from this directory

3. **Implement volume strategies**:
   - Try both named volumes and bind mounts
   - Compare the differences between these approaches

## Application Structure

- `app.py` - Flask application with read/write endpoints
- `Dockerfile` - Container definition with volume-related TODOs
- `data/` - Directory that will be mounted as a volume
- `requirements.txt` - Python dependencies for the application

## Docker Commands

After completing the Dockerfile TODOs, build and run the application:

### Option 1: Using a Named Volume (Recommended First)

```bash
# TODO: Build the image with an appropriate tag
docker build -t volume-demo:1.0 .

# TODO: Create a named volume
docker volume create demo-data

# TODO: Run the container with the volume mounted to /app/data
docker run -d \
  --name volume-demo-app \
  -v demo-data:/app/data \
  -p 5000:5000 \
  volume-demo:1.0
```

### Option 2: Using a Bind Mount (For Development)

```bash
# TODO: Build the image with an appropriate tag
docker build -t volume-demo:1.0 .

# TODO: Run the container with the host directory mounted to /app/data
docker run -d \
  --name volume-demo-app \
  -v "$(pwd)/data:/app/data" \
  -p 5000:5000 \
  volume-demo:1.0
```

## Testing the Application

### Using the Web Interface

Open a browser and navigate to: http://localhost:5000

### Using API Endpoints

Write data:
```bash
curl -X POST -H "Content-Type: application/json" \
  -d '{"content": "Hello, Volumes!"}' \
  http://localhost:5000/write
```

Read data:
```bash
curl http://localhost:5000/read
```

## Demonstrating Data Persistence

Follow these steps to verify data persistence:

1. Write data using the API
2. Stop and remove the container (but keep the volume):
   ```bash
   docker stop volume-demo-app
   docker rm volume-demo-app
   ```
3. Start a new container using the same volume:
   ```bash
   docker run -d \
     --name volume-demo-app-new \
     -v demo-data:/app/data \
     -p 5000:5000 \
     volume-demo:1.0
   ```
4. Read the data using the API
5. Verify the data has persisted!

## Extension Tasks

After completing the basic TODOs, try these additional improvements:

1. Modify the Dockerfile to use a non-root user for better security
2. Add a second volume for logs, and update the application to write logs there
3. Create a script to backup your named volume to a tar file

## Cleaning Up

```bash
docker stop volume-demo-app-new
docker rm volume-demo-app-new
docker volume rm demo-data
``` 