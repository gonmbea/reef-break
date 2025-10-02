# Reef Break (Reef Health vs Surf Break Popularity - A Correlation Analysis)

I got this idea while watching a surfing reel where a surfer skimmed over a shallow reef, almost injuring themselves, but the comments barely seemed to notice. Instead, they were full of worry about reef health, which made me curious: could there be a connection between **coral reef stress** and the **popularity of surf spots**?

This project is my way of exploring that question while practicing data analysis.

## Code Structure
- `fetch_surfline_data.py` -> given a list of reef names it pulls coordinates and country from the Surfline API and saves it in `reef_breaks.csv`
- `fetch_dhw_data.py` -> fetches reef thermal stress (NOAA DHW), monthly-averages it and saves it in `reef_dhw_data.csv`
- `fetch_popularity_trend.py` -> gets Google Trends search interest and saves it in `reef_breaks_trends.csv`
- `combine_data.py` -> merges everything into `reef_combined.csv` for analysis

Run them in order (1 → 4) to generate the full combined dataset.

## What is DHW?
**Degree Heating Weeks (DHW)** measure how much **heat stress** a reef experiences over a rolling 12-week window:
- `0–2 °C-weeks` -> No stress
- `2–4 °C-weeks` -> Bleaching Watch
- `4–8 °C-weeks` -> Bleaching Warning
- `≥8 °C-weeks` -> Severe bleaching & mortality risk

## Data Sources
- **Reef metadata** -> Surfline search API (`https://services.surfline.com/search/site?q=<break>`)
- **Reef health** -> NOAA Coral Reef Watch (CRW) DHW 5 km product via ERDDAP
  - Docs: [NOAA DHW](https://coastwatch.pfeg.noaa.gov/erddap/griddap/NOAA_DHW.html)
- **Popularity** -> Google Trends (via [pytrends](https://github.com/GeneralMills/pytrends))

*Google Trends is used as a simple proxy for surf break popularity over time.*

## Resources
- **Alex The Analyst** -> My Jupyter Notebook analysis followed mainly this [video's](https://www.youtube.com/watch?v=iPYVYBtUTyE&list=PLUaB-1hjhk8H48Pj32z4GZgGWyylqv85f&index=7) examples.
  - It helped me understand how to create and visualize correlation plots and matrices.


## Notes
- Data range limited to **2019–2024** to align sources.
- Google Trends and Surfline API sometimes return no data for some breaks.
- NOAA API is rate-limited so the scripts include small delays.

## Future Improvements
- Normalize Google Trends data to enable better comparison of search popularity between different reef breaks.
