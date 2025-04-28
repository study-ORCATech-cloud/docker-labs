#!/bin/bash
# Docker Hub Organization Setup Script
# This script demonstrates how to use the Docker Hub API to set up an organization structure

# Load environment variables from .env file if present
if [ -f .env ]; then
    export $(cat .env | grep -v '#' | xargs)
fi

# Check for required environment variables
if [ -z "$DOCKER_HUB_TOKEN" ] || [ -z "$DOCKER_HUB_ORG" ]; then
    echo "Error: Missing required environment variables"
    echo "Please set the following variables:"
    echo "  DOCKER_HUB_TOKEN: Your Docker Hub personal access token"
    echo "  DOCKER_HUB_ORG: Your Docker Hub organization name"
    exit 1
fi

# API Base URL
API_URL="https://hub.docker.com/v2"

# Headers for API calls
HEADERS=(
    -H "Content-Type: application/json"
    -H "Authorization: Bearer $DOCKER_HUB_TOKEN"
)

# Function to make API calls
call_api() {
    local method=$1
    local endpoint=$2
    local data=$3

    if [ -n "$data" ]; then
        curl -s -X "$method" "${API_URL}${endpoint}" "${HEADERS[@]}" -d "$data"
    else
        curl -s -X "$method" "${API_URL}${endpoint}" "${HEADERS[@]}"
    fi
}

# Function to create a team
create_team() {
    local team_name=$1
    local team_description=$2

    echo "Creating team: $team_name"
    
    # Prepare JSON data
    local data="{\"name\":\"$team_name\",\"description\":\"$team_description\",\"permission\":\"read\"}"
    
    # Make API call
    local response=$(call_api "POST" "/orgs/$DOCKER_HUB_ORG/groups/" "$data")
    
    # Check for errors
    if echo "$response" | grep -q "error"; then
        echo "Error creating team: $response"
        return 1
    else
        echo "Team created successfully: $team_name"
        return 0
    fi
}

# Function to add a member to a team
add_team_member() {
    local team_id=$1
    local username=$2
    
    echo "Adding member $username to team ID $team_id"
    
    # Prepare JSON data
    local data="{\"member\":\"$username\"}"
    
    # Make API call
    local response=$(call_api "POST" "/orgs/$DOCKER_HUB_ORG/groups/$team_id/members/" "$data")
    
    # Check for errors
    if echo "$response" | grep -q "error"; then
        echo "Error adding member: $response"
        return 1
    else
        echo "Member added successfully: $username"
        return 0
    fi
}

# Function to create a repository
create_repository() {
    local repo_name=$1
    local is_private=$2
    local description=$3
    
    echo "Creating repository: $repo_name"
    
    # Prepare JSON data
    local data="{\"namespace\":\"$DOCKER_HUB_ORG\",\"name\":\"$repo_name\",\"is_private\":$is_private,\"description\":\"$description\"}"
    
    # Make API call
    local response=$(call_api "POST" "/repositories/" "$data")
    
    # Check for errors
    if echo "$response" | grep -q "error"; then
        echo "Error creating repository: $response"
        return 1
    else
        echo "Repository created successfully: $DOCKER_HUB_ORG/$repo_name"
        return 0
    fi
}

# Function to set repository team permissions
set_repo_team_permission() {
    local repo_name=$1
    local team_id=$2
    local permission=$3  # read, write, admin
    
    echo "Setting $permission permission for team ID $team_id on repository $repo_name"
    
    # Prepare JSON data
    local data="{\"permission\":\"$permission\"}"
    
    # Make API call
    local response=$(call_api "PUT" "/repositories/$DOCKER_HUB_ORG/$repo_name/groups/$team_id" "$data")
    
    # Check for errors
    if echo "$response" | grep -q "error"; then
        echo "Error setting permission: $response"
        return 1
    else
        echo "Permission set successfully"
        return 0
    fi
}

# Function to get team ID by name
get_team_id() {
    local team_name=$1
    
    # Get all teams
    local response=$(call_api "GET" "/orgs/$DOCKER_HUB_ORG/groups/")
    
    # Extract team ID
    local team_id=$(echo "$response" | grep -o "\"id\":[0-9]*,\"name\":\"$team_name\"" | grep -o "[0-9]*")
    
    if [ -z "$team_id" ]; then
        echo "Error: Team not found: $team_name"
        return 1
    else
        echo "$team_id"
        return 0
    fi
}

# Main script execution

echo "Setting up organization structure for $DOCKER_HUB_ORG"

# 1. Create teams
echo "Creating teams..."
create_team "admins" "Organization administrators with full access"
create_team "developers" "Development team with access to dev repositories"
create_team "operations" "Operations team with access to production repositories"
create_team "cicd" "CI/CD systems with push access"

# 2. Create repositories
echo "Creating repositories..."
create_repository "base-image" true "Base Docker image for all applications"
create_repository "app-dev" true "Development version of the application"
create_repository "app-prod" true "Production version of the application"

# 3. Set team permissions
echo "Setting team permissions..."

# Get team IDs
admins_id=$(get_team_id "admins")
developers_id=$(get_team_id "developers")
operations_id=$(get_team_id "operations")
cicd_id=$(get_team_id "cicd")

# Set permissions for base-image repository
set_repo_team_permission "base-image" "$admins_id" "admin"
set_repo_team_permission "base-image" "$developers_id" "read"
set_repo_team_permission "base-image" "$operations_id" "read"
set_repo_team_permission "base-image" "$cicd_id" "write"

# Set permissions for app-dev repository
set_repo_team_permission "app-dev" "$admins_id" "admin"
set_repo_team_permission "app-dev" "$developers_id" "write"
set_repo_team_permission "app-dev" "$operations_id" "read"
set_repo_team_permission "app-dev" "$cicd_id" "write"

# Set permissions for app-prod repository
set_repo_team_permission "app-prod" "$admins_id" "admin"
set_repo_team_permission "app-prod" "$developers_id" "read"
set_repo_team_permission "app-prod" "$operations_id" "write"
set_repo_team_permission "app-prod" "$cicd_id" "write"

echo "Organization setup complete!"
echo "Remember to add team members using the Docker Hub web interface or API"

# Note: In a real script, you would add error handling and checks between each step 