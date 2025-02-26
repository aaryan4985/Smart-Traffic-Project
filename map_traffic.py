import pandas as pd
import folium

# Load the cleaned traffic data
df = pd.read_csv("cleaned_traffic_data.csv")

# Create a map centered at an average location
map_center = [df["latitude"].mean(), df["longitude"].mean()]
m = folium.Map(location=map_center, zoom_start=12)

# Define color categories for different traffic conditions
def get_marker_color(maxspeed):
    if maxspeed == 0:  
        return "gray"   # No speed data
    elif maxspeed < 30:
        return "red"    # Heavy traffic
    elif maxspeed < 60:
        return "orange" # Moderate traffic
    else:
        return "green"  # Free-flowing traffic

# Add points to the map
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

# Save the map as an HTML file
m.save("traffic_map.html")
print("✅ Map updated with traffic conditions! Open 'traffic_map.html' to view.")
