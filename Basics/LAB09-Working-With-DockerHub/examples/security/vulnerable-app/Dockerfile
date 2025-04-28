FROM ubuntu:18.04

# Install system dependencies without cleanup
RUN apt-get update && \
    apt-get install -y python3 python3-pip python3-dev sqlite3 curl

# Set working directory
WORKDIR /app

# Copy application files
COPY . .

# Install Python dependencies
RUN pip3 install -r requirements.txt

# Create a database directory with insecure permissions
RUN mkdir -p /data && \
    chmod 777 /data

# Environment variable with hardcoded secret
ENV API_KEY="super-secret-api-key-1234" \
    DEBUG=true

# Expose application port
EXPOSE 8080

# Run as root (insecure)
# Missing USER instruction

# Start the application
CMD ["python3", "app.py"] 