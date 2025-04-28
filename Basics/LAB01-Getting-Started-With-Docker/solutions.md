# LAB01: Getting Started with Docker - Solutions

This document contains solutions to the TODO exercises in LAB01. Use these solutions only after attempting to solve the problems yourself.

## Code Implementation Solutions

### Dockerfile Solution

```dockerfile
# Base Dockerfile for the Flask application
FROM python:3.9-slim

# Set the working directory inside the container
WORKDIR /app

# Copy and install requirements first (for better caching)
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the application code into the container
COPY . .

# Expose the port the app runs on
EXPOSE 80

# Command to run the application
CMD ["python", "app.py"]
```

### app.py Container ID Implementation Solution

In the `container_info()` function, replace the TODO with:

```python
# Extract container ID from cgroup file
result = subprocess.run(
    ["cat /proc/self/cgroup | grep -o -E '([0-9a-f]{64})' | head -n 1"],
    shell=True, 
    capture_output=True, 
    text=True
)
container_id = result.stdout.strip()
if container_id:
    info += f"Container ID: {container_id[:12]}"
else:
    info += "Container ID: Not running in Docker"
```

### app.py Environment Variables Route Solution

Add this route to display environment variables:

```python
@app.route('/env-vars')
def env_vars():
    env_list = []
    
    # Get important Docker-related environment variables
    env_vars = {
        'HOME': os.environ.get('HOME', 'Not set'),
        'HOSTNAME': os.environ.get('HOSTNAME', 'Not set'),
        'PATH': os.environ.get('PATH', 'Not set'),
        'PYTHON_VERSION': os.environ.get('PYTHON_VERSION', 'Not set'),
        'PYTHONPATH': os.environ.get('PYTHONPATH', 'Not set')
    }
    
    for key, value in env_vars.items():
        env_list.append(f"{key}: {value}")
    
    return "<h1>Environment Variables</h1><pre>" + "\n".join(env_list) + "</pre>"
```

## TODO Exercise Solutions

### TODO 1: Pull and Run a Redis Container

```bash
# Pull the Redis image
docker pull redis:latest

# Run Redis container in detached mode
docker run -d --name my-redis redis:latest

# Verify it's running
docker ps

# Get logs
docker logs my-redis

# Stop the container
docker stop my-redis

# Remove the container
docker rm my-redis
```

### TODO 2: Create and Manage an Alpine Container

```bash
# Create an Alpine container with interactive shell
docker run -it --name alpine-test alpine sh

# Inside the container, create the file
echo "Hello from Docker!" > /tmp/hello.txt
cat /tmp/hello.txt
exit

# Start the container again
docker start -i alpine-test

# Verify the file exists
cat /tmp/hello.txt

# Exit and remove the container
exit
docker rm alpine-test
```

Note: Alpine uses `sh` instead of `bash` by default. If you need `bash`, you would need to install it first with `apk add bash`.

### TODO 3: Container Resource Limits

```bash
# Run Nginx with resource limits
docker run -d --name limited-nginx --memory=200m --cpus=0.5 -p 8888:80 nginx

# Verify it's running with the resource limits
docker inspect limited-nginx | grep -A 10 "HostConfig"

# Access in browser: http://localhost:8888

# Stop and remove
docker stop limited-nginx
docker rm limited-nginx
```

### TODO 4: Running Multiple Containers

```bash
# Run the three containers
docker run -d -p 8081:80 --name apache httpd
docker run -d -p 8082:80 --name nginx nginx
docker run -d -p 8083:80 --name pyserver python:3.9-alpine python -m http.server 80

# Verify all three are running
docker ps

# List only container IDs
docker ps -q

# Stop all containers
docker stop $(docker ps -q)

# Remove all containers
docker rm $(docker ps -a -q)
```

## Additional Tips

1. To check Docker resource usage:
```bash
docker stats
```

2. To save container output to a file:
```bash
docker logs my-container > container_logs.txt
```

3. To copy files between host and container:
```bash
# From host to container
docker cp file.txt container-name:/path/in/container/

# From container to host
docker cp container-name:/path/in/container/file.txt ./
```

4. To view container details:
```bash
docker inspect container-name
```

5. Modified run-demo command with environment variables and volume:
```bash
mkdir -p data
docker run --rm -it -p 8080:80 -e DEMO_VAR="Hello Student" -v $(pwd)/data:/app/data --name docker-lab-py docker-getting-started-py
``` 