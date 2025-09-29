import pandas as pd
import time

# This script fetches the health trend of each reef break from NOAA's DHW (Degree Heating Week) data
# and saves it to a csv file (reef_dhw_data.csv)
# https://coastwatch.pfeg.noaa.gov/erddap/griddap/documentation.html

def get_reef_health_timeseries(latitude, longitude, name, country, years_back=5):
    """
    Get raw DHW time series for the past N years.
    """
    current_year = 2024  # last year with data
    start_year = current_year - years_back

    dfs = []

    for year in range(start_year, current_year + 1):
        try:
            url = (
                f"https://pae-paha.pacioos.hawaii.edu/erddap/griddap/dhw_5km.csv?"
                f"CRW_DHW"
                f"[({year}-01-01T00:00:00Z):1:({year}-12-31T00:00:00Z)]"
                f"[({latitude}):1:({latitude})]" #(Start:stride:stop)
                f"[({longitude}):1:({longitude})]"
            )

            df = pd.read_csv(url, skiprows=[1])  # Skip units row
            df = df.rename(columns={"time": "date", "CRW_DHW": "dhw"})
            df["date"] = pd.to_datetime(df["date"])
            df["name"] = name
            df["country"] = country

            dfs.append(df[["date", "name", "country", "dhw"]])

        except Exception as e:
            print(f"  {year}: Error fetching data for {name} - {e}")
            continue

    if dfs:
        return pd.concat(dfs, ignore_index=True)
    else:
        return None


def process_all_reefs(input_csv, output_csv, years_back=5, delay=1):
    """
    Process all reef breaks and return monthly-averaged DHW time series for each.
    Saves DataFrame with columns: [date, dhw, reef_break].
    """
    reefs_df = pd.read_csv(input_csv)
    all_dfs = []

    for index, row in reefs_df.iterrows():
        print(f"\nProcessing {index+1}/{len(reefs_df)}: {row['name']} ({row['country']})")
        print(f"Coordinates: ({row['lat']}, {row['lon']})")

        df = get_reef_health_timeseries(
            row["lat"], row["lon"], row["name"], row["country"], years_back
        )

        if df is not None:
            # Calculate monthly averages
            df = (
                df.set_index("date")
                  .resample("MS")  # Month Start
                  .mean(numeric_only=True)
                  .reset_index()
            )
            df["reef_break"] = row["name"]

            all_dfs.append(df[["date", "dhw", "reef_break"]])
        else:
            print("No data retrieved.")

        time.sleep(delay)  # to avoid getting flagged by the api

    if all_dfs:
        final_df = pd.concat(all_dfs, ignore_index=True)
        final_df.to_csv(output_csv, index=False)
        print("\nSaved", output_csv)
        return final_df
    else:
        print("No results generated.")
        return None


if __name__ == "__main__":
    results = process_all_reefs(
        input_csv="reef_breaks.csv",
        output_csv="reef_dhw_data.csv"
    )
