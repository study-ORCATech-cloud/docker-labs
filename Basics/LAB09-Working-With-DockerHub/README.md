# LAB09: Working With DockerHub

This lab teaches how to effectively use Docker Hub for storing, sharing, and deploying Docker images.

## Lab Overview

In this lab, you will:
- Learn how to create and manage Docker Hub accounts and repositories
- Create and push Docker images to Docker Hub
- Work with public and private repositories
- Use Docker Hub features like tags, automation, and webhooks
- Implement best practices for Docker image distribution
- Understand Docker Hub security features and limitations

## Important Note

**This lab is designed for hands-on learning:**
- Implement all TODOs in the example directories yourself before checking solutions
- Consult the `solutions.md` file *only after* attempting to solve the problems yourself
- Focus on understanding the principles behind each operation
- All code examples in this lab use Python for consistency

## Learning Objectives

- Master Docker Hub account and repository management
- Implement proper image tagging and versioning strategies
- Understand and configure DockerHub webhooks
- Set up automated builds from source control
- Implement proper security practices for Docker Hub
- Efficiently search and use public Docker images
- Configure Docker Hub integrations

## Prerequisites

- Docker Engine installed
- Completion of LAB01-LAB08
- Basic understanding of Docker images and containers
- Internet connection for Docker Hub access
- A free Docker Hub account (you'll create one if you don't have it)

## Important Instructions

This lab is designed for hands-on learning. You are expected to:
- Create a free Docker Hub account (if you don't already have one)
- Follow the exercises in each task sequentially
- Implement solutions yourself rather than copying from external sources
- Document your findings regarding Docker Hub features and limitations

Do not skip the account setup steps if you're unfamiliar with Docker Hub - the goal is to develop your Docker Hub skills through practical experience.

## Lab Projects

This lab includes a series of examples in the `examples` directory demonstrating various Docker Hub operations and best practices.

## Lab Tasks

### Task 1: Getting Started with Docker Hub

1. **Create a Docker Hub account**
   - Navigate to [Docker Hub](https://hub.docker.com/)
   - Sign up for a free account if you don't have one
   - Verify your email address

2. **Explore Docker Hub interface**
   - Repositories section
   - Profile settings
   - Organizations (if applicable)
   - Security settings

3. **Install Docker CLI (if not already installed)**
   - Ensure Docker CLI is configured on your system
   - Test with basic commands (`docker info`, `docker version`)

Navigate to the `examples/account-setup` directory:

```bash
cd examples/account-setup
```

TODO:
1. Follow the instructions in the README to create a Docker Hub account
2. Configure Docker CLI to work with your Docker Hub account
3. Explore the Docker Hub dashboard and familiarize yourself with its interface
4. Document the key features of Docker Hub that you'll be using in this lab

### Task 2: Creating and Managing Repositories

Navigate to the `examples/repositories` directory:

```bash
cd ../repositories
```

TODO:
1. Create a public repository on Docker Hub through the web interface
2. Create a private repository on Docker Hub through the web interface
3. Explore repository settings and features
4. Document the differences between public and private repositories
5. Configure repository description, readme, and tags

### Task 3: Building and Pushing Images

Navigate to the `examples/pushing-images` directory:

```bash
cd ../pushing-images
```

TODO:
1. Build the provided Dockerfile to create a simple image
2. Tag the image according to Docker Hub conventions
3. Push the image to your Docker Hub repository
4. Verify the image appears in your Docker Hub repository
5. Update the image and push a new version

### Task 4: Tagging and Versioning Strategies

Navigate to the `examples/tagging-strategy` directory:

```bash
cd ../tagging-strategy
```

TODO:
1. Implement semantic versioning for the provided application
2. Create multiple tagged versions of the same image
3. Use the `latest` tag appropriately
4. Implement environment-specific tags (dev, staging, prod)
5. Document your tagging strategy and its benefits

### Task 5: Working with Docker Hub Webhooks

Navigate to the `examples/webhooks` directory:

```bash
cd ../webhooks
```

TODO:
1. Create a simple webhook receiver using the provided Python application
2. Configure a webhook in your Docker Hub repository
3. Test the webhook with image pushes
4. Document the webhook payload and potential use cases
5. Implement a basic automation triggered by the webhook

### Task 6: Automated Builds

Navigate to the `examples/automated-builds` directory:

```bash
cd ../automated-builds
```

TODO:
1. Connect your Docker Hub account to a GitHub or GitLab account
2. Set up automated builds for a repository
3. Configure build rules based on branches or tags
4. Test the automated build by pushing changes to your source repository
5. Document the automated build process and its benefits

### Task 7: Image Security and Scanning

Navigate to the `examples/security` directory:

```bash
cd ../security
```

TODO:
1. Enable vulnerability scanning for your Docker Hub repository
2. Analyze the scan results for the provided image
3. Fix the vulnerabilities identified in the image
4. Implement security best practices for Docker images
5. Document the security features of Docker Hub and their limitations

### Task 8: Working with Docker Hub API

Navigate to the `examples/api-access` directory:

```bash
cd ../api-access
```

TODO:
1. Generate a Docker Hub access token
2. Use the provided Python script to interact with the Docker Hub API
3. List your repositories programmatically
4. Get detailed information about a specific repository
5. Implement a simple script to automate repository management

### Task 9: Docker Hub Organizations and Teams

Navigate to the `examples/organizations` directory:

```bash
cd ../organizations
```

TODO:
1. Understand the concept of Docker Hub organizations
2. Explore the organization features (teams, permissions, etc.)
3. Document the benefits of using organizations for team collaboration
4. Create a simulated organization structure using the provided examples
5. Implement proper access controls and permissions

### Task 10: Real-world Docker Hub Integration

Navigate to the `examples/real-world` directory:

```bash
cd ../real-world
```

TODO:
1. Create a complete CI/CD pipeline that integrates with Docker Hub
2. Implement proper image lifecycle management
3. Configure notifications and monitoring for Docker Hub activities
4. Document the real-world integration patterns and best practices
5. Implement a sample deployment workflow using Docker Hub images

## Testing Your Understanding

After completing the lab exercises, you should be able to:
- Create and manage Docker Hub repositories effectively
- Implement proper tagging and versioning strategies
- Use Docker Hub features for automation and integration
- Implement security best practices for Docker images
- Understand the role of Docker Hub in a CI/CD pipeline

## Lab Cleanup

Clean up resources created during this lab:

```bash
# Remove local images created for this lab
docker rmi $(docker images -q "yourusername/*")

# Remove containers created during testing
docker rm $(docker ps -a -q --filter "name=lab09*")

# Log out of Docker Hub (optional)
docker logout
```

## Additional Resources

- [Docker Hub Documentation](https://docs.docker.com/docker-hub/)
- [Docker Hub API Documentation](https://docs.docker.com/docker-hub/api/latest/)
- [Docker Official Images](https://hub.docker.com/search?q=&type=image&image_filter=official)
- [Docker Hub Best Practices](https://docs.docker.com/docker-hub/publish/)
- [Docker Content Trust](https://docs.docker.com/engine/security/trust/) 