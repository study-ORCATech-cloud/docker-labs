# LAB08: Monitoring and Logging with Docker Compose

This lab focuses on implementing comprehensive monitoring and logging solutions for Docker Compose applications using industry-standard tools.

## Learning Objectives

- Set up a complete monitoring stack for Docker containers
- Implement structured logging with centralized log management
- Create dashboards for visualizing application and container metrics
- Configure alerts for critical system events
- Understand how to debug applications using advanced logging techniques
- Implement health checks for Docker Compose services
- Learn best practices for production-grade monitoring

## Prerequisites

- Docker Engine installed
- Docker Compose v2 installed
- Basic understanding of Docker concepts
- Familiarity with Docker Compose from previous labs
- Basic Python knowledge (for sample applications)

## Monitoring and Logging Concepts

Effective container monitoring and logging are crucial for production environments:

1. **Infrastructure Monitoring**: Track host and container-level metrics
2. **Application Monitoring**: Collect application-specific metrics 
3. **Centralized Logging**: Aggregate logs from all services
4. **Log Analysis**: Extract insights from structured logs
5. **Alerting**: Get notified of problems before users do
6. **Visualization**: Create dashboards for system visibility
7. **Health Checks**: Continuously verify service availability

## Lab Exercises

### Exercise 1: Basic Monitoring with Prometheus and Grafana

Set up the foundation of container monitoring with Prometheus and Grafana.

1. Configure Prometheus to scrape container metrics
2. Set up Grafana for metric visualization
3. Create basic dashboards for container stats
4. Implement custom metrics in a Python application

### Exercise 2: Advanced Application Monitoring

Build on Exercise 1 to implement detailed application-level monitoring.

1. Extend Python applications with custom instrumentation
2. Set up more advanced Grafana dashboards
3. Configure alerts based on metric thresholds
4. Implement recording rules and PromQL queries

### Exercise 3: Centralized Logging with ELK Stack

Implement the ELK stack (Elasticsearch, Logstash, Kibana) for log aggregation.

1. Set up Elasticsearch for log storage
2. Configure Logstash for log processing
3. Implement Kibana for log visualization
4. Add structured logging to Python applications

### Exercise 4: Complete Observability Solution

Combine all previous exercises into a comprehensive observability platform.

1. Merge metrics and logs for complete visibility
2. Implement distributed tracing
3. Create unified dashboards
4. Set up advanced alerting rules
5. Monitor Docker Compose infrastructure

## Files Included

- `docker-compose.yml` - Base configuration for monitoring stack
- `prometheus/` - Prometheus configuration files
- `grafana/` - Grafana dashboards and configuration
- `elasticsearch/` - Elasticsearch configuration
- `logstash/` - Logstash pipelines and configuration
- `kibana/` - Kibana dashboards and configuration
- `/exercise1-4/` - Exercise-specific files and applications

## Project Structure

```
LAB08-MonitoringLogging/
├── exercise1/
│   ├── app/
│   │   ├── Dockerfile
│   │   ├── app.py
│   │   └── requirements.txt
│   ├── prometheus/
│   │   └── prometheus.yml
│   ├── grafana/
│   │   ├── dashboards/
│   │   └── provisioning/
│   └── docker-compose.yml
├── exercise2/
│   ├── app/
│   │   ├── Dockerfile
│   │   ├── app.py
│   │   └── requirements.txt
│   ├── prometheus/
│   │   └── prometheus.yml
│   ├── grafana/
│   │   ├── dashboards/
│   │   └── provisioning/
│   └── docker-compose.yml
├── exercise3/
│   ├── app/
│   │   ├── Dockerfile
│   │   ├── app.py
│   │   └── requirements.txt
│   ├── elasticsearch/
│   │   └── elasticsearch.yml
│   ├── logstash/
│   │   └── pipeline/
│   ├── kibana/
│   │   └── kibana.yml
│   └── docker-compose.yml
├── exercise4/
│   ├── app/
│   │   ├── Dockerfile
│   │   ├── app.py
│   │   └── requirements.txt
│   ├── prometheus/
│   ├── grafana/
│   ├── elasticsearch/
│   ├── logstash/
│   ├── kibana/
│   └── docker-compose.yml
└── README.md
```

## Lab Steps

### Step 1: Basic Monitoring Setup

Let's start with implementing a basic monitoring stack:

```bash
cd exercise1
docker compose up -d
```

This will start:
- A sample Python web application instrumented with Prometheus metrics
- Prometheus server for collecting and storing metrics
- Grafana for visualizing metrics
- Node Exporter for host-level metrics
- cAdvisor for container metrics

