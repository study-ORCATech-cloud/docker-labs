#!/usr/bin/env python3
"""
Docker Event Monitor - Skeleton

This script provides a skeleton for monitoring Docker events and taking actions
based on specific events. Students will need to implement the missing parts.
"""

import json
import subprocess
import sys
import time
import os
from datetime import datetime

# Configuration
LOG_FILE = "docker_events.log"
STATS_FILE = "event_stats.json"

# TODO: Implement the log_event function to record events to a file
def log_event(event_data):
    """Log the event to a file.
    
    Args:
        event_data: The Docker event data to log
    """
    pass

# TODO: Implement the update_stats function to track event statistics
def update_stats(event_data):
    """Update event statistics.
    
    Args:
        event_data: The Docker event data to track
    """
    pass

# TODO: Implement the send_alert function to notify about critical events
def send_alert(event_data, message):
    """Send an alert for critical events.
    
    Args:
        event_data: The Docker event data
        message: The alert message to send
    """
    pass

# TODO: Implement the handle_event function to process events and take actions
def handle_event(event_data):
    """Process an event and take appropriate actions.
    
    Args:
        event_data: The Docker event data to process
    """
    pass

# TODO: Implement the generate_report function to create event statistics reports
def generate_report():
    """Generate a report of collected event statistics."""
    pass

def main():
    """Main function to monitor Docker events."""
    if len(sys.argv) > 1 and sys.argv[1] == "--report":
        generate_report()
        return
    
    print("Starting Docker event monitor...")
    print(f"Logging events to: {LOG_FILE}")
    
    try:
        # Run docker events command and process the output
        cmd = ["docker", "events", "--format", "{{json .}}"]
        # TODO: Implement the code to run the docker events command and process each event
        
    except KeyboardInterrupt:
        print("\nMonitoring stopped.")
    
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main() 