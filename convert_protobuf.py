import requests
import alerts_pb2  # Import the generated Python class from the compiled proto file
from google.protobuf.json_format import MessageToJson

# Step 1: Download the protobuf file
url = "https://cdn.mbta.com/realtime/Alerts.pb"
response = requests.get(url)

with open("Alerts.pb", "wb") as file:
    file.write(response.content)

# Step 2: Read and parse the protobuf file
with open("Alerts.pb", "rb") as file:
    data = file.read()

feed = alerts_pb2.FeedMessage()
feed.ParseFromString(data)

# Step 3: Convert the parsed data to JSON
json_data = MessageToJson(feed)

# Step 4: Save the JSON data to a file
with open("Alerts.json", "w") as json_file:
    json_file.write(json_data)

print("Data successfully converted to JSON and saved to Alerts.json")
