import requests
import pandas as pd

OVERPASS_URL = "https://overpass-api.de/api/interpreter"

bounding_box = [40.7000, -74.0200, 40.8000, -73.9500]  # Example: NYC

overpass_query = f"""
[out:json];
(
  way["highway"]["maxspeed"]({bounding_box[0]},{bounding_box[1]},{bounding_box[2]},{bounding_box[3]});
  way["highway"](if:!t["maxspeed"])({bounding_box[0]},{bounding_box[1]},{bounding_box[2]},{bounding_box[3]});  # Fetch roads without maxspeed
);
out center;
"""

response = requests.get(OVERPASS_URL, params={"data": overpass_query})

if response.status_code != 200:
    print("❌ Failed to fetch traffic data!")
    exit()

data = response.json()

traffic_data = []
for element in data["elements"]:
    if "tags" in element:
        highway = element["tags"].get("highway", "unknown")
        maxspeed = element["tags"].get("maxspeed", "N/A")  # Use "N/A" if missing
        lanes = element["tags"].get("lanes", "1")
        oneway = element["tags"].get("oneway", "no")

        # Assign default speed limits based on highway type
        if maxspeed == "N/A":
            if highway in ["motorway", "trunk"]:
                maxspeed = "100"
            elif highway in ["primary", "secondary"]:
                maxspeed = "60"
            else:
                maxspeed = "30"  # Default for local roads

        # Get latitude and longitude
        if "center" in element:
            lat, lon = element["center"]["lat"], element["center"]["lon"]
        else:
            continue

        traffic_data.append([highway, maxspeed, lanes, oneway, lat, lon])

df = pd.DataFrame(traffic_data, columns=["highway", "maxspeed", "lanes", "oneway", "latitude", "longitude"])
df.to_csv("realtime_traffic_data.csv", index=False)
print("✅ Fixed traffic data saved to 'realtime_traffic_data.csv'!")
