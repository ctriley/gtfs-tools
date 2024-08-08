#### Task 1: GPS to AVL
1. **Goal**: Match GPS data of vehicles to specific trips.
2. **Steps**:
   - Download static GTFS data from [here](https://cdn.mbta.com/MBTA_GTFS.zip).
   - Scrape GPS data from the real-time feed [here](https://cdn.mbta.com/realtime/VehiclePositions.pb).
   - Match the GPS data to trip IDs.

#### Task 2: Create a Better Schedule
1. **Goal**: Make a more accurate bus/train schedule using real-time data.
2. **Steps**:
   - Download static GTFS data from [here](https://cdn.mbta.com/MBTA_GTFS.zip).
   - Collect real-time data from these links:
     - [Service Alerts](https://cdn.mbta.com/realtime/Alerts.pb)
     - [Trip Updates](https://cdn.mbta.com/realtime/TripUpdates.pb)
     - [Vehicle Positions](https://cdn.mbta.com/realtime/VehiclePositions.pb)
   - Use this real-time data to update the schedule, focusing on the `stop_times.txt` file.


- Take vehicle id and position ---> tripId