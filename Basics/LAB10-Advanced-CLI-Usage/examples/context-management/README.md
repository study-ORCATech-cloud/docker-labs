# Docker Context Management

This guide covers Docker context management, allowing you to seamlessly work with multiple Docker environments from a single CLI.

## Overview

Docker contexts enable you to:
- Configure and manage connections to different Docker environments
- Switch between environments without modifying configuration files
- Work with multiple Docker engines (local, remote, swarm, Kubernetes)
- Create environment-specific workflows

## Understanding Docker Contexts

A Docker context contains endpoint configuration that tells the Docker CLI how to communicate with the Docker Engine. By default, Docker creates a context named `default` that connects to the local Docker daemon.

### Basic Context Commands

```bash
# List available contexts
docker context ls

# Create a new context
docker context create my-remote-docker --docker "host=ssh://username@remote-host"

# Switch to a different context
docker context use my-remote-docker

# Display current context
docker context show

# Inspect a context
docker context inspect my-remote-docker

# Remove a context
docker context rm my-remote-docker
```

## Creating Different Types of Contexts

### SSH-Based Remote Docker Context

```bash
# Create a context for a remote Docker host using SSH
docker context create remote-prod \
  --docker "host=ssh://user@remote-server.example.com"
```

### HTTPS-Based Remote Docker Context with TLS

```bash
# Create a context with TLS certificates
docker context create secure-prod \
  --docker "host=tcp://remote-server.example.com:2376,ca=/path/to/ca.pem,cert=/path/to/cert.pem,key=/path/to/key.pem"
```

### Kubernetes Context Integration

```bash
# Create a context that points to a Kubernetes cluster
docker context create k8s-context \
  --kubernetes "config=/path/to/kube/config,context=kubernetes-cluster-name"
```

### Local Development Context with Custom Settings

```bash
# Create a development context with specific environment variables
docker context create dev \
  --docker "host=unix:///var/run/docker.sock" \
  --description "Local development environment"
```

## Using Contexts Effectively

### Running Commands in a Specific Context Without Switching

```bash
# Run a command in a specific context without changing the current context
docker --context remote-prod ps -a

# Pull an image in a specific context
docker --context dev pull nginx:latest

# Deploy a stack to a specific Swarm context
docker --context swarm-prod stack deploy -c docker-compose.yml my-stack
```

### Environment Variables for Context Selection

```bash
# Set the default context via environment variable
export DOCKER_CONTEXT=remote-prod
docker ps -a  # Will use remote-prod context

# Override with specific context for a single command
DOCKER_CONTEXT=dev docker ps -a
```

## Context Management Best Practices

1. **Use Descriptive Names**
   ```bash
   docker context create prod-eu-west --description "Production EU West Region" --docker "host=ssh://user@eu-west.example.com"
   ```

2. **Export and Import Contexts**
   ```bash
   # Export a context
   docker context export prod-eu-west --output prod-eu-west.dockercontext
   
   # Import a context
   docker context import new-prod-eu-west prod-eu-west.dockercontext
   ```

3. **Organize Contexts by Environment or Region**
   Use naming conventions like `env-region-role` (e.g., `prod-useast-manager`)

4. **Update Context Configuration**
   ```bash
   docker context update my-context --docker "host=ssh://new-host.example.com"
   ```

## Security Considerations

1. **Never embed passwords in context definitions**
   Use SSH keys or appropriate credential stores

2. **Restrict access to exported context files**
   They may contain sensitive endpoint information

3. **Use TLS certificates for secure connections**
   Always specify CA, cert, and key files for non-SSH connections

4. **Regularly rotate credentials**
   Update contexts when certificates or SSH keys change

## Practical Scenarios

### Scenario: Multi-Environment Deployment

```bash
# Deploy to development
docker --context dev stack deploy -c docker-compose.yml my-app

# Deploy to staging
docker --context staging stack deploy -c docker-compose.yml my-app

# Deploy to production
docker --context prod stack deploy -c docker-compose.yml my-app
```

### Scenario: Resource Monitoring Across Environments

```bash
# Check container status across environments
for ctx in dev staging prod; do
  echo "===== $ctx ====="
  docker --context $ctx ps
done
```

### Scenario: Working with Multiple Kubernetes Clusters

```bash
# Create contexts for different Kubernetes clusters
docker context create k8s-dev --kubernetes config=/path/to/kubeconfig,context=dev-cluster
docker context create k8s-prod --kubernetes config=/path/to/kubeconfig,context=prod-cluster

# Switch between Kubernetes contexts
docker context use k8s-dev
kubectl get pods

docker context use k8s-prod
kubectl get pods
```

## Automated Context Switching

When working with multiple contexts, you may want to create aliases or helper functions:

```bash
# Add these to your .bashrc or .zshrc
alias docker-dev="docker --context dev"
alias docker-prod="docker --context prod"

# Create a function to easily switch contexts
dctx() {
  docker context use "$1"
}
```

## TODO Tasks

1. Create contexts for at least three different environments:
   - Local development environment
   - A staging environment (can be simulated with Docker-in-Docker if needed)
   - A production-like environment

2. Configure proper SSH keys and/or TLS certificates for secure context connections

3. Write a shell script that executes the same Docker command across all contexts and compares the results

4. Create an organizational strategy for your contexts with proper naming conventions and descriptions

5. Practice exporting and importing contexts between different machines

6. Create a context for a Kubernetes cluster (if available) and practice kubectl commands

7. Develop a routine for context verification before executing critical commands

8. Document each context's purpose, connection details, and usage examples

9. Create helper aliases or functions for commonly used context operations

10. Test context-specific environment variables and their impact on Docker commands

## Additional Resources

- [Docker Context Documentation](https://docs.docker.com/engine/context/working-with-contexts/)
- [Docker Context Command Reference](https://docs.docker.com/engine/reference/commandline/context/)
- [Docker Context Environment Variables](https://docs.docker.com/engine/reference/commandline/cli/#environment-variables)
- [Secure Docker Daemon Connections](https://docs.docker.com/engine/security/protect-access/) 