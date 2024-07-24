import requests
import time
import json
import protos.alerts_pb2 as alerts_pb2
import protos.updates_pb2 as updates_pb2
import protos.vehicles_pb2 as vehicles_pb2
from google.protobuf.json_format import MessageToJson

def fetch_protobuf_data(url, proto_class):
    response = requests.get(url)
    if response.status_code == 200:
        proto_obj = proto_class()
        proto_obj.ParseFromString(response.content)
        return proto_obj
    else:
        print(f"Failed to fetch data from {url}")
        return None

def save_to_json(data, filename):
    with open(filename, "w") as json_file:
        json.dump(data, json_file, indent=2)

def fetch_and_save_data():
    service_alerts_url = "https://cdn.mbta.com/realtime/Alerts.pb"
    trip_updates_url = "https://cdn.mbta.com/realtime/TripUpdates.pb"
    vehicle_positions_url = "https://cdn.mbta.com/realtime/VehiclePositions.pb"

    # Fetch data
    alerts_data = fetch_protobuf_data(service_alerts_url, alerts_pb2.AlertFeedMessage)
    trip_updates_data = fetch_protobuf_data(trip_updates_url, updates_pb2.TripUpdateFeedMessage)
    vehicle_positions_data = fetch_protobuf_data(vehicle_positions_url, vehicles_pb2.VehiclePositionFeedMessage)

    # Convert to JSON
    alerts_json = MessageToJson(alerts_data) if alerts_data else "{}"
    trip_updates_json = MessageToJson(trip_updates_data) if trip_updates_data else "{}"
    vehicle_positions_json = MessageToJson(vehicle_positions_data) if vehicle_positions_data else "{}"

    # Save JSON data
    timestamp = int(time.time())
    save_to_json(json.loads(alerts_json), f"alerts_{timestamp}.json")
    save_to_json(json.loads(trip_updates_json), f"trip_updates_{timestamp}.json")
    save_to_json(json.loads(vehicle_positions_json), f"vehicle_positions_{timestamp}.json")

# Fetch and save data every minute for 30 minutes
start_time = time.time()
while (time.time() - start_time) < 1800:  # 30 minutes
    fetch_and_save_data()
    time.sleep(60)  # Wait for 1 minute before fetching again

print("Finished fetching data for 30 minutes.")

