FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
RUN pip install netifaces

# Add networking tools for demonstration
RUN apt-get update && apt-get install -y --no-install-recommends \
    iputils-ping \
    net-tools \
    traceroute \
    dnsutils \
    curl \
    && rm -rf /var/lib/apt/lists/*

COPY . .

EXPOSE 8080

CMD ["python", "app.py"] 