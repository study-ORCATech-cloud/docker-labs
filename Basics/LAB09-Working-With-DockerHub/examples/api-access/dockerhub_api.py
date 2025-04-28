#!/usr/bin/env python3
"""
Docker Hub API Client - Example script for interacting with Docker Hub API
"""

import requests
import os
import json
import sys
import argparse
import datetime
from dotenv import load_dotenv

# Load environment variables from .env file if present
load_dotenv()

# Configuration
DOCKER_HUB_USERNAME = os.environ.get('DOCKER_HUB_USERNAME')
DOCKER_HUB_TOKEN = os.environ.get('DOCKER_HUB_TOKEN')

# Base API URL
API_URL = "https://hub.docker.com/v2"

# Check if credentials are set
if not DOCKER_HUB_USERNAME or not DOCKER_HUB_TOKEN:
    print("Error: Missing Docker Hub credentials")
    print("Please set DOCKER_HUB_USERNAME and DOCKER_HUB_TOKEN environment variables")
    print("You can create a .env file with these variables or export them in your shell")
    sys.exit(1)

# Headers for authentication
headers = {
    "Content-Type": "application/json",
    "Authorization": f"Bearer {DOCKER_HUB_TOKEN}"
}

def call_api(method, endpoint, data=None, params=None):
    """Generic function to call the Docker Hub API with error handling"""
    url = f"{API_URL}{endpoint}"
    
    try:
        if method.lower() == 'get':
            response = requests.get(url, headers=headers, params=params)
        elif method.lower() == 'post':
            response = requests.post(url, headers=headers, json=data if data else {})
        elif method.lower() == 'put':
            response = requests.put(url, headers=headers, json=data if data else {})
        elif method.lower() == 'delete':
            response = requests.delete(url, headers=headers)
        elif method.lower() == 'patch':
            response = requests.patch(url, headers=headers, json=data if data else {})
        else:
            raise ValueError(f"Unsupported method: {method}")
        
        # Check for API errors
        response.raise_for_status()
        
        # Return JSON response if content exists, otherwise empty dict
        return response.json() if response.text else {}
    
    except requests.exceptions.HTTPError as e:
        print(f"HTTP Error: {e}")
        if hasattr(e, 'response') and e.response is not None:
            print(f"Response: {e.response.text}")
        return None
    except requests.exceptions.ConnectionError:
        print(f"Connection Error: Could not connect to {url}")
        return None
    except requests.exceptions.Timeout:
        print("Timeout Error: The request timed out")
        return None
    except requests.exceptions.RequestException as e:
        print(f"Error: {e}")
        return None
    except Exception as e:
        print(f"Unexpected error: {e}")
        return None

def list_repositories():
    """List all repositories for the user"""
    response = call_api('get', f"/repositories/{DOCKER_HUB_USERNAME}/")
    
    if response:
        repositories = response.get('results', [])
        print(f"Repositories for {DOCKER_HUB_USERNAME}:")
        for repo in repositories:
            print(f"- {repo['name']}: {repo.get('description', 'No description')}")
            print(f"  Last pushed: {repo.get('last_updated', 'Unknown')}")
            print(f"  Stars: {repo.get('star_count', 0)}, Pulls: {repo.get('pull_count', 0)}")
            print()
        
        return repositories
    return None

def get_repository_details(repository_name):
    """Get details for a specific repository"""
    response = call_api('get', f"/repositories/{DOCKER_HUB_USERNAME}/{repository_name}")
    
    if response:
        print(f"Details for {DOCKER_HUB_USERNAME}/{repository_name}:")
        print(f"Description: {response.get('description', 'No description')}")
        print(f"Stars: {response.get('star_count', 0)}")
        print(f"Pull Count: {response.get('pull_count', 0)}")
        print(f"Last Updated: {response.get('last_updated', 'Unknown')}")
        print(f"Is Private: {response.get('is_private', False)}")
        print()
        
        return response
    return None

def list_tags(repository_name):
    """List all tags for a repository"""
    response = call_api('get', f"/repositories/{DOCKER_HUB_USERNAME}/{repository_name}/tags")
    
    if response:
        tags = response.get('results', [])
        print(f"Tags for {DOCKER_HUB_USERNAME}/{repository_name}:")
        for tag in tags:
            last_updated = tag.get('last_updated', 'Unknown')
            size = tag.get('full_size', 0) / 1_000_000  # Convert to MB
            print(f"- {tag['name']}")
            print(f"  Last updated: {last_updated}")
            print(f"  Size: {size:.2f} MB")
            print()
        
        return tags
    return None

