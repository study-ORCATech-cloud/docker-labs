# Stage 1: Base Python with common dependencies
FROM python:3.9-slim as base

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1

WORKDIR /app

# Copy requirements files
COPY app/requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Stage 2: Development environment
FROM base as development

# Copy dev requirements
COPY app/requirements-dev.txt .

# Install dev dependencies
RUN pip install --no-cache-dir -r requirements-dev.txt

# Set development environment
ENV FLASK_ENV=development \
    DEBUG=true

# Copy application code
COPY app/ .

# Command for development
CMD ["python", "app.py"]

# Stage 3: Testing stage
FROM development as testing

# Run tests
CMD ["pytest"]

# Stage 4: Asset optimization
FROM node:14-alpine as asset-builder

WORKDIR /build

# Copy static assets for processing
COPY app/static /build/static

# Install node dependencies for asset optimization
RUN npm install -g clean-css-cli terser

# Minify CSS files
RUN find /build/static/css -name "*.css" -exec sh -c 'cleancss -o "${1%.css}.min.css" "$1"' _ {} \;

# Stage 5: Production image
FROM base as production

# Set production environment
ENV FLASK_ENV=production \
    DEBUG=false

# Copy application code excluding development files
COPY app/ .

# Copy optimized assets from asset-builder stage
COPY --from=asset-builder /build/static/css/*.min.css /app/static/css/

# Run with gunicorn
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "app:app"] 