#!/usr/bin/env python3
"""
Docker Logging Demo Application

This application demonstrates different logging approaches and techniques
that can be used with Docker containers.
"""

import logging
import random
import time
import os
import sys
import datetime
import threading

# Configure basic logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)

logger = logging.getLogger(__name__)

# Different log messages by level
ERROR_MESSAGES = [
    "Failed to connect to database",
    "Connection timeout after 30 seconds",
    "Authentication failed: Invalid credentials",
    "Permission denied: Insufficient privileges",
    "File not found: /data/config.yaml",
    "Out of memory error during operation",
    "Failed to process request: Invalid format",
    "Network error: Unable to reach service",
    "Unexpected error in module: Data corruption",
    "Disk space full: Cannot write to log"
]

WARNING_MESSAGES = [
    "Database connection slow (took 2532ms)",
    "Memory usage at 85% threshold",
    "Request rate approaching limit (950/1000)",
    "Retrying operation (attempt 3/5)",
    "Cache hit ratio below threshold (45%)",
    "Deprecated API call detected",
    "Configuration value using default",
    "Task took longer than expected (5432ms)",
    "Invalid parameter ignored",
    "Response time degraded (avg: 850ms)"
]

INFO_MESSAGES = [
    "Application started successfully",
    "Processing batch #12345 (50 items)",
    "User login successful: user123",
    "Cache refreshed (10245 entries)",
    "Scheduled task completed in 1.5s",
    "New connection accepted from 192.168.1.5",
    "Configuration loaded from /etc/app/config.json",
    "API request received: GET /api/v1/users",
    "Database query executed in 123ms",
    "Request processed successfully (id: req-123)"
]

DEBUG_MESSAGES = [
    "Initializing module MyModule v1.2",
    "Connection parameters: host=db.example.com, port=5432",
    "Query executed: SELECT * FROM users WHERE id = 123",
    "Response payload: {\"status\": \"success\"}",
    "Thread pool status: 4/10 active",
    "Cache lookup for key: user:profile:123",
    "Temp file created: /tmp/app-12345.tmp",
    "HTTP headers received: Content-Type=application/json",
    "Function call stack: get_user() -> validate() -> format()",
    "Memory allocated: 25MB for operation"
]

def generate_random_log():
    """Generate a random log message with random level."""
    level = random.choices(
        ["DEBUG", "INFO", "WARNING", "ERROR"],
        weights=[15, 65, 15, 5],
        k=1
    )[0]
    
    if level == "ERROR":
        message = random.choice(ERROR_MESSAGES)
        logger.error(message)
    elif level == "WARNING":
        message = random.choice(WARNING_MESSAGES)
        logger.warning(message)
    elif level == "INFO":
        message = random.choice(INFO_MESSAGES)
        logger.info(message)
    else:  # DEBUG
        message = random.choice(DEBUG_MESSAGES)
        logger.debug(message)
    
    # Simulate processing time
    processing_time = random.uniform(0.01, 2.0)
    if level == "INFO":
        logger.info(f"Request processing time: {processing_time:.3f}s")
    
    return level, message, processing_time

def simulate_traffic(interval=1.0):
    """Simulate log traffic at a given rate."""
    logger.info(f"Starting log traffic simulation with {interval:.1f}s interval")
    
    # Counters for log statistics
    counters = {
        "ERROR": 0,
        "WARNING": 0,
        "INFO": 0,
        "DEBUG": 0,
        "total": 0
    }
    
    try:
        start_time = time.time()
        
        # Generate random logs
        while True:
            level, message, _ = generate_random_log()
            counters[level] += 1
            counters["total"] += 1
            
            # Occasionally generate a burst of logs
            if random.random() < 0.05:  # 5% chance
                logger.info("Processing burst of requests")
                for _ in range(random.randint(5, 10)):
                    burst_level, burst_message, _ = generate_random_log()
                    counters[burst_level] += 1
                    counters["total"] += 1
            
            # Log statistics every 50 messages
            if counters["total"] % 50 == 0:
                elapsed = time.time() - start_time
                logger.info(f"Log statistics: {counters} in {elapsed:.1f}s")
            
            # Random delay between log messages
            time.sleep(random.uniform(interval * 0.5, interval * 1.5))
            
    except KeyboardInterrupt:
        logger.info("Log simulation stopped by user")
    except Exception as e:
        logger.error(f"Error in log simulation: {e}")

def simulate_error_scenario():
    """Periodically simulate error scenarios."""
    while True:
        # Sleep for a while before generating the next error scenario
        sleep_time = random.uniform(30, 60)
        time.sleep(sleep_time)
        
        # Simulate different error scenarios
        scenario = random.randint(1, 3)
        
        if scenario == 1:
            # Database connection issue
            logger.error("ERROR: Database connection lost. Reconnecting...")
            for attempt in range(1, 4):
                logger.warning(f"Reconnection attempt {attempt}/3")
                time.sleep(2)
                if random.random() < 0.7:  # 70% chance of success
                    logger.info("Database connection re-established")
                    break
                else:
                    logger.error("Reconnection failed")
            
        elif scenario == 2:
            # API dependency issue
            logger.error("ERROR: External API service unavailable")
            logger.warning("Requests will be queued until service is restored")
            time.sleep(5)
            logger.info("External API service restored, processing queued requests")
            
        else:
            # Resource issue
            logger.warning("Memory usage high (92%), attempting to free resources")
            logger.info("Running garbage collection cycle")
            time.sleep(1)
            if random.random() < 0.3:  # 30% chance of failure
                logger.error("ERROR: Memory allocation failed, some operations will be rejected")
            else:
                logger.info("Resources freed successfully, memory usage now at 78%")

def main():
    """Main function to run the logging demo."""
    logger.info("=" * 50)
    logger.info("Docker Logging Demo Application - Starting")
    logger.info(f"Time: {datetime.datetime.now().isoformat()}")
    logger.info(f"Host: {os.uname().nodename if hasattr(os, 'uname') else 'Unknown'}")
    logger.info(f"PID: {os.getpid()}")
    logger.info(f"Python version: {sys.version}")
    logger.info("=" * 50)
    
    # Parse interval from environment or use default
    try:
        interval = float(os.environ.get("LOG_INTERVAL", "1.0"))
    except ValueError:
        logger.warning("Invalid LOG_INTERVAL value, using default of 1.0s")
        interval = 1.0
    
    # Start error scenario simulator in a separate thread
    error_thread = threading.Thread(target=simulate_error_scenario, daemon=True)
    error_thread.start()
    
    # Start main log traffic simulation
    simulate_traffic(interval)

if __name__ == "__main__":
    main() 