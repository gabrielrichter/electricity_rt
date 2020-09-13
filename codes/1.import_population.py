# title: 1.import_population.py
# author: Gabriel Richter de Almeida (FGV EPGE)
# date: 2020-09-13

# import modules
import os
import pandas as pd

# set paths
root = r'C:\Users\gabri\Desktop\electricity_rt'
data = os.path.join(root, 'data')
temp = os.path.join(root, 'temp')

# import dataset
df = pd.read_excel(os.path.join(data, 'population.xlsx'),
                   dtype={'state': 'category', 'id_municipality': 'object', 'municipality': 'category'},
                   skiprows=1
                   )

# clean dataset
df = df.melt(id_vars=['state', 'id_municipality', 'municipality'],
             var_name='year',
             value_name='population'
             )

df = df.set_index('year')

# save dataset in pickle (serialized) format
df.to_pickle(os.path.join(temp, 'population.pkl'))
