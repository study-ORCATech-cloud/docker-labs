FROM python:3.9-slim

# Build arguments
ARG GIT_COMMIT=unknown
ARG BUILD_DATE=unknown
ARG APP_VERSION=1.0.0

# Set environment variables
ENV GIT_COMMIT=$GIT_COMMIT \
    BUILD_DATE=$BUILD_DATE \
    APP_VERSION=$APP_VERSION \
    PYTHONUNBUFFERED=1

# Set working directory
WORKDIR /app

# Copy requirements and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY app.py .

# Expose port
EXPOSE 8080

# Set image metadata
LABEL org.opencontainers.image.created=$BUILD_DATE \
    org.opencontainers.image.revision=$GIT_COMMIT \
    org.opencontainers.image.version=$APP_VERSION \
    org.opencontainers.image.title="AutoBuild Demo" \
    org.opencontainers.image.description="Sample application for Docker Hub automated builds" \
    org.opencontainers.image.source="https://github.com/yourusername/repo"

# Run the application
CMD ["python", "app.py"] 