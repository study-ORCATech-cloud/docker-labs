import os
import time
import json
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime

# Shared data directory (mounted volume)
SHARED_DIR = '/shared-data'
# Results directory within the shared volume
RESULTS_DIR = os.path.join(SHARED_DIR, 'results')

def ensure_results_directory():
    """Ensure the results directory exists"""
    if not os.path.exists(RESULTS_DIR):
        os.makedirs(RESULTS_DIR)
        print(f"Created results directory: {RESULTS_DIR}")

def check_for_new_data():
    """Check if there's a flag file indicating new data"""
    flag_file = os.path.join(SHARED_DIR, 'new_data_available.flag')
    if os.path.exists(flag_file):
        with open(flag_file, 'r') as f:
            flag_content = f.read()
        print(f"Found new data flag: {flag_content}")
        return True
    return False

def get_unprocessed_data_files():
    """Find data files that haven't been processed yet"""
    all_files = [f for f in os.listdir(SHARED_DIR) if f.startswith('data_') and f.endswith('.csv')]
    
    # Check which files have already been processed
    processed_marker = os.path.join(RESULTS_DIR, 'processed_files.txt')
    processed_files = set()
    
    if os.path.exists(processed_marker):
        with open(processed_marker, 'r') as f:
            processed_files = set(line.strip() for line in f.readlines())
    
    # Return files that haven't been processed
    return [f for f in all_files if f not in processed_files]

def process_data_file(filename):
    """Process a data file and create summary/visualization"""
    file_path = os.path.join(SHARED_DIR, filename)
    print(f"Processing file: {file_path}")
    
    # Read data
    df = pd.read_csv(file_path)
    
    # Create a summary
    summary = {
        'filename': filename,
        'record_count': len(df),
        'processed_at': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        'average_value': df['value'].mean(),
        'min_value': df['value'].min(),
        'max_value': df['value'].max()
    }
    
    # Save summary as JSON
    batch_num = filename.split('_')[1].split('.')[0]
    summary_path = os.path.join(RESULTS_DIR, f'summary_{batch_num}.json')
    with open(summary_path, 'w') as f:
        json.dump(summary, f, indent=2)
    
    # Create a visualization
    plt.figure(figsize=(10, 6))
    plt.bar(df['label'], df['value'])
    plt.title(f'Data Visualization - Batch {batch_num}')
    plt.xlabel('Label')
    plt.ylabel('Value')
    plt.xticks(rotation=45)
    plt.tight_layout()
    
    # Save the plot
    plot_path = os.path.join(RESULTS_DIR, f'plot_{batch_num}.png')
    plt.savefig(plot_path)
    plt.close()
    
    print(f"Created summary: {summary_path}")
    print(f"Created visualization: {plot_path}")
    
    # Mark this file as processed
    processed_marker = os.path.join(RESULTS_DIR, 'processed_files.txt')
    with open(processed_marker, 'a') as f:
        f.write(f"{filename}\n")
    
    # Update the consumer log
    log_path = os.path.join(RESULTS_DIR, 'consumer_log.txt')
    with open(log_path, 'a') as f:
        f.write(f"Processed {filename} at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")

def main():
    """Main function that continuously checks for and processes new data"""
    ensure_results_directory()
    print("Data consumer started. Reading from shared volume...")
    
    # Initial wait to allow producer to generate some data
    time.sleep(5)
    
    while True:
        if check_for_new_data():
            # Clear the flag
            flag_file = os.path.join(SHARED_DIR, 'new_data_available.flag')
            os.remove(flag_file)
            
            # Get unprocessed files
            unprocessed_files = get_unprocessed_data_files()
            
            if unprocessed_files:
                print(f"Found {len(unprocessed_files)} unprocessed file(s).")
                for filename in unprocessed_files:
                    process_data_file(filename)
            else:
                print("No new files to process.")
        else:
            print("No new data flag found.")
        
        # Wait before checking again
        wait_time = 5
        print(f"Sleeping for {wait_time} seconds...")
        time.sleep(wait_time)

if __name__ == "__main__":
    main() 