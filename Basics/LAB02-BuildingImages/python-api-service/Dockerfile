# TODO: Implement a multi-stage build for the Python API service
# The build should have two stages: a builder stage and a final stage

# TODO: Build Stage
# HINT: Use a suitable Python base image for the build stage
# Example: FROM python:3.9 AS builder
FROM scratch AS builder

# TODO: Set up the working directory for the build stage

# TODO: Copy only the requirements file first and prepare dependencies
# HINT: Consider using pip wheel to create wheel files for better performance

# TODO: Final Stage
# HINT: Use a smaller base image for the final stage
FROM scratch

# TODO: Create a non-root user for security
# HINT: Use the useradd command to create a user with appropriate permissions

# TODO: Set up the working directory for the final stage

# TODO: Copy and install dependencies from the build stage
# HINT: Copy the wheel files from the builder stage and install them

# TODO: Copy the application code
# HINT: Only copy the files needed for the application to run

# TODO: Set necessary environment variables
# HINT: Configure Python to not write bytecode files and use unbuffered output

# TODO: Switch to the non-root user
# HINT: Use the USER instruction to run as the non-root user you created

# TODO: Expose the port the application listens on
# HINT: The API service runs on port 8000

# TODO: Add a healthcheck
# HINT: Use the HEALTHCHECK instruction to verify the application is running correctly
# Example: HEALTHCHECK --interval=30s --timeout=3s CMD curl -f http://localhost:8000/health || exit 1

# TODO: Set the command to run the application
# HINT: Use CMD or ENTRYPOINT to specify how to start the Python application 