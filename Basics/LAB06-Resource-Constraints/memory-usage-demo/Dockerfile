FROM python:3.9-slim

WORKDIR /app

# Copy script
COPY memory_load.py .

# Install dependencies
RUN pip install psutil

# Make script executable
RUN chmod +x memory_load.py

# Set default arguments (can be overridden at runtime)
ENV MAX_MEMORY=512
ENV INCREMENT=10
ENV SLEEP=0.5

# TODO: Run the memory load generator script
# Hint: Use the MAX_MEMORY, INCREMENT, and SLEEP environment variables with the memory_load.py script
# The script accepts --max-memory, --increment, and --sleep arguments 