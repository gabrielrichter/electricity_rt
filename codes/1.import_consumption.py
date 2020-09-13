# title: 1.import_consumption.py
# author: Gabriel Richter de Almeida (FGV EPGE)
# date: 2020-09-13

# import modules
import os
import pandas as pd
import numpy as np

# set paths
root = r'C:\Users\gabri\Desktop\electricity_rt'
data = os.path.join(root, 'data')
temp = os.path.join(root, 'temp')

# import datasets
df = pd.read_csv(os.path.join(data, 'consumption.csv'),
                 header=None,
                 names=['date', 'region', 'consumption_total', 'consumption_region'],
                 index_col=['date'],
                 usecols=[0, 1, 2, 4],
                 skiprows=1,
                 parse_dates=['date'],
                 thousands=','
                 )

df_holidays = pd.read_excel(os.path.join(data, 'holidays.xls'),
                            header=None,
                            names=['date', 'dow', 'holiday'],
                            index_col='date',
                            skiprows=1,
                            nrows=241
                            )

# clean datasets
df['region'].replace({None: 'BR',
                      'Nordeste': 'NE',
                      'Norte': 'N',
                      'Sudeste/Centro-Oeste': 'SE-CW',
                      'Sul': 'S'},
                     inplace=True
                     )

df[['consumption_total', 'consumption_region']] = df[['consumption_total', 'consumption_region']].fillna(method='bfill',
                                                                                                         axis='columns'
                                                                                                         )

df = df.drop(columns=['consumption_region'])

df = df.rename(columns={'consumption_total': 'consumption'})

df_holidays = df_holidays.drop(columns='dow')
df_holidays['dholiday'] = 1  # holiday dummy

# merge consumption and holiday datasets
df['year'], df['month'], df['day'] = df.index.year, df.index.month, df.index.day
df_holidays['year'], df_holidays['month'], df_holidays[
    'day'] = df_holidays.index.year, df_holidays.index.month, df_holidays.index.day

df = df[~(df.index == '2020-09-01') & ~(df['region'] == 'BR')]

df = df.reset_index()
df_holidays = df_holidays.reset_index()

df = df.merge(right=df_holidays,
              how='left',
              on=['year', 'month', 'day'],
              suffixes=['', '_y'],
              indicator=True,
              validate='m:1')

df = df.set_index('date')

df = df.fillna(value={'dholiday': 0}).drop(
    columns=['year', 'month', 'day', 'date_y', 'holiday', '_merge'])

df = df.rename(columns={'dholiday': 'holiday'})

# create new variables
# important note: Pandas uses the ISO-8601 standard for date/time (https://en.wikipedia.org/wiki/ISO_8601)
#   (1) weeks start on Monday
#   (2) years have 52 or 53 full weeks. The first week of the year is the one that contains that year's first Thursday.
df['hod'] = df.index.hour  # hour of day
df['dow'] = df.index.dayofweek  # day of week
df['woy'] = df.index.weekofyear  # week of year

# organize and save dataset in pickle (serialized) format
df[['region', 'hod', 'dow', 'woy']] = df[['region', 'hod', 'dow', 'woy']].astype('category')  # optimize memory usage
df['holiday'] = df['holiday'].astype('bool_')

df.to_pickle(os.path.join(temp, 'consumption.pkl'))
