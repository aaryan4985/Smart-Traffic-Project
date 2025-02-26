import requests

# OpenStreetMap Overpass API endpoint
OVERPASS_URL = "https://overpass-api.de/api/interpreter"

# Define the Overpass Query to get traffic signals around a location (e.g., New York)
query = """
[out:json];
node(around:1000,40.7128,-74.0060)[highway=traffic_signals];
out;
"""

# Make the request
response = requests.get(OVERPASS_URL, params={"data": query})

# Check if request was successful
if response.status_code == 200:
    data = response.json()
    print("✅ Traffic Data Fetched Successfully!")
    print(data)  # Print fetched data
else:
    print("❌ Failed to fetch data:", response.status_code)
