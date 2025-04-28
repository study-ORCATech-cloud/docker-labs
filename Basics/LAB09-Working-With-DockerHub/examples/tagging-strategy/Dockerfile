FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY app.py .

# Default environment variables
ENV APP_VERSION="1.0.0" \
    APP_ENV="production"

EXPOSE 8080

CMD ["python", "app.py"] 