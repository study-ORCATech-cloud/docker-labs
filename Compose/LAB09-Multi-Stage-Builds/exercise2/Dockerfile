###############################################
# STAGE 1: Base dependencies
###############################################
FROM python:3.11-slim AS base

# Create a non-root user
RUN useradd -m appuser

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1 \
    PYTHONPATH=/app

# Create and set working directory
WORKDIR /app

###############################################
# STAGE 2: Builder - Production dependencies
###############################################
FROM base AS builder-prod

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

# Install production dependencies
RUN pip install --no-cache-dir -r requirements.txt

###############################################
# STAGE 3: Builder - Development dependencies
###############################################
FROM builder-prod AS builder-dev

# Copy development requirements
COPY app/requirements-dev.txt .

# Install development dependencies
RUN pip install --no-cache-dir -r requirements-dev.txt

###############################################
# STAGE 4: Development runtime
###############################################
FROM base AS development

# Install curl for health check and other useful tools
RUN apt-get update && apt-get install -y \
    curl \
    vim \
    && rm -rf /var/lib/apt/lists/*

# Copy virtual environment from development builder
COPY --from=builder-dev /opt/venv /opt/venv

# Set environment variables
ENV PATH="/opt/venv/bin:$PATH" \
    BUILD_ENV=development \
    FLASK_ENV=development \
    FLASK_DEBUG=1

# Copy application code
COPY app/ .

# Expose port
EXPOSE 8000

# Health check
HEALTHCHECK --interval=30s --timeout=3s --start-period=5s --retries=3 \
  CMD curl -f http://localhost:8000/health || exit 1

# Switch to non-root user
USER appuser

# Command to run the application
CMD ["python", "app.py"]

###############################################
# STAGE 5: Production runtime
###############################################
FROM base AS production

# Install only the required runtime dependencies
RUN apt-get update && apt-get install -y \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Copy virtual environment from production builder
COPY --from=builder-prod /opt/venv /opt/venv

# Set environment variables
ENV PATH="/opt/venv/bin:$PATH" \
    BUILD_ENV=production \
    FLASK_ENV=production \
    FLASK_DEBUG=0

# Copy application code
COPY app/ .

# Expose port
EXPOSE 8000

# Health check
HEALTHCHECK --interval=30s --timeout=3s --start-period=5s --retries=3 \
  CMD curl -f http://localhost:8000/health || exit 1

# Switch to non-root user
USER appuser

# Command to run the application with gunicorn
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "--workers", "2", "app:app"] 