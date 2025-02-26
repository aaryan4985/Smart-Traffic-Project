import pandas as pd

# Load the CSV file
df = pd.read_csv("traffic_data.csv")

# Print available columns to debug
print("📜 Available Columns:", df.columns)

# Rename columns if needed (modify based on actual column names)
column_mapping = {
    "lat": "latitude",
    "Latitude": "latitude",
    "Lat": "latitude",
    "lon": "longitude",
    "Longitude": "longitude",
    "Lng": "longitude"
}

df.rename(columns=column_mapping, inplace=True)

# Ensure required columns exist
required_columns = ["highway", "maxspeed", "lanes", "oneway", "latitude", "longitude"]

missing_columns = [col for col in required_columns if col not in df.columns]
if missing_columns:
    print(f"⚠️ Missing columns: {missing_columns}. Adding default values.")
    
    # Assign default values if missing (for testing purposes)
    if "latitude" in missing_columns:
        df["latitude"] = 40.7128  # Default to New York
    if "longitude" in missing_columns:
        df["longitude"] = -74.0060
    if "highway" in missing_columns:
        df["highway"] = "unknown"
    if "maxspeed" in missing_columns:
        df["maxspeed"] = 0
    if "lanes" in missing_columns:
        df["lanes"] = 1
    if "oneway" in missing_columns:
        df["oneway"] = False

# Select the required columns
df = df[required_columns]

# Display the first few rows to confirm
print("✅ Processed Data Preview:\n", df.head())

# Save cleaned data (optional)
df.to_csv("cleaned_traffic_data.csv", index=False)
print("✅ Cleaned data saved to 'cleaned_traffic_data.csv'")
