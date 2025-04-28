#!/usr/bin/env python3
"""
DockerHub Tag Cleanup Utility

This script helps manage Docker Hub repositories by automatically deleting old or unused tags
based on age, count limits, or naming patterns.
"""

import requests
import os
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
        elif method.lower() == 'delete':
            response = requests.delete(url, headers=headers)
        else:
            raise ValueError(f"Unsupported method: {method}")
        
        response.raise_for_status()
        return response.json() if response.text else {}
    
    except requests.exceptions.HTTPError as e:
        print(f"HTTP Error: {e}")
        if hasattr(e, 'response') and e.response is not None:
            print(f"Response: {e.response.text}")
        return None
    except Exception as e:
        print(f"Error: {e}")
        return None

def get_repository_tags(repository_name):
    """Get all tags for a repository with pagination support"""
    all_tags = []
    page = 1
    page_size = 100  # Maximum allowed by Docker Hub API
    
    while True:
        params = {
            'page': page,
            'page_size': page_size
        }
        
        response = call_api('get', f"/repositories/{DOCKER_HUB_USERNAME}/{repository_name}/tags", params=params)
        
        if not response or not response.get('results'):
            break
            
        all_tags.extend(response['results'])
        
        # Check if there are more pages
        if page * page_size >= response.get('count', 0):
            break
            
        page += 1
    
    return all_tags

def delete_tag(repository_name, tag_name):
    """Delete a tag from a repository"""
    print(f"Deleting tag {repository_name}:{tag_name}...")
    
    response = call_api('delete', f"/repositories/{DOCKER_HUB_USERNAME}/{repository_name}/tags/{tag_name}")
    
    if response is not None:  # Could be empty dict for successful delete
        print(f"Tag {repository_name}:{tag_name} deleted successfully")
        return True
    
    return False

def cleanup_by_age(repository_name, days_old):
    """Delete tags older than specified days"""
    print(f"Cleaning up tags older than {days_old} days from {repository_name}...")
    
    tags = get_repository_tags(repository_name)
    if not tags:
        print(f"No tags found in repository {repository_name}")
        return
    
    # Calculate the cutoff date
    cutoff_date = datetime.datetime.now(datetime.timezone.utc) - datetime.timedelta(days=days_old)
    
    deleted_count = 0
    protected_tags = ['latest']  # Add any tags you want to protect
    
    for tag in tags:
        tag_name = tag.get('name')
        
        # Skip protected tags
        if tag_name in protected_tags:
            print(f"Skipping protected tag: {tag_name}")
            continue
        
        # Parse the last_updated date
        last_updated_str = tag.get('last_updated')
        if not last_updated_str:
            print(f"No last_updated information for tag {tag_name}, skipping")
            continue
        
        # Convert to datetime object
        try:
            last_updated = datetime.datetime.fromisoformat(last_updated_str.replace('Z', '+00:00'))
        except ValueError:
            print(f"Could not parse date for tag {tag_name}: {last_updated_str}")
            continue
        
        # Check if older than cutoff
        if last_updated < cutoff_date:
            print(f"Tag {tag_name} is older than {days_old} days (last updated: {last_updated_str})")
            if delete_tag(repository_name, tag_name):
                deleted_count += 1
    
    print(f"Cleanup complete. Deleted {deleted_count} tags from {repository_name}")

def cleanup_by_count(repository_name, keep_count):
    """Keep only the specified number of most recent tags"""
    print(f"Cleaning up repository {repository_name}, keeping {keep_count} most recent tags...")
    
    tags = get_repository_tags(repository_name)
    if not tags:
        print(f"No tags found in repository {repository_name}")
        return
    
    # Sort tags by last_updated (most recent first)
    sorted_tags = sorted(
        tags, 
        key=lambda x: x.get('last_updated', '1970-01-01T00:00:00.000000Z'), 
        reverse=True
    )
    
    # Keep the specified number of most recent tags
    tags_to_keep = sorted_tags[:keep_count]
    tags_to_delete = sorted_tags[keep_count:]
    
    # Get names of tags to keep for reporting
    keep_names = [tag.get('name') for tag in tags_to_keep]
    print(f"Keeping these tags: {', '.join(keep_names)}")
    
    # Delete older tags
    deleted_count = 0
    protected_tags = ['latest']  # Add any tags you want to protect
    
    for tag in tags_to_delete:
        tag_name = tag.get('name')
        
        # Skip protected tags
        if tag_name in protected_tags:
            print(f"Skipping protected tag: {tag_name}")
            continue
            
        if delete_tag(repository_name, tag_name):
            deleted_count += 1
    
    print(f"Cleanup complete. Deleted {deleted_count} tags from {repository_name}")

def cleanup_by_pattern(repository_name, pattern):
    """Delete tags matching the specified pattern"""
    import re
    
    print(f"Cleaning up tags matching pattern '{pattern}' from {repository_name}...")
    
    try:
        regex = re.compile(pattern)
    except re.error as e:
        print(f"Invalid regular expression: {e}")
        return
    
    tags = get_repository_tags(repository_name)
    if not tags:
        print(f"No tags found in repository {repository_name}")
        return
    
    deleted_count = 0
    protected_tags = ['latest']  # Add any tags you want to protect
    
    for tag in tags:
        tag_name = tag.get('name')
        
        # Skip protected tags
        if tag_name in protected_tags:
            continue
            
        # Check if tag matches pattern
        if regex.search(tag_name):
            print(f"Tag {tag_name} matches pattern '{pattern}'")
            if delete_tag(repository_name, tag_name):
                deleted_count += 1
    
    print(f"Cleanup complete. Deleted {deleted_count} tags from {repository_name}")

def main():
    """Main function to parse arguments and execute commands"""
    parser = argparse.ArgumentParser(description='Docker Hub Tag Cleanup Utility')
    parser.add_argument('repository', help='Repository name to clean up')
    
    # Create a group for cleanup methods (mutually exclusive)
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument('--age', type=int, help='Delete tags older than specified days')
    group.add_argument('--keep', type=int, help='Keep only the specified number of most recent tags')
    group.add_argument('--pattern', help='Delete tags matching the specified regex pattern')
    
    # Add dry-run option
    parser.add_argument('--dry-run', action='store_true', help='Simulate the cleanup without actually deleting tags')
    
    args = parser.parse_args()
    
    # Handle dry run mode
    global delete_tag
    if args.dry_run:
        print("DRY RUN MODE: No tags will be actually deleted")
        # Save the original function
        original_delete_tag = delete_tag
        # Replace with a version that just logs
        delete_tag = lambda repo, tag: print(f"Would delete tag {repo}:{tag}")
    
    # Execute the requested cleanup method
    if args.age:
        cleanup_by_age(args.repository, args.age)
    elif args.keep:
        cleanup_by_count(args.repository, args.keep)
    elif args.pattern:
        cleanup_by_pattern(args.repository, args.pattern)
    
    # Restore original function if in dry-run mode
    if args.dry_run:
        delete_tag = original_delete_tag

if __name__ == "__main__":
    main() 