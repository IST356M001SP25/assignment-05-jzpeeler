import pandas as pd
import streamlit as st
import pandaslib as pl

# TODO: Write your transformation code here

survey_data = pd.read_csv('cache/survey.csv')
states_data = pd.read_csv('cache/states.csv')

col_data = []
for year in survey_data['year'].dropna().unique():
    df_col = pd.read_csv(f'cache/col_{year}.csv')
    df_col['year'] = int(year)
    col_data.append(df_col)
col_data = pd.concat(col_data, ignore_index=True)

survey_data['_country'] = survey_data['What country do you work in?'].apply(pl.clean_country_usa)

survey_states_combined = survey_data.merge(
    states_data,
    left_on="If you're in the U.S., what state do you work in?",
    right_on='State',
    how='inner'
)

survey_states_combined['_full_city'] = (
    survey_states_combined['What city do you work in?'] + ', ' +
    survey_states_combined['Abbreviation'] + ', ' +
    survey_states_combined['_country']
)

combined = survey_states_combined.merge(
    col_data,
    left_on=['year', '_full_city'],
    right_on=['year', 'City'],
    how='inner'
)

combined["_annual_salary_cleaned"] = combined[
    "What is your annual salary? (You'll indicate the currency in a later question. "
    "If you are part-time or hourly, please enter an annualized equivalent -- what you would earn "
    "if you worked the job 40 hours a week, 52 weeks a year.)"
].apply(pl.clean_currency)

combined['_annual_salary_adjusted'] = combined.apply(
    lambda row: row["_annual_salary_cleaned"] * (100 / row['Cost of Living Index']),
    axis=1
)

# --- Save engineered dataset ---
combined.to_csv('cache/survey_dataset.csv', index=False)

# --- Report: by Age ---
report_age = combined.pivot_table(
    index='_full_city',
    columns='How old are you?',
    values='_annual_salary_adjusted',
    aggfunc='mean'
)
report_age.to_csv('cache/annual_salary_adjusted_by_location_and_age.csv')

# --- Report: by Education ---
report_edu = combined.pivot_table(
    index='_full_city',
    columns='What is your highest level of education completed?',
    values='_annual_salary_adjusted',
    aggfunc='mean'
)
report_edu.to_csv('cache/annual_salary_adjusted_by_location_and_education.csv')