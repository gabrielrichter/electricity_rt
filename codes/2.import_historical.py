# title: 2.import_historical.py
# author: Gabriel Richter de Almeida (FGV EPGE)
# date: 2020-09-13

# import modules
import os
import numpy as np
import pandas as pd

# set path
root = r'C:\Users\gabri\Desktop\electricity_rt'
data = os.path.join(root, 'data')
output = os.path.join(root, 'output')
temp = os.path.join(root, 'temp')

# load datasets
df = pd.read_pickle(os.path.join(temp, 'consumption.pkl'))  # consumption dataset

df_gdp = pd.read_excel(os.path.join(data, 'gdp.xlsx'),
                       skiprows=5,
                       skipfooter=1)  # gdp dataset

# clean datasets
df = df.groupby('date')['consumption'].sum().rename('consumption_yoy')

df = df.resample('Q').sum()

df = df.pct_change(periods=4)

df = df * 100

df = df[4:-1]  # excludes first year and last quarter (since it is not over yet)

df_gdp.columns = pd.date_range(start='1996-01-01', end='2020-06-30', freq='Q')

df_gdp = df_gdp.melt(var_name='date', value_name='gdp_yoy')

df_gdp = df_gdp.set_index('date')

df_gdp = df_gdp.squeeze()  # convert dataframe to series

df_gdp = df_gdp['2002':]

# merge datasets
df = pd.concat([df, df_gdp], axis=1)

# export datasets
df.to_pickle(os.path.join(output, 'historical.pkl'))
