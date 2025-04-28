FROM python:3.9

WORKDIR /app

# Copy everything at once - not optimal for CI/CD caching
COPY . .

# Install dependencies without caching
RUN pip install -r requirements.txt

# Set environment variables
ENV APP_VERSION=1.0.0
ENV ENVIRONMENT=production

# Expose port
EXPOSE 8080

# Start application
CMD ["gunicorn", "--bind", "0.0.0.0:8080", "app:app"]

# TODO: This Dockerfile has issues for CI/CD environments:
# TODO: Poor caching of dependencies
# TODO: No separation of build and runtime environments
# TODO: No consideration for CI/CD specific optimizations
# TODO: No build arguments for dynamic values
# TODO: Does not implement layer caching effectively 