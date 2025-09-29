import pandas as pd
from pytrends.request import TrendReq
import warnings

warnings.simplefilter(action="ignore", category=FutureWarning) # Ignore pandas warnings

# This script fetches the popularity trend of each reef break from google trends using pytrends
# and saves it to a csv file (reef_breaks_trends.csv)
# https://github.com/GeneralMills/pytrends

reef_breaks = pd.read_csv("reef_breaks.csv")

# Setup pytrends
pytrends = TrendReq(hl="en-US", tz=360)

all_data = []

for name in reef_breaks["name"]:
    query = f"surf {name}"
    print(f"Fetching Google Trends for: {query}")
    
    try:
        # Fetches popularity trends from 2019-2024 (The health data stops after 2024)
        pytrends.build_payload([query], cat=0, timeframe="2019-01-01 2024-12-31", geo="", gprop="")
        df = pytrends.interest_over_time()
        
        if not df.empty:
            df = df.reset_index()[["date", query]]
            df = df.rename(columns={query: "interest"})
            df["reef_break"] = name
            all_data.append(df)
        else:
            print(f"No data found for {query}")

    except Exception as e:
        print(f"Error fetching {query}: {e}")

# Combine, create dataframe and save
if all_data:
    final_df = pd.concat(all_data, ignore_index=True)
    final_df.to_csv("reef_breaks_trends.csv", index=False)
    print("\nSaved reef_breaks_trends.csv with Google Trends data")
else:
    print("\nNo trends data collected.")
