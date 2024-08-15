import os
import json
import pandas as pd
from pandas import json_normalize
from datetime import datetime

def safe_get_first_stop_time(x):
    if isinstance(x, list) and len(x) > 0:
        first_stop = x[0]
        if isinstance(first_stop, dict) and 'departure' in first_stop:
            return first_stop['departure'].get('time')
    return None

def flatten_jsons(folder_path):
    all_data = []

    for filename in os.listdir(folder_path):
        if filename.endswith('.json'):
            file_path = os.path.join(folder_path, filename)
            
            with open(file_path, 'r') as file:
                data = json.load(file)
            
            # Flatten the nested structure
            flattened_data = json_normalize(data['entity'])
            
            # Add filename as a column
            flattened_data['source_file'] = filename
            
            all_data.append(flattened_data)

    # Combine all dataframes
    combined_df = pd.concat(all_data, ignore_index=True)
    
    # Convert timestamp to readable format
    for col in combined_df.columns:
        if 'timestamp' in col:
            combined_df[col] = pd.to_datetime(combined_df[col].astype(float), unit='s', errors='coerce')
    
    # Extract first stop time update
    combined_df['first_stop_time'] = combined_df['tripUpdate.stopTimeUpdate'].apply(safe_get_first_stop_time)
    combined_df['first_stop_time'] = pd.to_datetime(combined_df['first_stop_time'].astype(float), unit='s', errors='coerce')
    
    # Drop the original stopTimeUpdate column as it's now processed
    combined_df = combined_df.drop('tripUpdate.stopTimeUpdate', axis=1)
    
    return combined_df

if __name__ == "__main__":
    folder_path = "extracted_jsons"
    result_df = flatten_jsons(folder_path)
    
    # Display the first few rows of the result
    print(result_df.head())
    
    # Save the result to a CSV file
    result_df.to_csv("flattened_data.csv", index=False)
    print("Data has been saved to flattened_data.csv")