import folium
import pandas as pd

# Sample data for traffic points
data = {
    "latitude": [40.7128, 40.7138, 40.7148],
    "longitude": [-74.0060, -74.0070, -74.0080]
}
df = pd.DataFrame(data)

# Define map center (New York coordinates)
map_center = [40.7128, -74.0060]
traffic_map = folium.Map(location=map_center, zoom_start=13)

# Add traffic points to the map
for _, row in df.iterrows():
    folium.CircleMarker(
        location=(row["latitude"], row["longitude"]),  
        radius=5,  
        color="red",
        fill=True,
        fill_color="red",
    ).add_to(traffic_map)

# Save map as an HTML file
traffic_map.save("traffic_map.html")
print("✅ Traffic heatmap saved as 'traffic_map.html'")
