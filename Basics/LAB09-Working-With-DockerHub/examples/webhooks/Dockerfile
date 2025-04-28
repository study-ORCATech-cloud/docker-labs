FROM python:3.9-slim

WORKDIR /app

# Copy requirements first for better layer caching
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY webhook_receiver.py .

# Create directory for webhook data
RUN mkdir -p webhook_data && chmod 777 webhook_data

# Set environment variables
ENV PORT=5000 \
    PYTHONUNBUFFERED=1

# Expose the port
EXPOSE 5000

# Run the application
CMD ["python", "webhook_receiver.py"]