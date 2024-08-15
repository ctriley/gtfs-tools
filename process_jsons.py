import os
import json
import pandas as pd
from glob import glob

def process_json(file_path):
    with open(file_path, 'r') as file:
        data = json.load(file)
        
    entities = []
    for entity in data.get('entity', []):
        vehicle = entity.get('vehicle', {})
        trip = vehicle.get('trip', {})
        position = vehicle.get('position', {})
        vehicle_info = vehicle.get('vehicle', {})
        
        entities.append({
            'id': entity.get('id'),
            'tripId': trip.get('tripId'),
            'latitude': position.get('latitude'),
            'longitude': position.get('longitude'),
            'bearing': position.get('bearing'),
            'speed': position.get('speed'),
            'timestamp': vehicle.get('timestamp'),
            'vehicleId': vehicle_info.get('id'),
            'header_timestamp': data['header'].get('timestamp')
        })
    
    return entities

# Path to the folder containing JSON files
folder_path = 'gtfs-tools/extracted_jsons'

# Get all JSON files in the folder
json_files = glob(os.path.join(folder_path, '*.json'))

# Process all JSON files
all_entities = []
for file in json_files:
    all_entities.extend(process_json(file))

# Create a DataFrame
df = pd.DataFrame(all_entities)

# Display the first few rows of the DataFrame
print(df.head())

# Save the DataFrame to a CSV file
output_path = 'gtfs-tools/combined_data.csv'
df.to_csv(output_path, index=False)
print(f"Data saved to {output_path}")