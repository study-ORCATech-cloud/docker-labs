# Stage 1: Base Python image with dependencies
FROM python:3.9-slim as base

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1

WORKDIR /app

# Copy and install requirements
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Stage 2: Development stage
FROM base as development

# Install development tools
RUN pip install --no-cache-dir pytest flask-testing watchdog

# Set development environment
ENV DEBUG=true

# Copy application code
COPY ./app /app

# Command to run the application in development mode
CMD ["python", "app.py"]

# Stage 3: Production stage
FROM base as production

# Copy only the application code
COPY ./app /app

# Run the application with gunicorn
CMD ["gunicorn", "--bind", "0.0.0.0:8080", "app:app"] 