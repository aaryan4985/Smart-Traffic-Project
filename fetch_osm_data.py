import requests
import pandas as pd

# OpenStreetMap Overpass API URL
OVERPASS_URL = "https://overpass-api.de/api/interpreter"

# Query to fetch roads & traffic signals
query = """
[out:json];
way(around:2000,40.7128,-74.0060)[highway];
out body;
"""

# Fetch data from OSM
response = requests.get(OVERPASS_URL, params={"data": query})

# Check if request was successful
if response.status_code == 200:
    data = response.json()
    elements = data.get("elements", [])

    # Extract relevant details
    traffic_data = []
    for element in elements:
        if "tags" in element:
            traffic_data.append({
                "id": element.get("id"),
                "type": element.get("type"),
                "name": element["tags"].get("name", "Unknown"),
                "highway": element["tags"].get("highway", "Unknown"),
                "maxspeed": element["tags"].get("maxspeed", "Unknown"),
                "lanes": element["tags"].get("lanes", "Unknown"),
                "oneway": element["tags"].get("oneway", "Unknown"),
            })

    # Convert to DataFrame & Save to CSV
    df = pd.DataFrame(traffic_data)
    df.to_csv("traffic_data.csv", index=False)
    print("✅ Traffic Data Saved to 'traffic_data.csv'!")

else:
    print("❌ Failed to fetch data:", response.status_code)
