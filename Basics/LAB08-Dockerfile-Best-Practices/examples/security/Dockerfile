FROM python:3.9

# Set working directory
WORKDIR /app

# Install dependencies (without pinned versions)
COPY requirements.txt .
RUN pip install -r requirements.txt

# Copy application code
COPY . .

# Expose application port
EXPOSE 8080

# Run the application with root user (security issue)
CMD ["python", "app.py"]

# Security issues in this Dockerfile:
# TODO: The base image tag is not specific (should use a specific version)
# TODO: Running as root user (should create and use a non-root user)
# TODO: No healthcheck defined (add a HEALTHCHECK instruction)
# TODO: Using default exposed port (consider using a non-standard port)
# TODO: No verification of downloaded packages (consider adding integrity checks)
# TODO: Debug mode enabled in the application
# TODO: Sensitive data potentially exposed in the image 