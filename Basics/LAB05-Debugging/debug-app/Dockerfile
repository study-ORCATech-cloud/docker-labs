FROM python:3.9-slim

# BUG 1: Missing working directory setup
# WORKDIR /app

# BUG 2: Installing dependencies individually (inefficient)
COPY requirements.txt ./
RUN pip install flask==2.2.3
RUN pip install werkzeug==2.2.3
RUN pip install requests==2.28.2
RUN pip install itsdangerous==2.1.2

# BUG 3: Copying files incorrectly (could cause missing files)
COPY app.py /app.py

# BUG 4: Exposing wrong port (app runs on 8080, but we expose 5000)
EXPOSE 5000

# BUG 5: Command doesn't use absolute path for app.py
CMD ["python", "app.py"]

# BUG 6: No healthcheck
# HEALTHCHECK --interval=5s --timeout=3s --start-period=5s --retries=3 \
#   CMD curl -f http://localhost:8080/ || exit 1

# BUG 7: No environment variables set for configuration
# ENV API_KEY=demo-key

# BUG 8: No log directory created
# RUN mkdir -p /tmp/logs 