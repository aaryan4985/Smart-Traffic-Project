import pandas as pd
import folium

# Load the real-time traffic data
df = pd.read_csv("realtime_traffic_data.csv")

# Ensure there are valid latitude and longitude values
if df.empty or "latitude" not in df.columns or "longitude" not in df.columns:
    print("❌ Error: No valid location data found in realtime_traffic_data.csv")
    exit()

# Create a map centered at the average location
map_center = [df["latitude"].mean(), df["longitude"].mean()]
m = folium.Map(location=map_center, zoom_start=12)

# Function to determine marker color based on speed
def get_marker_color(maxspeed):
    try:
        speed = int(maxspeed)
    except ValueError:
        return "gray"  # If speed is missing or invalid, mark as gray
    if speed == 0:
        return "gray"   # No speed data
    elif speed < 30:
        return "red"    # Heavy traffic
    elif speed < 60:
        return "orange" # Moderate traffic
    else:
        return "green"  # Free-flowing traffic

# Add markers for each traffic point
for _, row in df.iterrows():
    folium.CircleMarker(
        location=[row["latitude"], row["longitude"]],
        radius=5,
        color=get_marker_color(row["maxspeed"]),
        fill=True,
        fill_color=get_marker_color(row["maxspeed"]),
        fill_opacity=0.7,
        popup=f"🛣️ Highway: {row['highway']}<br>🚦 Max Speed: {row['maxspeed']} km/h<br>🚗 Lanes: {row['lanes']}"
    ).add_to(m)

# Save the updated map
m.save("traffic_map.html")
print("✅ Real-time traffic map saved! Open 'traffic_map.html' to view.")
