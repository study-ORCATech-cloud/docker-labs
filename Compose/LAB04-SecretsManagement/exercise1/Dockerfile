FROM python:3.9-slim

WORKDIR /app

# Install dependencies
RUN pip install --no-cache-dir flask psycopg2-binary requests

# This is insecure - hardcoded credentials in Dockerfile
ENV BACKUP_DB_PASSWORD="dockerfile_hardcoded_password"
ENV BACKUP_API_KEY="dockerfile_hardcoded_api_key"

# Copy application code
COPY app.py /app/

# Expose the port the app runs on
EXPOSE 8000

# Command to run the application
CMD ["python", "app.py"] 