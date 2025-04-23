# Volume Demo Application

This application demonstrates Docker volume concepts using a simple Flask API that reads and writes data to a persistent volume.

## Application Structure

- `app.py` - Flask application with read/write endpoints
- `Dockerfile` - Container definition with a volume declaration
- `data/` - Directory that will be mounted as a volume

## Running the Application

### Option 1: Using a Named Volume

```bash
# Build the image
docker build -t volume-demo:1.0 .

# Create a named volume
docker volume create demo-data

# Run the container with the volume
docker run -d \
  --name volume-demo-app \
  -v demo-data:/app/data \
  -p 5000:5000 \
  volume-demo:1.0
```

### Option 2: Using a Bind Mount

```bash
# Build the image
docker build -t volume-demo:1.0 .

# Run the container with the host directory mounted
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
5. Notice the data has persisted!

## Cleaning Up

```bash
docker stop volume-demo-app
docker rm volume-demo-app
docker volume rm demo-data
``` 