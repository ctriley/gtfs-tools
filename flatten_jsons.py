import json
import csv
import os
from datetime import datetime

def flatten_json(json_obj, parent_key='', sep='_'):
    items = []
    for k, v in json_obj.items():
        new_key = f"{parent_key}{sep}{k}" if parent_key else k
        if isinstance(v, dict):
            items.extend(flatten_json(v, new_key, sep=sep).items())
        elif isinstance(v, list):
            for i, item in enumerate(v):
                items.extend(flatten_json(item, f"{new_key}{sep}{i}", sep=sep).items())
        else:
            items.append((new_key, v))
    return dict(items)

def combine_jsons_to_csv(input_folder, output_file):
    all_data = []
    fieldnames = set()
    processed_files = 0
    error_files = 0

    print(f"Starting to process JSON files in {input_folder}")

    # Iterate through all JSON files in the input folder
    for filename in os.listdir(input_folder):
        if filename.endswith('.json'):
            try:
                with open(os.path.join(input_folder, filename), 'r') as json_file:
                    data = json.load(json_file)
                    
                    # Flatten the JSON structure
                    flattened_data = flatten_json(data)
                    
                    # Update fieldnames
                    fieldnames.update(flattened_data.keys())
                    
                    # Append flattened data to the list
                    all_data.append(flattened_data)
                    
                processed_files += 1
                print(f"Processed: {filename}")
            except json.JSONDecodeError:
                print(f"Error: {filename} is not a valid JSON file. Skipping.")
                error_files += 1
            except Exception as e:
                print(f"Error processing {filename}: {str(e)}")
                error_files += 1

    if not all_data:
        print("No valid JSON files were found or processed. Exiting.")
        return

    print(f"\nWriting data to {output_file}")

    # Write the combined data to a CSV file
    try:
        with open(output_file, 'w', newline='') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=sorted(fieldnames))
            writer.writeheader()
            for row in all_data:
                writer.writerow(row)
        print(f"Successfully wrote data to {output_file}")
    except Exception as e:
        print(f"Error writing to CSV file: {str(e)}")

    print(f"\nSummary:")
    print(f"Total files processed: {processed_files}")
    print(f"Files with errors: {error_files}")

# Usage
input_folder = 'extracted_jsons'
output_file = 'combined_data.csv'

try:
    combine_jsons_to_csv(input_folder, output_file)
except Exception as e:
    print(f"An unexpected error occurred: {str(e)}")

print("Script execution completed.")