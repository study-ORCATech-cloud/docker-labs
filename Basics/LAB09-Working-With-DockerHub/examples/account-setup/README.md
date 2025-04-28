# Docker Hub Account Setup

This directory contains instructions and examples for setting up and configuring your Docker Hub account.

## Creating a Docker Hub Account

1. Visit [Docker Hub](https://hub.docker.com/) in your web browser
2. Click the "Sign Up" button in the top-right corner
3. Enter your details:
   - Docker ID (username, choose carefully as it will be visible in your image names)
   - Email address
   - Password
4. Click "Sign Up"
5. Verify your email address by clicking the link in the verification email
6. Complete any additional steps required (like CAPTCHA verification)

## Logging in to Docker Hub

### Via Web Interface
1. Visit [Docker Hub](https://hub.docker.com/)
2. Click "Sign In" in the top-right corner
3. Enter your Docker ID and password
4. Click "Sign In"

### Via Docker CLI
Using the command line interface:

```bash
# Log in to Docker Hub
docker login

# You'll be prompted for your username and password
# Enter your Docker ID and password
```

For improved security, you can create and use access tokens instead of your password:
1. Log in to Docker Hub via the web interface
2. Go to Account Settings > Security
3. Create a new access token
4. Use this token instead of your password when logging in via CLI

## Exploring Docker Hub Interface

After logging in, take some time to explore the Docker Hub interface:

1. **Home Page**: Displays featured and popular images
2. **Repositories**: Shows your repositories and allows creation of new ones
3. **Organizations**: Access to any organizations you belong to
4. **Explore**: Browse public images from the community
5. **Account Settings**:
   - Profile: Update your profile information
   - Security: Manage access tokens and linked accounts
   - Notifications: Configure email notifications
   - Linked Accounts: Connect to GitHub, GitLab, etc.

## Docker Hub Free vs Paid Plans

Docker Hub offers different plans with varying features:

- **Free Plan**:
  - Unlimited public repositories
  - Limited private repositories
  - Pull rate limits
  - Basic features

- **Pro/Team/Business Plans**:
  - More private repositories
  - Higher pull rate limits
  - Advanced security features
  - Team management capabilities
  - Priority support

## TODO

Complete the following tasks:
1. Create a Docker Hub account if you don't already have one
2. Configure Docker CLI to work with your Docker Hub account
3. Explore the Docker Hub dashboard and familiarize yourself with its interface
4. Document the key features of Docker Hub that you'll be using in this lab
5. Create a file called `docker_hub_notes.md` with your observations and key features 