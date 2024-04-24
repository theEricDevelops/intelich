import os
import re

log_file = '/mnt/c/users/eric/dev/intelich/process_hail_events.log'
data_dir = '/mnt/c/users/eric/dev/intelich/hailmaps/data'
processed_dir = '/mnt/c/users/eric/dev/intelich/hailmaps/data/processed'

# Create the processed directory if it doesn't exist
if not os.path.exists(processed_dir):
    os.makedirs(processed_dir)

with open(log_file, 'r') as f:
    for line in f:
        match = re.search(r'Finished processing file (\d{6})_rpts_raw_hail.csv', line)
        if match:
            filename = match.group(1) + "_rpts_raw_hail.csv"
            source_file = os.path.join(data_dir, filename)
            destination_file = os.path.join(processed_dir, filename)
            if os.path.exists(source_file):
                os.rename(source_file, destination_file)
                print(f"Moved {filename} to processed directory")
            else:
                print(f"File {filename} not found in data directory")

