import requests

url = "https://cdn.mbta.com/realtime/Alerts.pb"
response = requests.get(url)

with open("Alerts.pb", "wb") as file:
    file.write(response.content)
