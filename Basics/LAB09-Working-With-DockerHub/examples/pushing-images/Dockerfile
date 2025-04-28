FROM python:3.9-slim

# Set working directory
WORKDIR /app

# Copy requirements and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY app.py .

# Set environment variables
ENV APP_VERSION=1.0.0
ENV PYTHON_VERSION=3.9
ENV PORT=8080

# Expose port
EXPOSE 8080

# Run the application
CMD ["python", "app.py"]

# TODO: When pushing to Docker Hub, make sure to:
#  1. Tag with your Docker Hub username
#  2. Use a proper versioning scheme
#  3. Consider adding a descriptive README to your repository 