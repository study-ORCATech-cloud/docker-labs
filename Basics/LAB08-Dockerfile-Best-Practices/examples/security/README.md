# Docker Security Best Practices

This directory demonstrates security best practices for Docker images and how to identify and fix common security issues.

## The Importance of Docker Security

Security vulnerabilities in Docker images can lead to:
- Unauthorized access to containers
- Data breaches
- Privilege escalation
- Supply chain attacks
- Container escape

## Project Structure

- `app.py`: A simple Flask application with intentional security issues
- `requirements.txt`: Python dependencies (including a vulnerable version)
- `Dockerfile`: A Dockerfile with multiple security issues

## Security Issues in the Example

This example contains intentionally insecure practices:
1. Running as root user
2. Using unspecific base image tags
3. No health checks
4. Debug mode enabled
5. Hard-coded credentials
6. Outdated dependencies with vulnerabilities
7. No package integrity verification
8. No resource limits

## Task: Identify and Fix Security Issues

The goal is to identify all security issues in the Dockerfile and application, then fix them to create a secure image.

## Instructions

1. Review the insecure `Dockerfile` and `app.py`
2. Build the insecure image:
   ```bash
   docker build -t security-demo:insecure .
   ```

3. Identify all security issues in:
   - The Dockerfile
   - The application code
   - The dependencies

4. Create an improved version with security best practices:
   - Use specific base image tags
   - Create and use a non-root user
   - Add health checks
   - Set resource limits
   - Remove debug mode
   - Update vulnerable dependencies
   - Add package verification
   - Implement proper secret management

5. Build your secure version:
   ```bash
   docker build -t security-demo:secure -f Dockerfile.secure .
   ```

6. Test both images to ensure functionality is maintained while security is improved

## Security Best Practices

- **Use specific base image tags**: Never use 'latest' for production
- **Run as non-root user**: Create a dedicated user with minimal permissions
- **Implement health checks**: Help container orchestrators detect and recover from issues
- **Set resource limits**: Prevent DoS attacks through resource exhaustion
- **Keep dependencies updated**: Regularly update to patch security vulnerabilities
- **Use multi-stage builds**: Reduce attack surface in the final image
- **Scan images for vulnerabilities**: Use tools like Trivy, Clair, or Snyk
- **Use secrets management**: Never hardcode credentials in your image

## TODO

Complete the following tasks:
1. Identify all security issues in the Dockerfile
2. Create a secure version of the Dockerfile
3. Fix the security issues in the application code
4. Create a security checklist for Docker images
5. Scan the image for vulnerabilities using a scanning tool 