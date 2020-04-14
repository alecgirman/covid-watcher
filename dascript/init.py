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
datefile_df

dated_json = {}
for index, row in datefile_df.iterrows():
    with open(row['filename'], 'r') as datafile:
        dated_json[row['date']] = json.load(datafile)
