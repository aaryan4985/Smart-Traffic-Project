import pandas as pd

# Load the stored traffic data
df = pd.read_csv("traffic_data.csv")

# Display first few rows
print("📊 Traffic Data Overview:")
print(df.head())

# Check missing values
print("\n🔍 Missing Data Summary:")
print(df.isnull().sum())

# Count roads based on highway type
print("\n🚦 Road Type Distribution:")
print(df["highway"].value_counts())
