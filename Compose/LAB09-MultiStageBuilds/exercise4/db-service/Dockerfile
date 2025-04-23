# Stage 1: Build MongoDB image with init scripts
FROM mongo:5.0 as base

# Set environment variables
ENV MONGO_INITDB_DATABASE=apidb

# Stage 2: Development stage (with additional tools)
FROM base as development

# Install additional tools for development
RUN apt-get update && apt-get install -y --no-install-recommends \
    mongodb-clients \
    && rm -rf /var/lib/apt/lists/*

# Stage 3: Production stage (minimal image)
FROM base as production

# No additional tools for production, keeping it minimal
# This leverages the base MongoDB image with only the essentials 