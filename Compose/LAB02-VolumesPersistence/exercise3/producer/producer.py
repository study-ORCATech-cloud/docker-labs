import numpy as np
import pandas as pd
import time
import os
import json
from datetime import datetime

# Shared data directory (mounted volume)
SHARED_DIR = '/shared-data'

def ensure_directory_exists():
    """Ensure the shared directory exists"""
    if not os.path.exists(SHARED_DIR):
        os.makedirs(SHARED_DIR)
        print(f"Created directory: {SHARED_DIR}")

def generate_data():
    """Generate random data for demonstration"""
    # Generate random data points
    num_records = np.random.randint(5, 15)
    data = {
        'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        'values': np.random.rand(num_records).tolist(),
        'labels': [f'item_{i}' for i in range(num_records)]
    }
    return data

def save_data_to_csv(data, iteration):
    """Save data to CSV file in the shared volume"""
    # Create a DataFrame from the data
    df = pd.DataFrame({
        'label': data['labels'],
        'value': data['values'],
        'timestamp': data['timestamp']
    })
    
    # Save to CSV
    csv_path = os.path.join(SHARED_DIR, f'data_{iteration}.csv')
    df.to_csv(csv_path, index=False)
    print(f"Data saved to CSV: {csv_path}")
    
    # Also save metadata
    metadata = {
        'filename': f'data_{iteration}.csv',
        'record_count': len(data['values']),
        'created_at': data['timestamp'],
        'description': f'Sample data batch #{iteration}'
    }
    
    metadata_path = os.path.join(SHARED_DIR, f'metadata_{iteration}.json')
    with open(metadata_path, 'w') as f:
        json.dump(metadata, f, indent=2)
    print(f"Metadata saved to: {metadata_path}")
    
    # Create a flag file to signal that new data is available
    flag_file = os.path.join(SHARED_DIR, 'new_data_available.flag')
    with open(flag_file, 'w') as f:
        f.write(f"New data available: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

def main():
    """Main function that runs in a loop to continuously generate data"""
    ensure_directory_exists()
    print("Data producer started. Writing to shared volume...")
    
    iteration = 1
    while True:
        print(f"\n--- Producing data batch #{iteration} ---")
        data = generate_data()
        save_data_to_csv(data, iteration)
        
        # Summary log file that keeps track of all generated files
        log_path = os.path.join(SHARED_DIR, 'producer_log.txt')
        with open(log_path, 'a') as f:
            f.write(f"Batch #{iteration}: Generated {len(data['values'])} records at {data['timestamp']}\n")
        
        # Wait before generating next batch
        sleep_time = np.random.randint(10, 20)
        print(f"Sleeping for {sleep_time} seconds...")
        time.sleep(sleep_time)
        iteration += 1

if __name__ == "__main__":
    main() 