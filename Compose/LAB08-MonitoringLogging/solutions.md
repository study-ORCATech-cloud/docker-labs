# LAB08: Monitoring and Logging - Solutions

This document provides solutions and explanations for LAB08, focusing on setting up monitoring and logging using Docker Compose.

## Part 1: Basic Monitoring Setup

### 1.1 Docker Compose Configuration

The `docker-compose.yml` file sets up basic monitoring services:

```yaml
version: '3.8'

services:
  exercise1-app:
    build: ./exercise1/app
    ports:
      - "8081:8080"
    networks:
      - monitoring-net

networks:
  monitoring-net:
    driver: bridge
```

Key points:
- Building the app service from the `exercise1/app` directory
- Mapping port 8081 to container port 8080
- Connecting to the `monitoring-net` network

### 1.2 Starting the Services

Start the services with:

```bash
docker-compose up -d
```

This launches the services in detached mode.

## Part 2: Advanced Monitoring with Prometheus and Grafana

### 2.1 Prometheus Configuration

Configure Prometheus to scrape metrics:

```yaml
prometheus:
  image: prom/prometheus:v2.45.0
  ports:
    - "9090:9090"
  volumes:
    - ./prometheus/prometheus.yml:/etc/prometheus/prometheus.yml
    - prometheus_data:/prometheus
  networks:
    - monitoring-net
```

### 2.2 Grafana Configuration

Configure Grafana for visualization:

```yaml
grafana:
  image: grafana/grafana:10.0.3
  ports:
    - "3000:3000"
  environment:
    - GF_SECURITY_ADMIN_PASSWORD=admin
    - GF_USERS_ALLOW_SIGN_UP=false
  volumes:
    - grafana_data:/var/lib/grafana
    - ./grafana:/etc/grafana
  networks:
    - monitoring-net
  depends_on:
    - prometheus
```

### 2.3 Starting Prometheus and Grafana

Start the monitoring stack with:

```bash
docker-compose up -d prometheus grafana
```

Access Prometheus at `http://localhost:9090` and Grafana at `http://localhost:3000`.

## Part 3: Centralized Logging with ELK Stack

### 3.1 Elasticsearch Configuration

Configure Elasticsearch for log storage:

```yaml
elasticsearch:
  image: docker.elastic.co/elasticsearch/elasticsearch:7.17.9
  ports:
    - "9200:9200"
    - "9300:9300"
  environment:
    - discovery.type=single-node
    - ES_JAVA_OPTS=-Xms512m -Xmx512m
  volumes:
    - elasticsearch_data:/usr/share/elasticsearch/data
  networks:
    - monitoring-net
```

### 3.2 Logstash Configuration

Configure Logstash for log processing:

```yaml
logstash:
  image: docker.elastic.co/logstash/logstash:7.17.9
  ports:
    - "5044:5044"
    - "5000:5000"
    - "9600:9600"
  volumes:
    - ./logstash/pipeline:/usr/share/logstash/pipeline
  networks:
    - monitoring-net
  depends_on:
    - elasticsearch
```

### 3.3 Kibana Configuration

Configure Kibana for log visualization:

```yaml
kibana:
  image: docker.elastic.co/kibana/kibana:7.17.9
  ports:
    - "5601:5601"
  environment:
    - ELASTICSEARCH_HOSTS=http://elasticsearch:9200
  networks:
    - monitoring-net
  depends_on:
    - elasticsearch
```

### 3.4 Starting the ELK Stack

Start the ELK stack with:

```bash
docker-compose up -d elasticsearch logstash kibana
```

Access Kibana at `http://localhost:5601`.

## Part 4: Host and Container Metrics

### 4.1 Node Exporter Configuration

Configure Node Exporter for host metrics:

```yaml
node-exporter:
  image: prom/node-exporter:v1.6.1
  ports:
    - "9100:9100"
  volumes:
    - /proc:/host/proc:ro
    - /sys:/host/sys:ro
    - /:/rootfs:ro
  networks:
    - monitoring-net
```

### 4.2 cAdvisor Configuration

Configure cAdvisor for container metrics:

```yaml
cadvisor:
  image: gcr.io/cadvisor/cadvisor:v0.47.1
  ports:
    - "8080:8080"
  volumes:
    - /:/rootfs:ro
    - /var/run:/var/run:ro
    - /sys:/sys:ro
    - /var/lib/docker/:/var/lib/docker:ro
    - /dev/disk/:/dev/disk:ro
  networks:
    - monitoring-net
  privileged: true
```

### 4.3 Starting Node Exporter and cAdvisor

Start the metrics services with:

```bash
docker-compose up -d node-exporter cadvisor
```

## Cleanup

- Remember to clean up resources after completing the lab to avoid unnecessary charges or resource usage.
- Use `docker-compose down` to stop and remove containers, networks, and volumes created by the `docker-compose up` command. 