# Automated Builds with Docker Hub

This directory contains examples and instructions for setting up automated builds in Docker Hub.

## What are Automated Builds?

Automated builds allow you to automatically build Docker images whenever you push code to your source code repository (GitHub or GitLab). This creates a direct connection between your source code and Docker images.

## Benefits of Automated Builds

- **Code-to-image traceability**: Clear connection between source code and Docker images
- **Automated workflow**: No need to manually build and push images
- **Consistency**: Every build follows the same process
- **Versioning**: Automatic tagging based on Git branches and tags
- **Documentation**: README automatically synced from GitHub/GitLab
- **Security**: Improved trust for consumers of your images

## Prerequisites

Before setting up automated builds:
1. You need a Docker Hub account
2. You need a GitHub or GitLab account with a repository containing a Dockerfile
3. You need admin access to both accounts

## Connecting Docker Hub to GitHub/GitLab

1. Log in to Docker Hub
2. Go to Account Settings > Linked Accounts
3. Click on GitHub (or GitLab)
4. Authorize Docker Hub to access your account
5. Select the repositories you want to give access to

## Setting Up an Automated Build

1. Log in to Docker Hub
2. Click "Create Repository" or go to an existing repository
3. In the Build Settings tab:
   - Click "Link to GitHub" (or GitLab)
   - Select your GitHub repository
   - Configure the main build:
     - Source branch (e.g., main)
     - Dockerfile location (e.g., /Dockerfile)
     - Docker tag (e.g., latest)
4. Configure additional build rules as needed
5. Click "Save and Build" to start the first build

## Configuring Build Rules

Build rules determine how branches and tags in your Git repository map to Docker image tags. Examples:

- **Branch-based builds**:
  - Source Type: Branch
  - Source: main
  - Dockerfile location: Dockerfile
  - Docker Tag: latest

- **Tag-based builds**:
  - Source Type: Tag
  - Source: /^v[0-9.]+$/
  - Dockerfile location: Dockerfile
  - Docker Tag: {sourceref}

- **Feature branch builds**:
  - Source Type: Branch
  - Source: /^feature-.*/
  - Dockerfile location: Dockerfile
  - Docker Tag: dev-{sourceref}

## Automated Build Process

When an automated build is triggered:
1. Docker Hub receives a webhook from GitHub/GitLab
2. Docker Hub queues a build job
3. The build service clones your repository
4. The build service builds the Docker image according to your Dockerfile
5. The image is pushed to Docker Hub with the configured tag
6. Build status is updated in Docker Hub

## Sample Repository Structure

This directory includes a sample repository structure suitable for automated builds:

```
repository/
├── Dockerfile         # Main application Dockerfile
├── docker-compose.yml # For local testing
├── src/               # Application source code
│   └── ...
├── .dockerignore      # Files to exclude from the build
└── README.md          # Documentation for your image
```

## Build Triggers

In addition to automated builds, you can set up build triggers to manually trigger builds via API:

1. Go to your repository's Build Settings
2. Under "Build Triggers", create a new trigger
3. Save the trigger URL for use in your CI/CD pipelines

```bash
# Example trigger usage
curl -H "Content-Type: application/json" --data '{"source_type": "Branch", "source_name": "main"}' -X POST <TRIGGER_URL>
```

## TODO

Complete the following tasks:
1. Connect your Docker Hub account to a GitHub or GitLab account
2. Set up automated builds for a repository
3. Configure build rules based on branches or tags
4. Test the automated build by pushing changes to your source repository
5. Document the automated build process and its benefits
6. Create a file called `automated_build_notes.md` with your observations and experiences 