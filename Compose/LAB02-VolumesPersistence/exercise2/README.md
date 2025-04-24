# Exercise 2: Development Environment with Bind Mounts

This exercise demonstrates how to use bind mounts for real-time development. You'll create a web application that connects to the PostgreSQL database and updates as you edit the code.

## Overview

In this exercise, you will:
1. Configure Docker Compose with bind mounts for local development
2. Run a Python Flask web application with a bind mount to the host filesystem
3. Make changes to the code and see them reflected immediately
4. Understand the difference between bind mounts and volumes for development

## Files

- `Dockerfile`: Defines the Python environment for the web application
- `app/`: Contains the application source code
- `app/app.py`: Main Flask application file
- `app/templates/index.html`: HTML template for the web interface
- `app/requirements.txt`: Python dependencies

## Instructions

### Step 1: Configure the Docker Compose File

Before starting, add the bind mount configuration to the `docker-compose.yml` file:

```yaml
# TODO: Configure the webapp service with:
# 1. A bind mount that maps ./exercise2/app on your host to /app in the container
# 2. Make sure the Dockerfile and docker-compose.yml work together correctly
```

This configuration will sync your local development files with the container.

### Step 2: Start the Web Application

```bash
# Make sure the database is running
docker-compose up -d postgres-db

# Start the web application
docker-compose up -d webapp

# Check both services are running
docker-compose ps
```

### Step 3: Access the Web Application

Open your browser and navigate to http://localhost:8080

You should see the Notes application. Try adding a few notes to test that it works.

### Step 4: Edit the Code to See Real-time Changes

Now for the fun part - make changes to the code and see them update in real-time without restarting the container!

1. Open `app/templates/index.html` in your editor
2. Make a visible change to the HTML, such as:
   - Change the header text
   - Update the background color
   - Add a new element
3. Save the file
4. Refresh your browser to see the changes

For more significant changes, try:

- Modify `app.py` to add a new route or feature
- Change how notes are displayed
- Add sorting or filtering functionality 

### Step 5: Observe the Bind Mount in Action

```bash
# View the bind mount configuration
docker-compose config

# Inspect the container
docker inspect webapp-dev
```

### Step 6: Cleanup

When you're finished with this exercise, clean up the resources:

```bash
# Stop the web application container
docker-compose stop webapp

# Remove the web application container
docker-compose rm -f webapp

# If you also want to clean up the database (if not needed for other exercises)
docker-compose stop postgres-db
docker-compose rm -f postgres-db
```

## How Bind Mounts Work

Unlike named volumes, bind mounts:
- Link a container directory directly to a host directory
- Allow changes to propagate instantly between host and container
- Are ideal for development environments
- Provide a way to use your preferred editor on the host while running in a container

## Expected Results

- Changes to the application code should be reflected immediately
- You can develop within your host environment but run in the container
- The Flask debug mode will auto-reload on Python code changes

## Key Learning Points

- Bind mounts provide a direct connection to host files
- They enable efficient development workflows
- The performance may vary based on host OS and Docker implementation
- Using bind mounts in development but volumes in production is a common pattern
- Docker Compose makes development environment setup consistent across team members 