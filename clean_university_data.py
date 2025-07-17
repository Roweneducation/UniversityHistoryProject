import pandas as pd
import re

# Load the raw university data
df = pd.read_csv("universities_founded.csv")

# Drop rows without coordinates or year
df = df.dropna(subset=["coord", "year"])

# Extract lat/lon from 'coord' column (format: "Point(LONG LAT)")
def parse_coord(point_str):
    match = re.match(r'Point\(([-\d.]+) ([-\d.]+)\)', point_str)
    if match:
        lon, lat = match.groups()
        return float(lat), float(lon)
    return None, None

# Apply coordinate parsing
df[['latitude', 'longitude']] = df['coord'].apply(lambda x: pd.Series(parse_coord(x)))

# Drop malformed coordinate entries
df = df.dropna(subset=["latitude", "longitude"])

# ✅ Filter out invalid coordinates (e.g., (0,0), ocean, Antarctica)
df = df[
    (df['latitude'].between(-60, 85)) &
    (df['longitude'].between(-180, 180)) &
    ~((df['latitude'].abs() < 1) & (df['longitude'].abs() < 1))
]

# Optional: standardize country names to lowercase for consistency
df['country'] = df['country'].fillna("").str.strip()

# Optional: sort by year
df = df.sort_values("year")

# Save cleaned dataset with all useful columns
df.to_csv("universities_cleaned.csv", index=False)
print("Cleaned data saved to universities_cleaned.csv")