Access the services:
- Sample app: http://localhost:8080
- Prometheus: http://localhost:9090
- Grafana: http://localhost:3000 (default login: admin/admin)

Explore the pre-configured dashboards in Grafana to see container and application metrics.

### Step 2: Advanced Application Monitoring

Build on the foundation from Exercise 1 with more advanced monitoring:

```bash
cd ../exercise2
docker compose up -d
```

New features in this setup:
- Application with custom business metrics
- More detailed Prometheus configuration
- Pre-configured alerting rules
- Advanced Grafana dashboards
- Prometheus Alert Manager for notifications

Access additional services:
- Alert Manager: http://localhost:9093

Explore how to create custom metrics, recording rules, and alerts.

### Step 3: Centralized Logging

Set up a complete logging stack:

```bash
cd ../exercise3
docker compose up -d
```

This will start:
- Elasticsearch for log storage
- Logstash for log processing
- Kibana for log visualization
- Filebeat for log shipping
- Sample application with structured logging

Access the logging services:
- Kibana: http://localhost:5601

Explore the pre-configured dashboards in Kibana to analyze application logs.

### Step 4: Complete Observability Solution

Combine metrics and logging for full observability:

```bash
cd ../exercise4
docker compose up -d
```

This comprehensive setup includes:
- All components from previous exercises
- Distributed tracing with Jaeger
- Integration between metrics and logs
- Health checks and self-healing configuration
- Advanced alerting and notification system

Access additional services:
- Jaeger UI: http://localhost:16686

## Commands Reference

```bash
# Start the monitoring stack
docker compose up -d

# View logs from the Prometheus container
docker compose logs prometheus

# Execute a query in Prometheus
curl -s 'http://localhost:9090/api/v1/query?query=up'

# Check Elasticsearch status
curl -s http://localhost:9200/_cluster/health?pretty

# View indices in Elasticsearch
curl -s http://localhost:9200/_cat/indices

# Restart the logging stack
docker compose restart elasticsearch logstash kibana

# Scale the sample application
docker compose up -d --scale app=3
```

## Best Practices

- **Cardinality**: Limit the number of high-cardinality labels in Prometheus
- **Retention**: Configure appropriate data retention policies
- **Persistence**: Use volumes for persistent storage of metrics and logs
- **Alerting**: Set up actionable alerts with clear response procedures
- **Dashboard Organization**: Group related metrics for easier troubleshooting
- **Log Levels**: Use appropriate log levels (DEBUG, INFO, WARNING, ERROR)
- **Structured Logging**: Use JSON or structured format for easier parsing
- **Resource Limits**: Set container limits to prevent resource starvation
- **Security**: Implement authentication for monitoring and logging services
- **Regular Backups**: Back up your monitoring configurations regularly

## Security Considerations

- **Authentication**: Enable auth for all monitoring and logging interfaces
- **Encryption**: Use TLS for all service communications
- **Network Isolation**: Use dedicated networks for monitoring traffic
- **Least Privilege**: Use non-root users for monitoring services
- **Rate Limiting**: Implement rate limiting for monitoring endpoints
- **Data Protection**: Consider data retention and privacy regulations
- **Sensitive Data**: Filter sensitive information from logs

## Cleanup

When you're completely finished with all exercises, clean up all resources:

```bash
# Exercise 1
cd exercise1
docker compose down -v

# Exercise 2
cd ../exercise2
docker compose down -v

# Exercise 3
cd ../exercise3
docker compose down -v

# Exercise 4
cd ../exercise4
docker compose down -v

# Remove all volumes associated with monitoring
docker volume prune -f
```

## Troubleshooting

- **Prometheus not scraping metrics**: Check prometheus.yml configuration and target endpoints
- **No data in Grafana**: Verify Prometheus data source configuration and query syntax
- **Elasticsearch not starting**: Check vm.max_map_count system setting
- **Missing logs in Kibana**: Verify Logstash pipeline and Elasticsearch indices
- **Container metrics missing**: Ensure cAdvisor is running and configured correctly

## Extensions

- **External Alerting**: Integrate with PagerDuty, Slack, or email
- **Long-term Storage**: Set up remote storage for Prometheus with VictoriaMetrics or Thanos
- **Multi-environment Monitoring**: Add environment labels to distinguish staging/production
- **APM Integration**: Implement application performance monitoring with Elastic APM
- **Network Monitoring**: Add monitoring for container networks and traffic

## Next Steps

After completing this lab, you'll be ready to move on to LAB09-MultiStageBuilds to learn about optimizing your Docker images with multi-stage builds for better security and efficiency. 