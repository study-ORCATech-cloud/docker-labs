#!/usr/bin/env python3
"""
Secrets Manager for Docker Compose Applications
This tool securely manages secrets for applications running in Docker Compose
without requiring Docker Swarm.
"""

import os
import sys
import argparse
import logging
import json
import base64
import subprocess
import time
from typing import Dict, Optional, List, Any
import hashlib
import getpass

try:
    from Crypto.Cipher import AES
    from Crypto.Util.Padding import pad, unpad
    from Crypto.Random import get_random_bytes
except ImportError:
    print("Error: pycryptodome package is required")
    print("Please install with: pip install pycryptodome")
    sys.exit(1)

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger("secrets-manager")

# Default locations
DEFAULT_SECRETS_DIR = os.environ.get("SECRETS_DIR", "/app/secrets")
DEFAULT_ENV_FILE = ".env.secrets"
SECRET_KEY_ENV_VAR = "SECRETS_ENCRYPTION_KEY"

# Memory-only secrets store
_secrets_store = {}


def derive_key(password: str, salt: bytes) -> bytes:
    """Derive a secure encryption key from a password"""
    return hashlib.pbkdf2_hmac('sha256', password.encode(), salt, 100000)


def encrypt_secret(value: str, key: bytes) -> Dict[str, str]:
    """Encrypt a secret value"""
    iv = get_random_bytes(16)
    cipher = AES.new(key, AES.MODE_CBC, iv)
    encrypted = cipher.encrypt(pad(value.encode(), AES.block_size))
    return {
        'iv': base64.b64encode(iv).decode('utf-8'),
        'data': base64.b64encode(encrypted).decode('utf-8')
    }


def decrypt_secret(encrypted: Dict[str, str], key: bytes) -> str:
    """Decrypt a secret value"""
    iv = base64.b64decode(encrypted['iv'])
    encrypted_data = base64.b64decode(encrypted['data'])
    cipher = AES.new(key, AES.MODE_CBC, iv)
    decrypted = unpad(cipher.decrypt(encrypted_data), AES.block_size)
    return decrypted.decode('utf-8')


def get_encryption_key() -> bytes:
    """Get or generate the encryption key"""
    key = os.environ.get(SECRET_KEY_ENV_VAR)
    
    if not key:
        # For demo purposes, use a fixed key if not provided
        # In production, you'd want to manage this key securely
        logger.warning("Using default encryption key - NOT SECURE FOR PRODUCTION")
        key = "default_encryption_key_for_demo_only"
    
    # Derive a secure key from the provided value
    salt = b'SecureSecretsManagerSalt'  # In production, this should be stored securely
    return derive_key(key, salt)


def load_secrets_from_directory(directory: str = DEFAULT_SECRETS_DIR) -> Dict[str, str]:
    """Load and decrypt secrets from directory"""
    secrets = {}
    key = get_encryption_key()
    
    if not os.path.exists(directory):
        logger.warning(f"Secrets directory {directory} does not exist")
        return secrets
    
    logger.info(f"Loading secrets from {directory}")
    
    try:
        # First look for a secrets index file
        index_path = os.path.join(directory, "secrets.json")
        if os.path.exists(index_path):
            with open(index_path, 'r') as f:
                secret_files = json.load(f)
                
            for secret_name, filename in secret_files.items():
                file_path = os.path.join(directory, filename)
                if os.path.exists(file_path):
                    with open(file_path, 'r') as f:
                        encrypted_data = json.load(f)
                        secrets[secret_name] = decrypt_secret(encrypted_data, key)
                else:
                    logger.warning(f"Secret file {filename} referenced in index but not found")
        
        # Then load individual secret files (*.secret.json)
        for file in os.listdir(directory):
            if file.endswith(".secret.json") and not file.startswith("_"):
                secret_name = file.rsplit(".", 2)[0]  # Remove .secret.json
                file_path = os.path.join(directory, file)
                
                with open(file_path, 'r') as f:
                    encrypted_data = json.load(f)
                    secrets[secret_name] = decrypt_secret(encrypted_data, key)
        
        logger.info(f"Loaded {len(secrets)} secrets")
        
    except Exception as e:
        logger.error(f"Error loading secrets: {e}")
    
    return secrets


