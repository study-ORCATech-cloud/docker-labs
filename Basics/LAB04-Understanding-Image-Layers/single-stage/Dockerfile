FROM python:3.9

# Set a working directory
WORKDIR /app

# TODO 1: Install system dependencies efficiently
# -------------------------------------------------------------------
# TASK: Combine all system dependency installations into a single RUN command
# HINT: Use && to chain commands and \ for line continuation
# 
# Current implementation (inefficient - creates multiple layers):
RUN apt-get update
RUN apt-get install -y --no-install-recommends gcc
RUN apt-get install -y --no-install-recommends g++
RUN apt-get install -y --no-install-recommends build-essential

# TODO 2: Install Python dependencies efficiently
# -------------------------------------------------------------------
# TASK: Use requirements.txt with a single pip install command
# HINT: Use pip install -r requirements.txt with appropriate flags
#
# Current implementation (inefficient - creates multiple layers):
COPY requirements.txt .
RUN pip install Flask==2.2.3
RUN pip install Werkzeug==2.2.3
RUN pip install numpy==1.24.3
RUN pip install pandas==2.0.0
RUN pip install matplotlib==3.7.1
RUN pip install scipy==1.10.1
RUN pip install requests==2.28.2
RUN pip install gunicorn==20.1.0

# Copy the application code (another layer)
COPY app.py .

# TODO 3: Optimize directory creation and permissions
# -------------------------------------------------------------------
# TASK: Combine mkdir and chmod commands into a single RUN
# HINT: Chain commands with && to reduce layers
#
# Current implementation (inefficient - creates multiple layers):
RUN mkdir -p /app/data
RUN chmod 755 /app/app.py

# Set environment variables (metadata, not a layer)
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# TODO 4: Handle development packages appropriately
# -------------------------------------------------------------------
# TASK: Consider if these packages should be in a production image
# HINT: For production, these could be omitted or in a separate stage
#
# Current implementation (inefficient - creates multiple layers):
RUN pip install pytest==7.3.1
RUN pip install black==23.3.0
RUN pip install flake8==6.0.0

# Expose the port (metadata, not a layer)
EXPOSE 5000

# TODO 5: Use an efficient way to run the application
# -------------------------------------------------------------------
# TASK: Replace the default Flask development server
# HINT: Consider using gunicorn for a production environment
#
# Current implementation:
CMD ["python", "app.py"] 