import requests
import time
import json
import protos.alerts_pb2 as alerts_pb2
import protos.trip_updates_pb2 as trip_updates_pb2
import protos.vehicle_positions_pb2 as vehicle_positions_pb2
from google.protobuf.json_format import MessageToJson

def fetch_gps_data():
    # Simulated GPS data; replace with actual data fetching logic
    return [
        {
            "latitude": 37.791898010762964,
            "longitude": -122.3994580905113,
            "bearing": 32.3,
            "vehicleId": "vehicle1",
            "speed": 6.7
        }
        # Add more GPS data as needed
    ]

def match_gps_to_trip(gps_data, gtfs_data):
    # Logic to match GPS data to GTFS trip IDs
    matched_data = []
    for gps in gps_data:
        matched_data.append({
            "trip_id": "trip1",  # Simulated match; replace with actual matching logic
            "vehicle_id": gps["vehicleId"],
            "latitude": gps["latitude"],
            "longitude": gps["longitude"],
            "bearing": gps["bearing"],
            "speed": gps["speed"],
            "timestamp": int(time.time())
        })
    return matched_data

def fetch_gtfs_data():
    # Fetch GTFS static data
    gtfs_url = "https://cdn.mbta.com/MBTA_GTFS.zip"
    response = requests.get(gtfs_url)
    # Extract and parse GTFS data
    # For simplicity, assume GTFS data is parsed into a suitable format
    return {}

def generate_vehicle_positions_feed(matched_data):
    feed = vehicle_positions_pb2.VehiclePositionFeed()
    for data in matched_data:
        position = feed.entity.add()
        position.vehicle_id = data["vehicle_id"]
        position.latitude = data["latitude"]
        position.longitude = data["longitude"]
        position.bearing = data["bearing"]
        position.speed = data["speed"]
        position.timestamp = data["timestamp"]
    return feed

def save_to_json(data, filename):
    with open(filename, "w") as json_file:
        json.dump(data, json_file, indent=2)

def fetch_and_save_data():
    # Fetch GPS data
    gps_data = fetch_gps_data()
    
    # Fetch GTFS data
    gtfs_data = fetch_gtfs_data()
    
    # Match GPS data to GTFS trip IDs
    matched_data = match_gps_to_trip(gps_data, gtfs_data)
    
    # Generate GTFS-RT feeds
    vehicle_positions_feed = generate_vehicle_positions_feed(matched_data)
    
    # Convert to JSON
    vehicle_positions_json = MessageToJson(vehicle_positions_feed)
    
    # Save JSON data
    timestamp = int(time.time())
    save_to_json(json.loads(vehicle_positions_json), f"vehicle_positions_{timestamp}.json")

# Fetch and save data every minute for 30 minutes
start_time = time.time()
while (time.time() - start_time) < 1800:  # 30 minutes
    fetch_and_save_data()
    time.sleep(60)  # Wait for 1 minute before fetching again

print("Finished fetching data for 30 minutes.")
