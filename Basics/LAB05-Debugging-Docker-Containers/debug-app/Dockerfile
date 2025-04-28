FROM python:3.9-slim

# TODO 1: Set up a working directory
# Problem: Missing working directory setup
# HINT: Use WORKDIR to create and set a proper directory
# WORKDIR /app

# TODO 2: Install dependencies efficiently
# Problem: Dependencies are installed inefficiently, one by one
# HINT: Use the requirements.txt file with a single pip command
COPY requirements.txt ./
RUN pip install flask==2.2.3
RUN pip install werkzeug==2.2.3
RUN pip install requests==2.28.2
RUN pip install itsdangerous==2.1.2

# TODO 3: Fix file copying
# Problem: Files are copied to incorrect locations
# HINT: Copy files to the proper working directory
COPY app.py /app.py

# TODO 4: Fix port configuration
# Problem: Exposed port doesn't match the application code
# HINT: Make sure the port matches what's used in app.py
EXPOSE 5000

# TODO 5: Fix app execution path
# Problem: Command doesn't use absolute path
# HINT: Use the full path to ensure the app can be found
CMD ["python", "app.py"]

# TODO 6: Add healthcheck
# Problem: No health monitoring for the container
# HINT: Add a HEALTHCHECK instruction for monitoring container health
# HEALTHCHECK --interval=5s --timeout=3s --start-period=5s --retries=3 \
#   CMD curl -f http://localhost:8080/ || exit 1

# TODO 7: Set environment variables
# Problem: Missing required environment variables
# HINT: Set API_KEY and other necessary variables
# ENV API_KEY=demo-key

# TODO 8: Create log directory
# Problem: Log directory doesn't exist
# HINT: Create the directory needed for application logs
# RUN mkdir -p /tmp/logs 