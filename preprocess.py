import os
import pandas as pd
import numpy as np
from datetime import datetime as dt
import json

# one line magic for getting all county json files
jsonfiles = ['vintages/' + fname for fname in os.listdir('vintages') if 'county' in fname]
# one line magic for extracting the date and time from the filename
dateinputs = [dt.strptime(s[:19], "%Y-%m-%d.%H:%M:%S") for s in os.listdir('vintages') if 'county' in s]
dateinputs.sort()
jsonfiles.sort()

dateseries = pd.Series(dateinputs, name='date')
fnseries = pd.Series(jsonfiles, name='filename')
datefile_df = pd.concat([dateseries, fnseries], axis=1)

vintage_json = []
for index, row in datefile_df.iterrows():
    with open(row['filename'], 'r') as datafile:
        vintage_json.append(json.load(datafile))

def process_vintages():
    # create a dataframe for each vintage
    vintage_df = [pd.DataFrame(vintage_json[i]['message']) for i in range(len(vintage_json))]

    # create a new series that is made up of the county name and state name combined
    # and do this for each row (axis=1) rather than the whole dataframe
    keyseries = vintage_df[0][0:-1][['county_name', 'state_name']].agg(lambda x: ', '.join(x), axis=1)
    keyseries.name = 'key'
    return [pd.concat([vintage_df[i], keyseries], axis=1) for i in range(len(vintage_json))]

def process_cases(vintage_df, transpose=False):
    cases_series = [vintage_df[i][['key', 'confirmed']].rename(columns={'confirmed': str(dateseries[i])}) for i in range(len(vintage_json))]
    cases_df = pd.concat([cases_series[0], cases_series[1].drop(['key'], axis=1)], axis=1)
    # cases_df = pd.merge(left=cases_series[0], right=cases_series[1], how='inner', left_on='key', right_on='key')

    for i in range(2, len(vintage_json)):
        # cases_df = pd.merge(left=cases_df, right=cases_series[i], how='inner', left_on='key', right_on='key', axis=1)
        cases_df = pd.concat([cases_df, cases_series[i].drop(['key'], axis=1)], axis=1)

    # write county case xlsx
    cases_df.to_excel('cases.xlsx')
    cases_dft = cases_df.transpose()
    cases_dft.to_excel('cases_transposed.xlsx')

    if transpose == True:
        return cases_dft
    else:
        return cases_df

def process_deaths(vintage_df, transpose=False):
    death_series = [vintage_df[i][['key', 'death']].rename(columns={'death': str(dateseries[i])}) for i in range(len(vintage_json))]
    death_df = pd.concat([death_series[0], death_series[1].drop(['key'], axis=1)], axis=1)
    # cases_df = pd.merge(left=cases_series[0], right=cases_series[1], how='inner', left_on='key', right_on='key')

    for i in range(2, len(vintage_json)):
        # cases_df = pd.merge(left=cases_df, right=cases_series[i], how='inner', left_on='key', right_on='key', axis=1)
        death_df = pd.concat([death_df, death_series[i].drop(['key'], axis=1)], axis=1)

    # write county case xlsx
    death_df.to_excel('deaths.xlsx')
    death_dft = death_df.transpose()
    death_dft.to_excel('deaths_transposed.xlsx')

    if transpose == True:
        return death_dft
    else:
        return death_df

if __name__ == '__main__':
    vintages = process_vintages()
    cases = process_cases(vintages)
    deaths = process_deaths(vintages)
