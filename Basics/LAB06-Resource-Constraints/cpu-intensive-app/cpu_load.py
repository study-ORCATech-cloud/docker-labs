#!/usr/bin/env python3
"""
CPU Load Generator

This script generates CPU load by performing calculations that heavily utilize the CPU.
It can be used to demonstrate Docker CPU resource constraints.
"""

import os
import time
import multiprocessing
import argparse
import math
from datetime import datetime


def cpu_intensive_task(duration=60, process_id=0):
    """
    Performs CPU-intensive calculations.
    
    Args:
        duration: How long to run the task (in seconds)
        process_id: ID to identify the current process
    """
    print(f"Process {process_id}: Starting CPU-intensive task for {duration} seconds")
    start_time = time.time()
    end_time = start_time + duration
    
    # Counter for operations
    operations = 0
    
    # Perform CPU-intensive calculations until the duration is reached
    while time.time() < end_time:
        # Perform some arbitrary CPU-intensive calculations
        for i in range(10000):
            # Mix of operations to ensure CPU usage
            math.factorial(20)
            math.sin(i) * math.cos(i)
            math.sqrt(i * i)
        operations += 10000
        
        # Print progress every second
        elapsed = time.time() - start_time
        if int(elapsed) % 5 == 0:
            remaining = duration - elapsed
            print(f"Process {process_id}: {elapsed:.1f}s elapsed, {remaining:.1f}s remaining, {operations:,} operations")
            # Reset counter to avoid too large numbers
            operations = 0
            # Small sleep to allow logging
            time.sleep(0.01)
    
    total_time = time.time() - start_time
    print(f"Process {process_id}: Completed in {total_time:.2f} seconds")
    return total_time


def run_parallel_tasks(num_processes, duration):
    """
    Run multiple CPU-intensive tasks in parallel.
    
    Args:
        num_processes: Number of processes to spawn
        duration: Duration for each process to run
    """
    print(f"Starting {num_processes} CPU-intensive tasks for {duration} seconds each")
    
    # Create a pool of worker processes
    with multiprocessing.Pool(processes=num_processes) as pool:
        # Start timer for overall execution
        start_time = time.time()
        
        # Start all processes
        results = []
        for i in range(num_processes):
            result = pool.apply_async(cpu_intensive_task, (duration, i))
            results.append(result)
        
        # Wait for all processes to complete
        for result in results:
            result.get()
        
        # Calculate total execution time
        total_time = time.time() - start_time
        print(f"All processes completed. Total execution time: {total_time:.2f} seconds")


def main():
    """Main function to parse arguments and start the CPU load generation."""
    parser = argparse.ArgumentParser(description='Generate CPU load for testing Docker resource constraints')
    parser.add_argument('--duration', type=int, default=60, help='Duration in seconds for each CPU task')
    parser.add_argument('--processes', type=int, default=None, 
                        help='Number of parallel processes (defaults to number of CPU cores)')
    
    args = parser.parse_args()
    
    # If processes not specified, use the number of CPU cores
    if args.processes is None:
        args.processes = multiprocessing.cpu_count()
    
    print(f"=== CPU Load Generator ===")
    print(f"Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"Host CPU Count: {multiprocessing.cpu_count()}")
    print(f"Docker Container: Running in Docker environment: {os.path.exists('/.dockerenv')}")
    print(f"Configuration: {args.processes} processes, {args.duration} seconds per process")
    print(f"========================")
    
    # Run the tasks
    run_parallel_tasks(args.processes, args.duration)
    

if __name__ == "__main__":
    main() 