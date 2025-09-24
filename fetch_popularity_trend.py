import pandas as pd
from pytrends.request import TrendReq

# Ignoring warnings (pandas' new release)
import warnings
warnings.simplefilter(action="ignore", category=FutureWarning)


# Load reef breaks
reef_breaks = pd.read_csv("reef_breaks.csv")

# Setup pytrends
pytrends = TrendReq(hl="en-US", tz=360)

all_data = []

for name in reef_breaks["name"]:
    query = f"surf {name}"
    print(f"Fetching Google Trends for: {query}")
    
    try:
        # Get weekly interest for past 5 years
        pytrends.build_payload([query], cat=0, timeframe="today 5-y", geo="", gprop="")
        df = pytrends.interest_over_time()
        
        if not df.empty:
            df = df.reset_index()[["date", query]]
            df["reef_break"] = name
            all_data.append(df)
        else:
            print(f"No data for {query}")

    except Exception as e:
        print(f"Error fetching {query}: {e}")

# Combine and save
if all_data:
    final_df = pd.concat(all_data, ignore_index=True)
    final_df.to_csv("reef_breaks_trends.csv", index=False)
    print("\nSaved reef_breaks_trends.csv with Google Trends data")
else:
    print("\nNo trends data collected.")
