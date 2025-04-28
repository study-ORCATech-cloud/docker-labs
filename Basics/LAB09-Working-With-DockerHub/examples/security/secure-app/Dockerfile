FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Create a non-root user to run the application
RUN groupadd -r appuser && \
    useradd -r -g appuser -d /app -s /sbin/nologin -c "Docker image user" appuser

# Install only what's needed
RUN apt-get update && \
    apt-get install -y --no-install-recommends sqlite3 curl && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Copy requirements first to leverage build cache
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Create a data directory owned by the appuser
RUN mkdir -p /data && \
    chown -R appuser:appuser /data && \
    chmod 700 /data

# Copy application files
COPY --chown=appuser:appuser app.py .
COPY --chown=appuser:appuser templates ./templates

# Set secure environment variables
ENV DEBUG=false \
    PORT=8080 \
    DB_FILE=/data/app.db \
    PYTHONUNBUFFERED=1

# Expose application port
EXPOSE 8080

# Switch to non-root user
USER appuser

# Set health check
HEALTHCHECK --interval=30s --timeout=5s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:8080/ || exit 1

# Start the application
CMD ["python", "app.py"] 