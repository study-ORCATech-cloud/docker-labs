FROM python:3.9-slim

WORKDIR /app

# Copy the Python script
COPY cpu_load.py .

# Make the script executable
RUN chmod +x cpu_load.py

# Set default arguments (can be overridden at runtime)
ENV DURATION=60
ENV PROCESSES=1

# TODO: Run the CPU load generator script
# Hint: Use the DURATION and PROCESSES environment variables with the cpu_load.py script
# The script accepts --duration and --processes arguments 