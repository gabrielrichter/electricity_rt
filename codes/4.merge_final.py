# title: 4.merge_final.py
# author: Gabriel Richter de Almeida (FGV EPGE)
# date: 2020-09-13

# import modules
import os
import pandas as pd

# set paths
root = r'C:\Users\gabri\Desktop\electricity_rt'
temp = os.path.join(root, 'temp')
output = os.path.join(root, 'output')

# import datasets
df_consumption = pd.read_pickle(os.path.join(temp, 'consumption.pkl'))
df_temp_byregion = pd.read_pickle(os.path.join(temp, 'temperature_byregion.pkl'))

# merge consumption and temperature datasets
df_consumption = df_consumption.reset_index()
df_temp_byregion = df_temp_byregion.reset_index()

df = df_consumption.merge(right=df_temp_byregion,
                          how='left',
                          on=['date', 'region'],
                          indicator=True
                          )

df = df.set_index('date')
df = df.drop(columns=['_merge'])

# save dataset in pickle (serialized) format
df.to_pickle(os.path.join(output, 'df_byregion.pkl'))