def create_repository(repository_name, is_private=False, description=None):
    """Create a new repository"""
    data = {
        "namespace": DOCKER_HUB_USERNAME,
        "name": repository_name,
        "is_private": is_private
    }
    
    if description:
        data["description"] = description
    else:
        data["description"] = f"Repository created via API on {datetime.datetime.now().strftime('%Y-%m-%d')}"
    
    response = call_api('post', "/repositories/", data)
    
    if response:
        print(f"Repository {DOCKER_HUB_USERNAME}/{repository_name} created successfully!")
        return True
    return False

def delete_repository(repository_name):
    """Delete a repository"""
    # Confirmation for safety
    confirmation = input(f"Are you sure you want to delete {DOCKER_HUB_USERNAME}/{repository_name}? (y/N): ")
    if confirmation.lower() != 'y':
        print("Operation canceled.")
        return False
    
    response = call_api('delete', f"/repositories/{DOCKER_HUB_USERNAME}/{repository_name}")
    
    if response is not None:  # Could be empty dict for successful delete
        print(f"Repository {DOCKER_HUB_USERNAME}/{repository_name} deleted successfully!")
        return True
    return False

def update_repository_description(repository_name, description):
    """Update repository description"""
    data = {
        "description": description
    }
    
    response = call_api('patch', f"/repositories/{DOCKER_HUB_USERNAME}/{repository_name}", data)
    
    if response:
        print(f"Description for {DOCKER_HUB_USERNAME}/{repository_name} updated successfully!")
        return True
    return False

def get_user_info():
    """Get information about the authenticated user"""
    response = call_api('get', f"/users/{DOCKER_HUB_USERNAME}")
    
    if response:
        print(f"User: {response.get('username', 'Unknown')}")
        print(f"Full Name: {response.get('full_name', 'Unknown')}")
        print(f"Location: {response.get('location', 'Unknown')}")
        print(f"Joined: {response.get('date_joined', 'Unknown')}")
        print()
        
        return response
    return None

def main():
    """Main function to parse arguments and execute commands"""
    parser = argparse.ArgumentParser(description='Docker Hub API Client')
    subparsers = parser.add_subparsers(dest='command', help='Commands')
    
    # List repositories command
    list_repos_parser = subparsers.add_parser('list-repos', help='List all repositories')
    
    # Repository details command
    repo_details_parser = subparsers.add_parser('repo-details', help='Get repository details')
    repo_details_parser.add_argument('repository', help='Repository name')
    
    # List tags command
    list_tags_parser = subparsers.add_parser('list-tags', help='List all tags for a repository')
    list_tags_parser.add_argument('repository', help='Repository name')
    
    # Create repository command
    create_repo_parser = subparsers.add_parser('create-repo', help='Create a new repository')
    create_repo_parser.add_argument('repository', help='Repository name')
    create_repo_parser.add_argument('--private', action='store_true', help='Make repository private')
    create_repo_parser.add_argument('--description', help='Repository description')
    
    # Delete repository command
    delete_repo_parser = subparsers.add_parser('delete-repo', help='Delete a repository')
    delete_repo_parser.add_argument('repository', help='Repository name')
    
    # Update description command
    update_desc_parser = subparsers.add_parser('update-desc', help='Update repository description')
    update_desc_parser.add_argument('repository', help='Repository name')
    update_desc_parser.add_argument('description', help='New description')
    
    # User info command
    user_info_parser = subparsers.add_parser('user-info', help='Get user information')
    
    args = parser.parse_args()
    
    # Execute the requested command
    if args.command == 'list-repos':
        list_repositories()
    elif args.command == 'repo-details':
        get_repository_details(args.repository)
    elif args.command == 'list-tags':
        list_tags(args.repository)
    elif args.command == 'create-repo':
        create_repository(args.repository, args.private, args.description)
    elif args.command == 'delete-repo':
        delete_repository(args.repository)
    elif args.command == 'update-desc':
        update_repository_description(args.repository, args.description)
    elif args.command == 'user-info':
        get_user_info()
    else:
        parser.print_help()

if __name__ == "__main__":
    main() 