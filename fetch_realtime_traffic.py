import requests
import pandas as pd

# Define the Overpass API URL
OVERPASS_URL = "https://overpass-api.de/api/interpreter"

# Define the area (bounding box) to fetch traffic data
# Format: [south, west, north, east]
bounding_box = [40.7000, -74.0200, 40.8000, -73.9500]  # Example: New York City

# Overpass QL query to fetch highways with speed limits
overpass_query = f"""
[out:json];
(
  way["highway"]["maxspeed"]({bounding_box[0]},{bounding_box[1]},{bounding_box[2]},{bounding_box[3]});
);
out center;
"""

# Send request to Overpass API
response = requests.get(OVERPASS_URL, params={"data": overpass_query})

# Check for errors
if response.status_code != 200:
    print("❌ Failed to fetch traffic data!")
    exit()

# Parse JSON response
data = response.json()

# Extract relevant data
traffic_data = []
for element in data["elements"]:
    if "tags" in element:
        highway = element["tags"].get("highway", "unknown")
        maxspeed = element["tags"].get("maxspeed", "0")  # Default to 0 if missing
        lanes = element["tags"].get("lanes", "1")  # Default to 1 lane
        oneway = element["tags"].get("oneway", "no")

        # Get latitude and longitude (use "center" key for way elements)
        if "lat" in element and "lon" in element:
            lat, lon = element["lat"], element["lon"]
        elif "center" in element:
            lat, lon = element["center"]["lat"], element["center"]["lon"]
        else:
            continue  # Skip if no location data

        traffic_data.append([highway, maxspeed, lanes, oneway, lat, lon])

# Convert to Pandas DataFrame
df = pd.DataFrame(traffic_data, columns=["highway", "maxspeed", "lanes", "oneway", "latitude", "longitude"])

# Save to CSV
df.to_csv("realtime_traffic_data.csv", index=False)
print("✅ Real-time traffic data saved to 'realtime_traffic_data.csv'!")
