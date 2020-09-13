# title: 6.tables.py
# author: Gabriel Richter de Almeida (FGV EPGE)
# date: 2020-09-13

# import modules
import os
import numpy as np
import pandas as pd

# set paths
root = r'C:\Users\gabri\Desktop\electricity_rt'
output = os.path.join(root, 'output')

# define dictionary
region_dic = {'NE': [], 'N': [], 'SE-CW': [], 'S': []}

# import datasets
for i in region_dic.keys():
    df = pd.read_pickle(os.path.join(output, f'results_cluster_2020_{i}_month.pkl'))

    df.index = pd.date_range('01-01-2020', periods=8, freq='M')

    df = df['beta']

    region_dic[i] = df

df = pd.concat(region_dic.values(), axis=1)
df.columns = ['Nordeste', 'Norte', 'Sudeste/Centro-Oeste', 'Sul']

df_br = pd.read_pickle(os.path.join(output, 'results_cluster_2020_brazil_month.pkl'))
df_br = df_br['wbeta']
df = pd.concat([df, df_br], axis=1).rename(columns={'wbeta': 'Brazil'})

df = df['2020-03':]
df = df.apply(lambda x: x * 100).T

print(df.to_latex(float_format='%.2f'))
