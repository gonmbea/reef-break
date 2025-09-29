import requests
import csv

reef_breaks = [
    # Top reef breaks
    "Pipeline",
    "Uluwatu",
    "Cloudbreak",
    "J-Bay", #No popularity data
    "Snapper Rocks",
    "Padang Padang",
    "G-Land",
    "Honolua Bay",
    "Raglan",
    "Puerto Escondido",
    "Tavarua", #No popularity data
    "Nias", #No popularity data
    "Kirra",

    # Not so popular reef breaks
    "The Wharf",
    "Chinamans",
    "Unstad",
    "Kuta Reef",
    "Namotu Left",
    "Wilkes Pass",
]

# This script fetches the lat, lon and country of each reef break from surfline.com
# and saves it to a csv file (reef_breaks.csv)
# https://pkg.go.dev/github.com/mhelmetag/surflinef/v2
# https://github.com/mhelmetag/surflinef

data = []

for break_name in reef_breaks:
    url = f"https://services.surfline.com/search/site?q={break_name}"
    r = requests.get(url).json()

    try:
        # get first surf spot hit
        spot = r[0]["hits"]["hits"][0]["_source"]

        name = spot.get("name", break_name)
        lat = spot.get("location", {}).get("lat", "")
        lon = spot.get("location", {}).get("lon", "")
        # take last breadcrumb as "country/region"
        country = spot.get("breadCrumbs", [""])[0]

        data.append([name, lat, lon, country])
        print(f"Added: {name} ({lat}, {lon}) in {country}")

    except Exception as e:
        print(f"No spot found for: {break_name} ({e})")

# Save to CSV
with open("reef_breaks.csv", "w", newline="", encoding="utf-8") as f:
    writer = csv.writer(f)
    writer.writerow(["name", "lat", "lon", "country"])
    writer.writerows(data)

print("\nSaved reef_breaks.csv with", len(data), "entries.")
