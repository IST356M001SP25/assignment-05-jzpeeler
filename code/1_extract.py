import pandas as pd
import numpy as np
import streamlit as st
import pandaslib as pl
from pandaslib import extract_year_mdy
  
survey_url = "https://docs.google.com/spreadsheets/d/1IPS5dBSGtwYVbjsfbaMCYIWnOuRmJcbequohNxCyGVw/export?resourcekey=&gid=1625408792&format=csv"
survey = pd.read_csv(survey_url)

# Extract year from Timestamp using your library function
survey['year'] = survey['Timestamp'].apply(pl.extract_year_mdy)

# Save to cache
survey.to_csv("cache/survey.csv", index=False)

# --- Cost of Living Data ---
years = survey['year'].dropna().unique()

for year in years:
    try:
        col_tables = pd.read_html(f"https://www.numbeo.com/cost-of-living/rankings.jsp?title={int(year)}&displayColumn=0")
        col_year = col_tables[1]  # This is the correct table
        col_year['year'] = int(year)
        col_year.to_csv(f"cache/col_{int(year)}.csv", index=False)
        print(f"Saved: cache/col_{int(year)}.csv")
    except Exception as e:
        print(f"Failed to extract COL for {year}: {e}")

# --- State Lookup Data ---
states_url = "https://docs.google.com/spreadsheets/d/14wvnQygIX1eCVo7H5B7a96W1v5VCg6Q9yeRoESF6epw/export?format=csv"
states = pd.read_csv(states_url)
states.to_csv("cache/states.csv", index=False)