def create_encrypted_secret_file(secret_name: str, secret_value: str, directory: str = DEFAULT_SECRETS_DIR) -> str:
    """Create an encrypted secret file"""
    # Ensure directory exists
    os.makedirs(directory, exist_ok=True)
    
    key = get_encryption_key()
    encrypted = encrypt_secret(secret_value, key)
    
    # Create secret file
    filename = f"{secret_name}.secret.json"
    file_path = os.path.join(directory, filename)
    
    with open(file_path, 'w') as f:
        json.dump(encrypted, f)
    
    # Set appropriate permissions
    try:
        os.chmod(file_path, 0o600)  # Only owner can read/write
    except Exception as e:
        logger.warning(f"Could not set permissions on {file_path}: {e}")
    
    return file_path


def get_secret(name: str, default: str = "") -> str:
    """Get a secret from the secrets store"""
    global _secrets_store
    
    if not _secrets_store:
        _secrets_store = load_secrets_from_directory()
    
    return _secrets_store.get(name, default)


def run_application(app_path: str, args: List[str] = None) -> None:
    """Run the target application with secrets available"""
    if not os.path.exists(app_path):
        logger.error(f"Application {app_path} not found")
        sys.exit(1)
    
    logger.info(f"Running application: {app_path}")
    
    # Prepare environment with secrets available in memory
    env = os.environ.copy()
    
    # Make secrets available to the app via an import hook
    # In real production code, you'd use a more robust method
    module_code = """
import builtins
import os

# Store original import
original_import = builtins.__import__

def get_secret(name, default=""):
    from secrets_manager import get_secret as get_secret_impl
    return get_secret_impl(name, default)

# Make get_secret available to the application
builtins.get_secret = get_secret

# Continue with normal imports
builtins.__import__ = original_import
"""
    
    with open("_secrets_hook.py", "w") as f:
        f.write(module_code)
    
    # Run the application with the secrets hook
    cmd = [sys.executable, "-m", "_secrets_hook", app_path]
    if args:
        cmd.extend(args)
    
    try:
        process = subprocess.Popen(cmd)
        process.wait()
    except KeyboardInterrupt:
        logger.info("Application terminated by user")
    finally:
        # Clean up
        if os.path.exists("_secrets_hook.py"):
            try:
                os.remove("_secrets_hook.py")
            except:
                pass


def main():
    """Main entry point"""
    parser = argparse.ArgumentParser(description="Secrets Manager for Docker Compose")
    subparsers = parser.add_subparsers(dest="command", help="Command to execute")
    
    # Create secret command
    create_parser = subparsers.add_parser("create", help="Create a new secret")
    create_parser.add_argument("name", help="Name of the secret")
    create_parser.add_argument("--value", help="Value of the secret (if not provided, will prompt)")
    create_parser.add_argument("--directory", default=DEFAULT_SECRETS_DIR, help="Secrets directory")
    
    # List secrets command
    list_parser = subparsers.add_parser("list", help="List available secrets")
    list_parser.add_argument("--directory", default=DEFAULT_SECRETS_DIR, help="Secrets directory")
    
    # Get secret command
    get_parser = subparsers.add_parser("get", help="Get a secret value")
    get_parser.add_argument("name", help="Name of the secret")
    get_parser.add_argument("--directory", default=DEFAULT_SECRETS_DIR, help="Secrets directory")
    
    # Run application command
    run_parser = subparsers.add_parser("run", help="Run an application with secrets available")
    run_parser.add_argument("application", help="Path to the application to run")
    run_parser.add_argument("args", nargs="*", help="Arguments to pass to the application")
    run_parser.add_argument("--directory", default=DEFAULT_SECRETS_DIR, help="Secrets directory")
    
    args = parser.parse_args()
    
    if args.command == "create":
        value = args.value
        if not value:
            value = getpass.getpass(f"Enter value for secret '{args.name}': ")
        
        create_encrypted_secret_file(args.name, value, args.directory)
        logger.info(f"Secret '{args.name}' created successfully")
        
    elif args.command == "list":
        secrets = load_secrets_from_directory(args.directory)
        if secrets:
            print("Available secrets:")
            for name in secrets.keys():
                print(f"  - {name}")
        else:
            print("No secrets found")
            
    elif args.command == "get":
        secrets = load_secrets_from_directory(args.directory)
        if args.name in secrets:
            print(secrets[args.name])
        else:
            logger.error(f"Secret '{args.name}' not found")
            sys.exit(1)
            
    elif args.command == "run":
        # Load secrets from directory
        global _secrets_store
        _secrets_store = load_secrets_from_directory(args.directory)
        
        # Run the application
        run_application(args.application, args.args)
        
    else:
        parser.print_help()


if __name__ == "__main__":
    main() 