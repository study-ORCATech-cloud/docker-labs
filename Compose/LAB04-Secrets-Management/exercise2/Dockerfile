FROM python:3.9-slim

WORKDIR /app

# Install dependencies - minimal set for the app
RUN pip install --no-cache-dir flask psycopg2-binary requests

# Copy application code
COPY app.py /app/

# TODO: Notice no secrets are hardcoded in this Dockerfile
# HINT: All secrets will be read from mounted files at runtime

# Create a non-root user for security
RUN groupadd -g 1000 appuser && \
    useradd -u 1000 -g appuser -s /bin/bash -m appuser && \
    chown -R appuser:appuser /app

# Switch to non-root user
USER appuser

# Expose the port the app runs on
EXPOSE 8000

# Command to run the application
CMD ["python", "app.py"] 