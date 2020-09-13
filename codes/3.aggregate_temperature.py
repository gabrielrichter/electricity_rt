# title: 3.aggregate_temperature.py
# author: Gabriel Richter de Almeida (FGV EPGE)
# date: 2020-09-13

# import modules
import os
import numpy as np
import pandas as pd

# set paths
root = r'C:\Users\gabri\Desktop\electricity_rt'
temp = os.path.join(root, 'temp')

# define lists and dictionaries
year_lst = [str(i) for i in range(2001, 2021)]
year_dic = {i: [] for i in year_lst}

region = {'AL': 'NE',
          'BA': 'NE',
          'CE': 'NE',
          'PB': 'NE',
          'PE': 'NE',
          'PI': 'NE',
          'RN': 'NE',
          'SE': 'NE',

          'AM': 'N',
          'AP': 'N',
          'MA': 'N',
          'PA': 'N',
          'TO': 'N',

          'ES': 'SE-CW',
          'MG': 'SE-CW',
          'RJ': 'SE-CW',
          'SP': 'SE-CW',
          'AC': 'SE-CW',
          'DF': 'SE-CW',
          'GO': 'SE-CW',
          'MS': 'SE-CW',
          'MT': 'SE-CW',
          'RO': 'SE-CW',

          'PR': 'S',
          'RS': 'S',
          'SC': 'S',

          'RR': np.nan
          }

# import datasets
df_pop = pd.read_pickle(os.path.join(temp, 'population.pkl'))
df_pop = df_pop.reset_index()

# run loop
for i in year_dic.keys():
    year_name = i
    print('Year = ' + year_name)

    df_temp = pd.read_pickle(os.path.join(temp, f'temperature_{year_name}.pkl'))

    # create dataset
    df_temp['year'] = df_temp.index.year  # create 'year' variable, used on merge
    df_temp = df_temp.reset_index()

    # merge population and temperature datasets
    df = df_temp.merge(right=df_pop,
                       how='left',
                       on=['year', 'id_municipality'],
                       suffixes=('', '_y'),
                       indicator=True,
                       validate='m:1'
                       )

    df = df.set_index('date')
    df = df[['state', 'temperature', 'population']]  # select subset of columns

    df = df.dropna(subset=['population'])  # remove nan population values
    df['region'] = df['state'].apply(lambda i: region[i])

    df['region'] = df['region'].astype('category')  # optimize memory usage
    df['population'] = df['population'].astype('int32')  # optimize memory usage

    # aggregate temperature by date and region, weighting by the population size of each municipality within states
    def wavg(group):
        d = group['temperature']
        w = group['population']
        return (d * w).sum() / w.sum()


    grouped = df.groupby(['date', 'region'])
    x = grouped.apply(wavg)
    df = pd.DataFrame(x, columns=['temperature'])
    df = df.reset_index('region')

    year_dic[year_name] = df

df = pd.concat(year_dic.values())  # append datasets

df.to_pickle(os.path.join(temp, 'temperature_byregion.pkl'))  # save dataset in pickle (serialized) format
