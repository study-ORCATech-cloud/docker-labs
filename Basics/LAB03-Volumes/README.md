# LAB03: Working with Docker Volumes

This lab explores how to use Docker volumes to manage data persistence, share data between containers, and between host and container.

## Lab Overview

In this lab, you will:
- Understand the difference between bind mounts, volumes, and tmpfs
- Create and use named volumes in Docker
- Share data between host and containers
- Mount host directories into containers (bind mounts)
- Manage volume lifecycle (create, list, remove)

## Learning Objectives

- Learn how to persist container data with Docker volumes
- Understand when to use bind mounts vs. named volumes vs. tmpfs
- Practice mounting host directories for development
- Manage Docker volumes from the CLI

## Prerequisites

- Docker Engine installed
- Completion of LAB01-GettingStarted and LAB02-BuildingImages

## Lab Project

This lab includes a demo project, **volume-demo**, which illustrates basic volume usage.

Directory structure:
```
LAB03-Volumes/
└── volume-demo/
    ├── Dockerfile
    ├── app.py
    ├── requirements.txt
    └── data/
        └── README.txt
```

## Lab Tasks

### Task 1: Explore Volume Types

1. **Bind Mount** - Mount a host directory into a container:
   ```bash
   docker run -d \
     --name bind-demo \
     -v $(pwd)/volume-demo/data:/app/data \
     python:3.9-slim sleep infinity
   ```

2. **Named Volume** - Create and use a named volume:
   ```bash
   docker volume create demo-volume
   docker run -d \
     --name volume-demo \
     -v demo-volume:/app/data \
     python:3.9-slim sleep infinity
   ```

3. **Tmpfs** - Use tmpfs for in-memory storage:
   ```bash
   docker run -d \
     --name tmpfs-demo \
     --tmpfs /app/data \
     python:3.9-slim sleep infinity
   ```

### Task 2: Inspect and Manage Volumes

List volumes:
```bash
docker volume ls
```

Inspect a volume:
```bash
docker volume inspect demo-volume
```

Remove containers and volumes:
```bash
docker rm -f bind-demo volume-demo tmpfs-demo
docker volume rm demo-volume
```

### Task 3: Demo Application with Persistent Data

Let's build an application that writes and reads persistent data.

#### 3.1 Create the application

`app.py`:
```python
from flask import Flask, request, jsonify
import os

app = Flask(__name__)
DATA_DIR = '/app/data'
if not os.path.exists(DATA_DIR):
    os.makedirs(DATA_DIR)

@app.route('/write', methods=['POST'])
def write_data():
    content = request.json.get('content')
    with open(os.path.join(DATA_DIR, 'message.txt'), 'w') as f:
        f.write(content)
    return jsonify({'status': 'written', 'content': content})

@app.route('/read')
def read_data():
    try:
        with open(os.path.join(DATA_DIR, 'message.txt'), 'r') as f:
            content = f.read()
        return jsonify({'status': 'read', 'content': content})
    except FileNotFoundError:
        return jsonify({'status': 'error', 'message': 'No data found'}), 404

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
```

#### 3.2 Add requirements

`requirements.txt`:
```
flask==2.2.3
```

#### 3.3 Create the Dockerfile

```dockerfile
FROM python:3.9-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY app.py .
VOLUME ["/app/data"]
EXPOSE 5000
CMD ["python", "app.py"]
```

#### 3.4 Add initial data

Create `data/README.txt` with instructions or initial content.

### Task 4: Run the Demo

Build and run with a named volume:
```bash
cd volume-demo
docker build -t volume-demo:1.0 .
docker run -d \
  --name volume-demo-app \
  -v demo-data:/app/data \
  -p 5000:5000 \
  volume-demo:1.0
```

Test the endpoints:
```bash
# Write data
curl -X POST -H "Content-Type: application/json" \
  -d '{"content": "Hello, Volumes!"}' \
  http://localhost:5000/write

# Read data
curl http://localhost:5000/read
```


Test write/read endpoints as above.

## Clean Up

```bash
docker rm -f volume-demo-app
docker volume rm demo-data
```

## Real-World Applications

Using volumes is essential for stateful applications, databases, and sharing configuration or data between containers.

## Next Steps

Proceed to LAB04-Layers to learn about Docker image layers and optimization. 