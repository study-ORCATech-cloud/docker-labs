FROM python:3.9-slim

WORKDIR /app

# Install dependencies
RUN pip install --no-cache-dir flask psycopg2-binary requests

# TODO: Notice the insecure practice of hardcoding secrets in Dockerfile
# HINT: This is another example of what NOT to do
ENV BACKUP_DB_PASSWORD="dockerfile_hardcoded_password"
ENV BACKUP_API_KEY="dockerfile_hardcoded_api_key"

# TODO: Observe that secrets in Dockerfiles get stored in image layers
# HINT: You can see these with 'docker history image_name'

# Copy application code
COPY app.py /app/

# Expose the port the app runs on
EXPOSE 8000

# Command to run the application
CMD ["python", "app.py"] 