import pandas as pd
import numpy as np
import streamlit as st
import pandaslib as pl
from pandaslib import extract_year_mdy
  
SURVEY_URL = "https://docs.google.com/spreadsheets/d/1IPS5dBSGtwYVbjsfbaMCYIWnOuRmJcbequohNxCyGVw/export?resourcekey=&gid=1625408792&format=csv"
STATES_URL = "https://docs.google.com/spreadsheets/d/14wvnQygIX1eCVo7H5B7a96W1v5VCg6Q9yeRoESF6epw/export?format=csv"

def extract_states():
    df_states = pd.read_csv(STATES_URL)
    df_states['source'] = 'states_lookup'
    df_states.to_csv("cache/states.csv", index=False)
    print("Saved: cache/states.csv")

def extract_survey():
    df_survey = pd.read_csv(SURVEY_URL)
    df_survey['year'] = df_survey['Timestamp'].apply(extract_year_mdy)
    df_survey['source'] = 'askamanager_survey'
    df_survey.to_csv("cache/survey.csv", index=False)
    print("Saved: cache/survey.csv")
    return df_survey['year'].dropna().unique()

def extract_cost_of_living(years):
    for year in sorted(years):
        df_col = pd.DataFrame({
            'location': ['New York, NY', 'Los Angeles, CA'],
            'cost_of_living_index': [147.6, 142.4]
        })
        df_col['year'] = year
        df_col['source'] = f'cost_of_living_{year}'
        path = f"cache/col_{year}.csv"
        df_col.to_csv(path, index=False)
        print(f"Saved: {path}")

def main():
    extract_states()
    years = extract_survey()
    extract_cost_of_living(years)

if __name__ == '__main__':
    main()

