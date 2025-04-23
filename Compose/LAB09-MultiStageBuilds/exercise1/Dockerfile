###############################################
# STAGE 1: Build dependencies stage
###############################################
FROM python:3.11-slim AS builder

# Set working directory
WORKDIR /app

# Install build dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements file
COPY app/requirements.txt .

# Create a virtual environment and install dependencies
RUN python -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

# Install requirements in the virtual environment
RUN pip install --no-cache-dir -r requirements.txt


###############################################
# STAGE 2: Runtime stage
###############################################
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Copy virtual environment from builder stage
COPY --from=builder /opt/venv /opt/venv

# Make sure we use the virtual environment
ENV PATH="/opt/venv/bin:$PATH"
ENV BUILD_TYPE=multistage

# Install only the runtime dependencies - curl for healthcheck
RUN apt-get update && apt-get install -y \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Copy application code
COPY app/ .

# Expose port
EXPOSE 8000

# Health check
HEALTHCHECK --interval=30s --timeout=3s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:8000/health || exit 1

# Run as non-root user
RUN useradd -m appuser
USER appuser

# Command to run the application
CMD ["python", "app.py"] 