import pandas as pd
import matplotlib.pyplot as plt

# Load your cleaned dataset
df = pd.read_csv("universities_cleaned.csv")

# Ensure year is numeric and within a valid range
df['year'] = pd.to_numeric(df['year'], errors='coerce')
df = df.dropna(subset=['year'])
df['year'] = df['year'].astype(int)
df = df[df['year'] >= 1000]

# Normalize and clean country column
df['country'] = df['country'].fillna("").str.strip().str.lower()

# Define filters for USA and Europe
usa_filter = df['country'].str.contains("united states|usa")
europe_filter = df['country'].str.contains(
    "germany|france|spain|italy|switzerland|sweden|austria|belgium|netherlands|poland|czech|hungary|uk|united kingdom|portugal|denmark|finland|norway|romania|greece|ireland|bulgaria|slovakia|slovenia|croatia|estonia|latvia|lithuania|luxembourg|serbia|ukraine|bosnia|macedonia|moldova|montenegro|albania|iceland",
    case=False
)

# Define helper to get yearly counts
def count_universities(df_subset, label):
    return df_subset.groupby('year').size().reset_index(name=label)

# Count for each region
worldwide = count_universities(df, "worldwide")
usa = count_universities(df[usa_filter], "usa")
europe = count_universities(df[europe_filter], "europe")

# Merge all into a single table
merged = pd.merge(worldwide, usa, on="year", how="outer")
merged = pd.merge(merged, europe, on="year", how="outer")
merged = merged.fillna(0).astype({"worldwide": int, "usa": int, "europe": int})

# Add cumulative totals
merged["worldwide_cum"] = merged["worldwide"].cumsum()
merged["usa_cum"] = merged["usa"].cumsum()
merged["europe_cum"] = merged["europe"].cumsum()

# Print the table
print("\nCumulative Number of Universities by Year (Worldwide, USA, Europe):")
print(merged[["year", "worldwide_cum", "usa_cum", "europe_cum"]].head(15))  # Show first 15 rows

# Plot cumulative totals
plt.figure(figsize=(14, 6))
plt.plot(merged["year"], merged["worldwide_cum"], label="Worldwide (Cumulative)", linewidth=2)
plt.plot(merged["year"], merged["usa_cum"], label="USA (Cumulative)", linewidth=2)
plt.plot(merged["year"], merged["europe_cum"], label="Europe (Cumulative)", linewidth=2)

plt.title("Cumulative Number of Universities by Year")
plt.xlabel("Year")
plt.ylabel("Total Universities Existing")
plt.grid(True)
plt.legend()

# ⏱ Set x-axis ticks every 10 years
plt.xticks(ticks=range(1000, merged["year"].max() + 1, 50), rotation=45)
plt.yticks(ticks=range(0, merged[["worldwide_cum", "usa_cum", "europe_cum"]].values.max() + 500, 500))

plt.tight_layout()
plt.show()
