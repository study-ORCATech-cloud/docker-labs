# Logging Demo Application

This directory contains a Python application designed to demonstrate Docker's logging capabilities.

## Files

- `app.py`: Python script that generates various types of logs
- `Dockerfile`: Container definition for the logging demo application

## How It Works

The application simulates a real-world service by generating different types of log messages:
- ERROR: Critical issues that need immediate attention
- WARNING: Potential issues that may need attention
- INFO: Normal operational information
- DEBUG: Detailed information for troubleshooting

The application also simulates error scenarios and periodic log bursts to provide realistic log patterns.

## Building the Image

```bash
docker build -t logging-demo .
```

## Running the Container

### Basic Usage

```bash
docker run --name logging-app logging-demo
```

### Customizing Log Interval

You can control the rate at which logs are generated:

```bash
docker run --name logging-app -e LOG_INTERVAL=0.5 logging-demo
```

## Exercises

1. View the logs in real-time using Docker's log commands:
   ```bash
   docker logs -f logging-app
   ```

2. Filter logs by error level using grep:
   ```bash
   docker logs logging-app | grep ERROR
   ```

3. Extract timing information from the logs:
   ```bash
   docker logs logging-app | grep "processing time" | awk '{print $NF}'
   ```

4. Count occurrences of different log levels:
   ```bash
   docker logs logging-app | grep -c ERROR
   docker logs logging-app | grep -c WARNING
   docker logs logging-app | grep -c INFO
   ```

5. Modify the Dockerfile to implement log rotation using Docker's built-in options.

## Using Different Logging Drivers

Try running the container with different logging drivers:

```bash
# Using JSON-file with size limits
docker run --name logging-app --log-driver json-file --log-opt max-size=10m --log-opt max-file=3 logging-demo

# Using syslog
docker run --name logging-app --log-driver syslog logging-demo

# Using local logging driver
docker run --name logging-app --log-driver local --log-opt max-size=10m --log-opt max-file=3 logging-demo
```

## Analyzing the Logs

The log messages follow patterns that can be analyzed to understand application behavior:

- Database connection issues
- API dependency problems
- Resource usage patterns
- Performance metrics (processing times)
- Authentication events
- Request patterns and bursts

Try to extract meaningful insights from the logs using command-line tools. 