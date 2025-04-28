# Memory Usage Demonstration

This directory contains a Python application designed to demonstrate memory allocation and Docker memory constraints.

## Files

- `memory_load.py`: Python script that generates controlled memory load
- `Dockerfile`: Container definition for the memory load testing application

## How It Works

The application incrementally allocates memory until it reaches a specified limit. It reports memory usage statistics as it runs, allowing you to observe how Docker memory constraints affect the application.

## Building the Image

```bash
docker build -t memory-demo .
```

## Running the Container

### Basic Usage

```bash
docker run --name memory-demo memory-demo
```

This will run the memory load generator with default settings (allocate up to 512MB in 10MB increments).

### Custom Memory Settings

```bash
docker run --name memory-demo -e MAX_MEMORY=1024 -e INCREMENT=20 -e SLEEP=1 memory-demo
```

### With Memory Constraints

```bash
# Limit to 256MB
docker run --name memory-demo-256m --memory=256m memory-demo

# Limit to 512MB
docker run --name memory-demo-512m --memory=512m memory-demo

# Limit to 1GB
docker run --name memory-demo-1g --memory=1g memory-demo
```

### With OOM Killer Disabled

```bash
docker run --name memory-demo-no-oom --memory=256m --oom-kill-disable memory-demo
```

## Exercises

1. Run the application without any memory constraints and observe the resource usage using `docker stats`.
2. Run the application with various memory constraints and observe what happens when it exceeds the limit.
3. Experiment with OOM killer settings.
4. Try to modify the Dockerfile to make the application handle memory constraints more gracefully.

## Analyzing Results

After running the application with different constraints, you can examine what happened:

```bash
# Check if the container is still running or was killed
docker ps -a

# View the logs to see what happened
docker logs memory-demo-256m
```

## Monitoring Memory Usage

While the container is running, you can monitor its memory usage with:

```bash
docker stats memory-demo
``` 