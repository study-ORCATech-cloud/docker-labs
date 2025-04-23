from fastapi import FastAPI, HTTPException, Depends, Header
from pydantic import BaseModel
import redis
import os
import logging
from typing import Optional, Dict, List

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(title="Secrets Manager API")

# Redis connection configuration
redis_host = os.environ.get("REDIS_HOST", "secrets-store")
redis_port = int(os.environ.get("REDIS_PORT", 6379))
redis_password = os.environ.get("REDIS_PASSWORD", "secretstorepwd")
api_key = os.environ.get("API_KEY", "api_key_for_secrets_manager")

# Initialize Redis client
redis_client = redis.Redis(
    host=redis_host,
    port=redis_port,
    password=redis_password,
    db=0,
    decode_responses=True
)

# Make sure API is secure with API key
def verify_api_key(x_api_key: str = Header(...)):
    if x_api_key != api_key:
        raise HTTPException(status_code=401, detail="Invalid API Key")
    return x_api_key

# Models for request and response
class Secret(BaseModel):
    name: str
    value: str
    ttl: Optional[int] = None  # Time to live in seconds (optional)

class SecretName(BaseModel):
    name: str

class SecretResponse(BaseModel):
    name: str
    exists: bool
    value: Optional[str] = None

@app.get("/")
async def root():
    return {"message": "Secrets Manager API", "version": "1.0"}

@app.get("/health")
async def health():
    try:
        # Check Redis connection
        redis_client.ping()
        return {"status": "healthy", "redis_connected": True}
    except Exception as e:
        logger.error(f"Health check failed: {e}")
        return {"status": "unhealthy", "redis_connected": False, "error": str(e)}

@app.post("/secrets", status_code=201)
async def create_secret(secret: Secret, _: str = Depends(verify_api_key)):
    """Create or update a secret in the store"""
    try:
        if secret.ttl:
            redis_client.setex(secret.name, secret.ttl, secret.value)
        else:
            redis_client.set(secret.name, secret.value)
        logger.info(f"Secret '{secret.name}' created/updated successfully")
        return {"status": "success", "message": f"Secret '{secret.name}' stored successfully"}
    except Exception as e:
        logger.error(f"Failed to store secret: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to store secret: {str(e)}")

@app.get("/secrets/{name}")
async def get_secret(name: str, x_api_key: str = Header(...)):
    """Get a secret by name"""
    # Verify API key
    verify_api_key(x_api_key)
    
    try:
        value = redis_client.get(name)
        if value is None:
            return {"name": name, "exists": False}
        return {"name": name, "exists": True, "value": value}
    except Exception as e:
        logger.error(f"Failed to retrieve secret: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to retrieve secret: {str(e)}")

@app.delete("/secrets/{name}")
async def delete_secret(name: str, _: str = Depends(verify_api_key)):
    """Delete a secret by name"""
    try:
        deleted = redis_client.delete(name)
        if deleted == 0:
            return {"status": "warning", "message": f"Secret '{name}' not found"}
        return {"status": "success", "message": f"Secret '{name}' deleted successfully"}
    except Exception as e:
        logger.error(f"Failed to delete secret: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to delete secret: {str(e)}")

@app.get("/secrets")
async def list_secrets(_: str = Depends(verify_api_key)):
    """List all secret names (not values)"""
    try:
        # Use scan to safely iterate over all keys
        keys = []
        cursor = 0
        while True:
            cursor, partial_keys = redis_client.scan(cursor=cursor, count=100)
            keys.extend(partial_keys)
            if cursor == 0:
                break
        
        return {"secrets": keys, "count": len(keys)}
    except Exception as e:
        logger.error(f"Failed to list secrets: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to list secrets: {str(e)}")

# Initialize default secrets when the app starts
@app.on_event("startup")
async def startup_event():
    logger.info("Initializing secrets manager API")
    try:
        # Check if secrets already exist
        if not redis_client.exists("db_password") and not redis_client.exists("api_key"):
            # Create default secrets
            default_secrets = {
                "db_password": "redis_secret_db_password",
                "api_key": "redis_secret_api_key_12345",
                "jwt_secret": "redis_secret_jwt_token_67890"
            }
            
            for name, value in default_secrets.items():
                redis_client.set(name, value)
                logger.info(f"Created default secret: {name}")
            
            logger.info("Default secrets initialized")
        else:
            logger.info("Secrets already exist, skipping initialization")
    except Exception as e:
        logger.error(f"Failed to initialize default secrets: {e}")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000) 