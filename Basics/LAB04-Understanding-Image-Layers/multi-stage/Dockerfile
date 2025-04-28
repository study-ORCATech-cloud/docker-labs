# TODO: Build stage - Create a build stage with a descriptive name
# HINT: Use a more specific name than 'builder'
FROM python:3.9 as base

# Set working directory
WORKDIR /app

# TODO: Install system dependencies efficiently
# HINT: Combine all apt-get commands into a single RUN instruction
# Current implementation (inefficient):
RUN apt-get update
RUN apt-get install -y --no-install-recommends gcc
RUN apt-get install -y --no-install-recommends g++
RUN apt-get install -y --no-install-recommends build-essential
RUN apt-get clean
RUN rm -rf /var/lib/apt/lists/*

# Copy only requirements first to leverage Docker caching
COPY requirements.txt .

# TODO: Install all Python dependencies
# HINT: Use a single pip install command with the requirements.txt file
# Current implementation (inefficient):
RUN pip install Flask==2.2.3
RUN pip install Werkzeug==2.2.3
RUN pip install numpy==1.24.3
RUN pip install pandas==2.0.0
RUN pip install matplotlib==3.7.1
RUN pip install scipy==1.10.1
RUN pip install requests==2.28.2
RUN pip install gunicorn==20.1.0

# Copy application code
COPY app.py .

# TODO: Create a runtime stage
# HINT: Use a smaller base image like python:3.9-slim
FROM python:3.9

WORKDIR /app

# TODO: Install only the runtime dependencies
# HINT: Consider which system packages are needed only for runtime vs build

# TODO: Copy installed packages from the builder stage
# HINT: Use COPY --from=builder to copy only what's needed

# TODO: Copy application code from the builder stage
# HINT: Use COPY --from=builder to copy application files

# TODO: Create any necessary directories
# HINT: mkdir any directories needed for your application

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# TODO: Set proper permissions and security
# HINT: Consider creating a non-root user and setting appropriate file permissions

# Expose port
EXPOSE 5000

# TODO: Use an efficient command to run the application
# HINT: Consider using gunicorn instead of the default Flask server
CMD ["python", "app.py"] 