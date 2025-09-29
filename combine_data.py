import pandas as pd

# This script combines the health and trends datasets
# and saves it to a csv file (reef_combined.csv)
reef_health = pd.read_csv("reef_dhw_data.csv")
trends = pd.read_csv("reef_breaks_trends.csv")

# Make sure dates match format (drop timezone info from reef_health if present)
reef_health["date"] = pd.to_datetime(reef_health["date"]).dt.strftime("%Y-%m-%d")
trends["date"] = pd.to_datetime(trends["date"]).dt.strftime("%Y-%m-%d")

# Merge on date and break name
merged = pd.merge(
    trends,
    reef_health,
    on=["date", "reef_break"],
    # how="inner"  # only keep matching rows
    how="outer"
)

# Reorder columns for clarity and save
merged = merged[["date", "reef_break", "interest", "dhw"]]
merged.to_csv("reef_combined.csv", index=False)

print("Merged dataset saved as reef_combined.csv")
