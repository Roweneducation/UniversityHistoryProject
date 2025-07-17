import requests
import pandas as pd

# SPARQL endpoint
url = "https://query.wikidata.org/sparql"

# Updated SPARQL query with countryLabel
query = """
SELECT ?universityLabel ?inceptionYear ?coord ?countryLabel WHERE {
  ?university wdt:P31 wd:Q3918;       # instance of university
              wdt:P571 ?inception.    # inception date
  OPTIONAL { ?university wdt:P625 ?coord. }     # coordinates
  OPTIONAL { ?university wdt:P17 ?country. }    # country
  BIND(year(?inception) AS ?inceptionYear)
  SERVICE wikibase:label { bd:serviceParam wikibase:language "en". }
}
"""

# Headers required for Wikidata API
headers = {
    "User-Agent": "UniversityAnimationBot/1.0 (your_email@example.com)",
    "Accept": "application/sparql-results+json"
}

# Send request
response = requests.get(url, headers=headers, params={"query": query})

# Convert response to JSON
data = response.json()

# Parse data
results = []
for item in data["results"]["bindings"]:
    label = item.get("universityLabel", {}).get("value", "")
    year = int(item["inceptionYear"]["value"])
    coord = item.get("coord", {}).get("value", "")
    country = item.get("countryLabel", {}).get("value", "")
    results.append({
        "university": label,
        "year": year,
        "coord": coord,
        "country": country
    })

# Convert to DataFrame
df = pd.DataFrame(results)

# Save to CSV
df.to_csv("universities_founded.csv", index=False)
print("Saved to universities_founded.csv")


