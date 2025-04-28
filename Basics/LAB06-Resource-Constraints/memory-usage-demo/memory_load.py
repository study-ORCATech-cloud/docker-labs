#!/usr/bin/env python3
"""
Memory Load Generator

This script generates memory load by allocating memory in increments.
It can be used to demonstrate Docker memory resource constraints.
"""

import os
import time
import argparse
import psutil
import resource
import gc
from datetime import datetime


class MemoryLoadGenerator:
    """Class for generating controlled memory load."""
    
    def __init__(self, max_memory_mb=1024, increment_mb=10, sleep_sec=1, verbose=True):
        """Initialize the memory load generator.
        
        Args:
            max_memory_mb: Maximum memory to allocate in MB
            increment_mb: Size of each memory increment in MB
            sleep_sec: Seconds to sleep between increments
            verbose: Whether to print status messages
        """
        self.max_memory_mb = max_memory_mb
        self.increment_mb = increment_mb
        self.sleep_sec = sleep_sec
        self.verbose = verbose
        self.memory_blocks = []
    
    def get_current_memory_usage(self):
        """Get current memory usage of this process in MB."""
        process = psutil.Process(os.getpid())
        memory_info = process.memory_info()
        return memory_info.rss / (1024 * 1024)  # Convert to MB
    
    def get_memory_limit(self):
        """Try to detect the memory limit from cgroups or system."""
        try:
            # Try reading the cgroups limit (when running in Docker)
            with open('/sys/fs/cgroup/memory/memory.limit_in_bytes', 'r') as f:
                limit_bytes = int(f.read().strip())
                # Check if limit is set (not equal to huge number)
                if limit_bytes < 2**60:  # A reasonable upper limit
                    return limit_bytes / (1024 * 1024)  # Convert to MB
        except:
            pass
            
        # If no cgroups limit is found, use system memory
        return psutil.virtual_memory().total / (1024 * 1024)
    
    def print_status(self, allocated_mb, current_usage_mb):
        """Print the current status of memory allocation."""
        if not self.verbose:
            return
            
        detected_limit = self.get_memory_limit()
        percent_of_limit = (current_usage_mb / detected_limit) * 100 if detected_limit else 0
        
        print(f"Allocated: {allocated_mb:.1f} MB | "
              f"Actual usage: {current_usage_mb:.1f} MB | "
              f"Target: {self.max_memory_mb} MB | "
              f"Detected limit: {detected_limit:.1f} MB | "
              f"Usage: {percent_of_limit:.1f}%")
    
    def run(self):
        """Run the memory load generation process."""
        print(f"=== Memory Load Generator ===")
        print(f"Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"Process ID: {os.getpid()}")
        print(f"Docker Container: Running in Docker environment: {os.path.exists('/.dockerenv')}")
        print(f"Configuration: Max: {self.max_memory_mb} MB, Increment: {self.increment_mb} MB")
        print(f"System memory: {psutil.virtual_memory().total / (1024 * 1024):.1f} MB")
        print(f"Detected limit: {self.get_memory_limit():.1f} MB")
        print(f"============================")
        
        start_time = time.time()
        allocated_mb = 0
        
        try:
            # Loop until we reach the target memory allocation
            while allocated_mb < self.max_memory_mb:
                # Allocate a block of memory (in bytes)
                memory_block = bytearray(self.increment_mb * 1024 * 1024)
                self.memory_blocks.append(memory_block)
                
                # Update and display allocation stats
                allocated_mb += self.increment_mb
                current_usage_mb = self.get_current_memory_usage()
                self.print_status(allocated_mb, current_usage_mb)
                
                # Sleep between allocations
                time.sleep(self.sleep_sec)
                
            elapsed_time = time.time() - start_time
            print(f"\nFinished allocating {allocated_mb} MB in {elapsed_time:.1f} seconds")
            print(f"Final memory usage: {self.get_current_memory_usage():.1f} MB")
            
            # Hold the memory for a while
            print(f"\nHolding memory for 30 seconds...")
            for i in range(30):
                time.sleep(1)
                # Print a dot every second to show the program is still running
                print(".", end="", flush=True)
                if (i + 1) % 10 == 0:
                    print(f" {i + 1}s", flush=True)
            
        except MemoryError:
            print(f"\nMemory Error occurred at {allocated_mb} MB allocation!")
            print(f"Current memory usage: {self.get_current_memory_usage():.1f} MB")
            
        except KeyboardInterrupt:
            print(f"\nUser interrupted at {allocated_mb} MB allocation")
            print(f"Current memory usage: {self.get_current_memory_usage():.1f} MB")
            
        finally:
            # Clean up
            print(f"\nCleaning up allocated memory...")
            self.memory_blocks = []
            gc.collect()
            print(f"Final memory usage after cleanup: {self.get_current_memory_usage():.1f} MB")
            print(f"Total runtime: {time.time() - start_time:.1f} seconds")


def main():
    """Parse arguments and run the memory load generator."""
    parser = argparse.ArgumentParser(description='Generate memory load for testing Docker resource constraints')
    parser.add_argument('--max-memory', type=int, default=512, 
                        help='Maximum memory to allocate in MB (default: 512)')
    parser.add_argument('--increment', type=int, default=10, 
                        help='Size of each memory increment in MB (default: 10)')
    parser.add_argument('--sleep', type=float, default=0.5, 
                        help='Seconds to sleep between increments (default: 0.5)')
    parser.add_argument('--quiet', action='store_true', 
                        help='Reduce output verbosity')
    
    args = parser.parse_args()
    
    # Create and run the memory load generator
    generator = MemoryLoadGenerator(
        max_memory_mb=args.max_memory,
        increment_mb=args.increment,
        sleep_sec=args.sleep,
        verbose=not args.quiet
    )
    generator.run()


if __name__ == "__main__":
    main() 