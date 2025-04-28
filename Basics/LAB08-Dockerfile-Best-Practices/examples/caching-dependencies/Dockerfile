FROM python:3.9

# Set working directory
WORKDIR /app

# Copy the entire application at once (poor caching practice)
COPY . .

# Install all dependencies
RUN pip install -r requirements.txt

# Expose port for the application
EXPOSE 8080

# Command to run the application
CMD ["python", "app.py"]

# TODO: Refactor this Dockerfile to better leverage Docker's build cache
# TODO: Copy dependency files first (requirements.txt) before copying application code
# TODO: Install dependencies before copying the rest of the application
# TODO: Use pip's cache directory mounting if available in your environment
# TODO: Consider using multi-stage builds if there are build dependencies 