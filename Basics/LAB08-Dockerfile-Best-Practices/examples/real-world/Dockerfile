FROM ubuntu:20.04

# Set working directory
WORKDIR /app

# Update and install dependencies
RUN apt-get update
RUN apt-get install -y python3
RUN apt-get install -y python3-pip
RUN apt-get install -y curl
RUN apt-get install -y wget
RUN apt-get install -y vim
RUN apt-get install -y git

# Clear apt cache
RUN rm -rf /var/lib/apt/lists/*

# Copy application
COPY . /app/
COPY requirements.txt /app/

# Install Python dependencies
RUN pip3 install -r requirements.txt

# Setup environment
ENV DEBUG=False
ENV LOG_LEVEL=INFO
ENV PORT=8080
ENV API_KEY=dev-key-123
ENV REDIS_HOST=redis

# Expose port
EXPOSE 8080

# Start command
CMD ["python3", "app.py"]

# TODO: This Dockerfile has numerous issues to refactor:
# TODO: Using a heavy base image
# TODO: Running as root
# TODO: Too many RUN commands creating unnecessary layers
# TODO: App files copied before installing dependencies (breaks caching)
# TODO: No healthcheck
# TODO: No proper entrypoint script with graceful shutdown
# TODO: Installed unnecessary packages (vim, git)
# TODO: Hard-coded API key in the image
# TODO: No version pinning
# TODO: Using python directly instead of gunicorn for production 