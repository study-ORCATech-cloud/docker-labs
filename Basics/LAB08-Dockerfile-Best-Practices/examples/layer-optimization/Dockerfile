FROM ubuntu:20.04

# Update apt repository
RUN apt-get update

# Install Python
RUN apt-get install -y python3

# Install pip
RUN apt-get install -y python3-pip

# Install curl for health checks
RUN apt-get install -y curl

# Install Redis client
RUN pip3 install flask

# Install Flask
RUN pip3 install requests

# Install Redis client
RUN pip3 install redis

# Create app directories
RUN mkdir -p /app/data

# Create log directory
RUN mkdir -p /app/logs

# Create config directory
RUN mkdir -p /app/config

# Copy application code
COPY . /app

# Clean up temporary files in a new layer
RUN rm -rf /app/temp

# Clean up apt cache in a new layer
RUN rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app

# Expose the application port
EXPOSE 8080

# Command to run the application
CMD ["python3", "app.py"]

# TODO: Refactor this Dockerfile to reduce the number of layers
# TODO: Combine related commands with && to reduce layer count
# TODO: Use --no-install-recommends when installing packages
# TODO: Clean up temporary files in the same layer they were created
# TODO: Order instructions from least to most frequently changing 