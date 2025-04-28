FROM python:3.9-slim

WORKDIR /app

# Install dependencies
COPY ./app/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application files
COPY ./app .

# Create a directory for Docker secrets
RUN mkdir -p /run/secrets

EXPOSE 8080

CMD ["python", "app.py"] 