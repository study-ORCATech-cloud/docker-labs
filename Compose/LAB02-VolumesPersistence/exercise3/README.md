# Exercise 3: Sharing Data Between Services

This exercise demonstrates how to use volumes to share data between multiple containerized services.

## Overview

In this exercise, you'll create a data processing pipeline with two services:
1. **Producer**: Generates random data and writes it to a shared volume
2. **Consumer**: Reads the data from the shared volume (read-only) and processes it

This pattern is common in microservices architectures where services need to share data without direct communication.

## Files

- `/producer/`: Data generation service
  - `Dockerfile`: Container definition
  - `producer.py`: Python script that generates random data
  - `requirements.txt`: Python dependencies
  
- `/consumer/`: Data processing service
  - `Dockerfile`: Container definition
  - `consumer.py`: Python script that processes data and creates visualizations
  - `requirements.txt`: Python dependencies

## Instructions

### Step 1: Start the Data Pipeline

```bash
# Start both the producer and consumer services
docker-compose up -d data-producer data-consumer

# Check both services are running
docker-compose ps
```

### Step 2: Observe Data Sharing

```bash
# View logs from the producer
docker-compose logs data-producer

# View logs from the consumer
docker-compose logs data-consumer
```

### Step 3: Inspect the Shared Volume

```bash
# List the contents of the shared volume
docker-compose exec data-consumer ls -la /shared-data

# View a data file
docker-compose exec data-consumer cat /shared-data/data_1.csv

# View a metadata file
docker-compose exec data-consumer cat /shared-data/metadata_1.json

# View the results directory
docker-compose exec data-consumer ls -la /shared-data/results
```

### Step 4: Understand Read-Only Mounts

The consumer service has a read-only mount to the shared volume, which provides an extra layer of security:

```bash
# Try to write to the shared volume from the consumer (will fail)
docker-compose exec data-consumer touch /shared-data/test_file.txt
```

The command should fail with a "Read-only file system" error.

### Step 5: Cleanup

When you're finished with this exercise, clean up the resources:

```bash
# Stop the containers
docker-compose stop data-producer data-consumer

# Remove the containers
docker-compose rm -f data-producer data-consumer

# If you want to remove the shared volume and delete all data permanently
# docker volume rm lab02_shared_data
```

## How Shared Volumes Work

1. A named volume `shared_data` is created
2. The producer mounts this volume with read-write access
3. The consumer mounts the same volume with read-only access (`:ro` flag)
4. Data written by the producer is instantly available to the consumer
5. The consumer cannot modify or delete files in the shared volume

## Expected Results

- The producer will periodically generate CSV data files and metadata
- The consumer will detect new files and process them
- Processed results (summaries and visualizations) will be saved back to a subdirectory
- The consumer will keep a log of processed files to avoid reprocessing

## Key Learning Points

- Volumes can be shared between multiple containers
- Read-only mounts provide security by preventing modification
- Shared volumes allow for a simple data exchange mechanism
- No direct network communication is needed between the services 