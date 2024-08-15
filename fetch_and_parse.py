import requests
import time
import json
from google.protobuf.json_format import MessageToJson
from template_pb2 import FeedMessage
import os

def fetch_mbta_gtfs_rt_data(url):
    response = requests.get(url)
    if response.status_code == 200:
        feed = FeedMessage()
        feed.ParseFromString(response.content)
        return feed
    else:
        print(f"Failed to fetch data: HTTP {response.status_code}")
        return None

def process_feed(feed):
    json_feed = json.loads(MessageToJson(feed))
    
    # Extract relevant information
    processed_data = {
        "header": json_feed["header"],
        "entity": []
    }
    
    for entity in json_feed.get("entity", []):
        if "tripUpdate" in entity:
            processed_entity = {
                "id": entity["id"],
                "tripUpdate": {
                    "trip": entity["tripUpdate"]["trip"],
                    "stopTimeUpdate": entity["tripUpdate"].get("stopTimeUpdate", [])
                }
            }
            processed_data["entity"].append(processed_entity)
    
    return processed_data

def save_to_json(data, filename):
    directory = "extracted_jsons"
    os.makedirs(directory, exist_ok=True)  # Ensure the directory exists
    
    filepath = os.path.join(directory, filename)  # Create the full path for the file
    
    with open(filepath, "w") as json_file:
        json.dump(data, json_file, indent=2)


def fetch_and_save_data():
    trip_updates_url = "https://cdn.mbta.com/realtime/TripUpdates.pb"
    vehicle_positions_url = "https://cdn.mbta.com/realtime/VehiclePositions.pb"
    trip_updates_feed = json.loads(MessageToJson(fetch_mbta_gtfs_rt_data(trip_updates_url)))
    vehicle_positions_feed = json.loads(MessageToJson(fetch_mbta_gtfs_rt_data(vehicle_positions_url)))

    if trip_updates_feed and vehicle_positions_feed:
        # vehicle_processed_data = process_feed(vehicle_positions_feed)
        # trip_processed_data = process_feed(trip_updates_feed)
        timestamp = int(time.time())
        save_to_json(trip_updates_feed, f"mbta_trip_updates_{timestamp}.json")
        save_to_json(vehicle_positions_feed, f"mbta_vehicle_positions_{timestamp}.json")
        print(f"Data saved to mbta_trip_updates_{timestamp}.json")
    else:
        print("Failed to fetch and process data")

# Fetch and save data every minute for 30 minutes
start_time = time.time()
while (time.time() - start_time) < 1800:  # 30 minutes
    fetch_and_save_data()
    time.sleep(60)  # Wait for 1 minute before fetching again

print("Finished fetching data for 30 minutes.")
