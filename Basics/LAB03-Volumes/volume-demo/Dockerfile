FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY app.py .

# Declare a volume for persistent data
VOLUME ["/app/data"]

EXPOSE 5000

CMD ["python", "app.py"] 