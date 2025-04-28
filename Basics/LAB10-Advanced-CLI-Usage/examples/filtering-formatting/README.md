# Advanced Docker CLI Filtering and Formatting

This directory contains examples and instructions for mastering advanced Docker CLI filtering and formatting techniques.

## Overview

Docker CLI provides powerful filtering and formatting capabilities that allow you to:
- Extract specific information from command outputs
- Format output to suit your specific needs
- Filter resources based on a wide range of criteria
- Create custom views for different use cases

## Filtering Basics

Most Docker commands support the `--filter` (or `-f`) flag to filter results based on specific criteria.

### Common Filter Patterns

```bash
# Filter containers by name
docker ps --filter "name=web"

# Filter containers by status
docker ps --filter "status=running"

# Filter images by reference/tag
docker images --filter "reference=nginx:alpine"

# Filter by label
docker ps --filter "label=environment=production"

# Filter by mount point
docker ps --filter "volume=/data"

# Combine multiple filters (AND logic)
docker ps --filter "status=running" --filter "label=app=web"
```

### Advanced Filtering Techniques

The file `advanced_filters.sh` in this directory contains examples of advanced filtering techniques, including:

- Regular expression filtering
- Time-based filtering
- Network and volume filtering
- Health status filtering
- Exit code filtering

## Formatting Output

Docker CLI allows customizing output format using Go templates with the `--format` flag.

### Basic Formatting Examples

```bash
# Show only container IDs and names
docker ps --format "{{.ID}}: {{.Names}}"

# Format image listing to show repository, tag, and size
docker images --format "{{.Repository}}:{{.Tag}} ({{.Size}})"

# Table format for container listing
docker ps --format "table {{.ID}}\t{{.Names}}\t{{.Status}}"
```

### Available Template Data

Different Docker commands expose different data fields for formatting:

1. `docker ps`:
   - `.ID`, `.Names`, `.Image`, `.Command`, `.CreatedAt`, `.RunningFor`
   - `.Status`, `.Ports`, `.Size`, `.Labels`, `.Mounts`, `.Networks`

2. `docker images`:
   - `.Repository`, `.Tag`, `.ID`, `.CreatedAt`, `.Size`, `.Digest`
   - `.SharedSize`, `.VirtualSize`, `.UniqueSize`

3. `docker volume ls`:
   - `.Name`, `.Driver`, `.Scope`, `.Mountpoint`, `.Labels`

4. `docker network ls`:
   - `.ID`, `.Name`, `.Driver`, `.Scope`, `.IPv6`, `.Internal`
   - `.CreatedAt`, `.Labels`

### Advanced Formatting

The file `custom_formats.sh` in this directory demonstrates advanced formatting techniques:

- Conditional formatting
- Nested templates
- Built-in functions
- Custom reporting templates

## Combining Filtering and Formatting

The real power comes from combining filtering and formatting:

```bash
# List running containers with their CPU and memory usage
docker ps --filter "status=running" --format "{{.Names}}: {{.CPUPerc}} CPU, {{.MemUsage}} MEM"

# Find images larger than 1GB and display their size
docker images --format "{{.Size}}: {{.Repository}}:{{.Tag}}" | grep GB

# List untagged (dangling) images with creation date
docker images --filter "dangling=true" --format "{{.ID}}: created {{.CreatedAt}}"
```

## Practical Examples

This directory includes several practical examples:

1. `container_report.py`: Python script that generates a detailed container usage report
2. `image_analyzer.py`: Tool to analyze image usage and identify cleanup opportunities
3. `resource_dashboard.sh`: Shell script creating a real-time resource usage dashboard
4. `custom_view_templates/`: Directory containing custom view templates for different use cases

## Custom View Templates

You can save your commonly used formats in template files for reuse. The `custom_view_templates/` directory contains examples:

- `container_compact.tmpl`: Compact view of containers
- `container_detailed.tmpl`: Detailed container information
- `security_audit.tmpl`: Container view focusing on security aspects
- `network_view.tmpl`: Network-focused container view

## TODO

Complete the following tasks:
1. Experiment with the filter patterns in the examples
2. Create at least three custom formatting templates for different use cases
3. Modify the `container_report.py` script to include additional information you find useful
4. Implement an image cleanup script that identifies unused/old images using filters
5. Create a script that generates a daily Docker resource usage report
6. Document your preferred filtering and formatting patterns in `my_formats.md` 