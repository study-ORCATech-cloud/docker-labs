FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY app.py .

# Create volume mount points
VOLUME ["/app/data", "/app/web-output"]

EXPOSE 5000

CMD ["python", "app.py"] 