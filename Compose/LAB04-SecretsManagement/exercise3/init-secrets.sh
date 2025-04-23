#!/bin/bash
# Initialize secrets in Redis for Exercise 3

# Set up colors for output
GREEN='\033[0;32m'
YELLOW='\033[0;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo -e "${BLUE}=== Redis Secrets Store Setup ===${NC}"

# Ensure all containers are running
echo -e "${YELLOW}Checking if containers are running...${NC}"
docker compose ps

# Wait for the secrets-api container to be ready
echo -e "${YELLOW}Waiting for the secrets API to be ready...${NC}"
max_attempts=10
attempt=1
while [ $attempt -le $max_attempts ]; do
    echo -e "${YELLOW}Attempt $attempt/${max_attempts}...${NC}"
    if curl -s http://localhost:8088/health | grep -q "healthy"; then
        echo -e "${GREEN}Secrets API is ready!${NC}"
        break
    else
        echo -e "${YELLOW}Secrets API not ready yet, waiting...${NC}"
        sleep 5
        attempt=$((attempt + 1))
    fi
done

if [ $attempt -gt $max_attempts ]; then
    echo -e "${YELLOW}Timed out waiting for Secrets API. Continuing anyway...${NC}"
fi

# Create some default secrets
echo -e "${BLUE}Setting up default secrets...${NC}"

# API Key for accessing the secrets API
API_KEY="${API_KEY:-api_key_for_secrets_manager}"

# Function to create a secret
create_secret() {
    local name=$1
    local value=$2
    
    echo -e "${YELLOW}Creating/updating secret: ${name}${NC}"
    curl -s -X POST \
      -H "Content-Type: application/json" \
      -H "X-API-Key: $API_KEY" \
      -d "{\"name\":\"$name\",\"value\":\"$value\"}" \
      http://localhost:8088/secrets
      
    echo ""
}

# Create default secrets
create_secret "db_password" "redis_secret_db_password_example"
create_secret "api_key" "redis_secret_api_key_example_12345"
create_secret "jwt_secret" "redis_secret_jwt_token_example_67890"

echo -e "${GREEN}=== Secrets setup completed! ===${NC}"
echo -e "${YELLOW}You can access the application at: http://localhost:8003${NC}"
echo -e "${YELLOW}You can access the secrets API at: http://localhost:8088${NC}"
echo -e "${YELLOW}You can view API documentation at: http://localhost:8088/docs${NC}" 