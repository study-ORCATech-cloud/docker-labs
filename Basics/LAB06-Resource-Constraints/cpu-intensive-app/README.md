# CPU Intensive Application

This directory contains a simple Python application designed to generate CPU load for testing Docker resource constraints.

## Files

- `cpu_load.py`: Python script that generates CPU load
- `Dockerfile`: Container definition for the CPU load testing application

## How It Works

The application spawns multiple processes that perform CPU-intensive calculations for a specified duration. This allows you to observe how Docker's CPU constraints affect the performance of the application.

## Building the Image

```bash
docker build -t cpu-demo .
```

## Running the Container

### Basic Usage

```bash
docker run --name cpu-demo cpu-demo
```

This will run the CPU load generator with default settings (1 process for 60 seconds).

### Custom Duration and Processes

```bash
docker run --name cpu-demo -e DURATION=30 -e PROCESSES=2 cpu-demo
```

### With CPU Constraints

```bash
# Limit to 0.5 CPUs
docker run --name cpu-demo-half --cpus=0.5 cpu-demo

# Limit to 1 CPU
docker run --name cpu-demo-one --cpus=1 cpu-demo

# Limit to 2 CPUs (if your host has multiple cores)
docker run --name cpu-demo-two --cpus=2 cpu-demo
```

## Exercises

1. Run the application without any CPU constraints and observe the resource usage using `docker stats`.
2. Run the application with various CPU constraints and compare the execution times.
3. Experiment with different numbers of processes and observe how they interact with the CPU constraints.
4. Modify the application to handle CPU constraints more gracefully.

## Analyzing Results

After running the application with different constraints, you can compare the execution times:

```bash
docker logs cpu-demo | grep "Total execution time"
```

The total execution time will increase as you decrease the CPU allocation. 