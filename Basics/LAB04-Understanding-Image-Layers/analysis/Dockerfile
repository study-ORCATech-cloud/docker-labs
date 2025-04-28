# Dockerfile for analysis exercise
# This file contains several inefficient practices
# Your task is to analyze each problem and document them

# TODO: Analyze the base image choice
# HINT: Consider if this is the most appropriate base image for a production application
FROM ubuntu:latest

# Set the working directory
WORKDIR /app

# TODO: Analyze these RUN commands - are they efficient?
# HINT: Think about Docker layers and caching
RUN apt-get update
RUN apt-get install -y python3
RUN apt-get install -y python3-pip
RUN apt-get install -y curl
RUN apt-get install -y git
RUN apt-get install -y vim

# Install Python packages individually
# TODO: Analyze this approach to dependency installation
# HINT: Consider the number of layers being created
RUN pip3 install Flask
RUN pip3 install requests
RUN pip3 install pandas
RUN pip3 install matplotlib
RUN pip3 install numpy
RUN pip3 install scikit-learn

# TODO: Analyze the file copying approach
# HINT: Consider how Docker caching works with file changes
COPY . /app/

# TODO: Analyze these commands
# HINT: Think about unnecessary operations in a container
RUN apt-get update
RUN apt-get install -y nodejs npm
RUN npm install -g some-package
RUN apt-get clean

# TODO: Analyze the cleanup approach
# HINT: Is this effective for reducing image size?
RUN rm -rf /var/lib/apt/lists/*

# TODO: Analyze the command choice
# HINT: Consider if this is the most efficient way to run a Flask application
CMD ["python3", "app.py"]

# After completing your analysis, create a file called layer_analysis.md in this directory
# documenting all the issues you've identified and how you would improve them 