DOCKER VOLUMES DEMO

This file is stored in a directory that will be mounted as a Docker volume.
Any changes made to this file will persist even if the container is removed.

This demonstrates how Docker volumes provide persistent storage for containers.

Try the following:
1. Run the container with a volume mounted to this directory
2. Use the API to write data (POST to /write)
3. Stop and remove the container
4. Start a new container with the same volume
5. Use the API to read data (GET from /read)
6. Notice that the data persists across container restarts

VOLUME TYPES:
- Named volumes: Managed by Docker, great for persistent data
- Bind mounts: Link to a host directory, great for development
- tmpfs mounts: Stored in memory, great for sensitive information 