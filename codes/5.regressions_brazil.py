# title: 5.regressions_brazil.py
# author: Gabriel Richter de Almeida (FGV EPGE)
# date: 2020-09-13

# import modules
import os
import numpy as np
import pandas as pd

# set path
root = r'C:\Users\gabri\Desktop\electricity_rt'
output = os.path.join(root, 'output')

# define lists and dictionaries
region_lst = ['NE', 'N', 'SE-CW', 'S']

region_dic = {x: [] for x in region_lst}

# import datasets
df = pd.read_pickle(os.path.join(output, 'df_byregion.pkl'))

for i in region_lst:
    region_dic[i] = pd.read_pickle(os.path.join(output, f'results_cluster_2020_{i}.pkl'))
    region_dic[i] = region_dic[i][['variable', 'beta']]
    region_dic[i]['date'] = pd.date_range(start='2020-01-01', end='2020-08-31')
    region_dic[i]['region'] = i

df_results = pd.concat(region_dic.values())

# clean datasets
df = df['2016':'2019'][['region', 'consumption']]

# create weight variable
df_weight = df.groupby('region').aggregate(
    {'consumption': np.sum}).rename(columns={'consumption': 'weight'})

df_weight = df_weight / df_weight.sum()
df_weight = df_weight.reset_index()

# merge datasets
df_results = df_results.merge(right=df_weight,
                              how='left',
                              on='region',
                              validate='m:1')

# create weighted beta variables
df_stats = df_results.groupby('variable').aggregate(
    {'beta': lambda x: np.average(x, weights=df_results.loc[x.index, 'weight'])}).rename(columns={'beta': 'wbeta'})

df_results = df_results.merge(right=df_stats,
                              how='left',
                              left_on=['variable'],
                              right_index=True,
                              validate='m:1')

df_results = df_results.set_index('date')
df_results = df_results[['variable', 'wbeta']]
df_results = df_results[~df_results.index.duplicated()]
df_results = df_results.sort_index()

df_results.to_pickle(os.path.join(output, 'results_cluster_2020_brazil.pkl'))
