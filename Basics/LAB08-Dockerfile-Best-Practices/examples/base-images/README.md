# Base Image Examples

This directory contains examples of different base image strategies for Dockerfiles.

## Multi-stage Distroless Example

The `Dockerfile.multistage-distroless` demonstrates:

- Using multi-stage builds to separate build and runtime environments
- Building a Python application with a full build environment
- Creating a minimal production image using a distroless base image
- Running as a non-root user for better security

### What are Distroless Images?

Distroless images:
- Contain only your application and its runtime dependencies
- Do not contain package managers, shells, or other programs found in standard Linux distributions
- Result in smaller, more secure images with reduced attack surface
- Are maintained by Google (the `gcr.io/distroless` series)

### Building and Running

Build the image:
```bash
docker build -t distroless-demo -f Dockerfile.multistage-distroless .
```

Run the container:
```bash
docker run -p 8080:8080 distroless-demo
```

Access the application at http://localhost:8080

### Benefits

- **Smaller image size**: Only includes the necessary runtime components
- **Improved security**: Fewer installed packages means fewer potential vulnerabilities
- **Reduced attack surface**: No shell, package managers, or other utilities that could be exploited
- **Better performance**: Less overhead from unnecessary components

## TODO

Try modifying the example:
1. Change the application to serve different content
2. Experiment with different distroless base images (e.g., `gcr.io/distroless/base`)
3. Add dependencies to the application and observe how the build process changes
4. Compare the size of the different images (Ubuntu, Debian, Alpine, Distroless)
5. Document your findings regarding the security, performance and size differences 