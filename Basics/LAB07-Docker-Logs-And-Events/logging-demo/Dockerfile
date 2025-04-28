FROM python:3.9-slim

WORKDIR /app

# Copy the application code
COPY app.py .

# Make the script executable
RUN chmod +x app.py

# Set environment variables
ENV LOG_INTERVAL=1.0

# TODO: Run the logging demo application
# Hint: The app.py script should be executed to generate logs 