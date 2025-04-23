FROM python:3.9

# Set a working directory
WORKDIR /app

# Install system dependencies (separate layer)
RUN apt-get update
RUN apt-get install -y --no-install-recommends gcc
RUN apt-get install -y --no-install-recommends g++
RUN apt-get install -y --no-install-recommends build-essential

# Copy and install Python dependencies one by one (each as a separate layer)
COPY requirements.txt .
RUN pip install Flask==2.2.3
RUN pip install Werkzeug==2.2.3
RUN pip install numpy==1.24.3
RUN pip install pandas==2.0.0
RUN pip install matplotlib==3.7.1
RUN pip install scipy==1.10.1
RUN pip install requests==2.28.2
RUN pip install gunicorn==20.1.0

# Copy the application code (another layer)
COPY app.py .

# Create a directory for data (another layer)
RUN mkdir -p /app/data

# Set environment variables (metadata, not a layer)
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Set permissions (another layer)
RUN chmod 755 /app/app.py

# Install development packages for debugging (another layer)
RUN pip install pytest==7.3.1
RUN pip install black==23.3.0
RUN pip install flake8==6.0.0

# Expose the port (metadata, not a layer)
EXPOSE 5000

# Run the application
CMD ["python", "app.py"] 