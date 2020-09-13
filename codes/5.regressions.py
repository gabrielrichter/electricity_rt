# title: 5.regressions.py
# author: Gabriel Richter de Almeida (FGV EPGE)
# date: 2020-09-13

# import modules
import os
import numpy as np
import pandas as pd
import patsy
import statsmodels.api as sm

# set paths
root = r'C:\Users\gabri\Desktop\electricity_rt'
output = os.path.join(root, 'output')

# define lists
region_lst = ['NE', 'N', 'SE-CW', 'S']

# import dataset
df = pd.read_pickle(os.path.join(output, 'df_byregion.pkl'))

# run loop
for i in region_lst:
    region_name = i
    print('Region = ' + region_name)

    # subset dataset
    df_subset = df[(df['region'] == region_name) & (df.index.year >= 2016) & (df.index.year <= 2020)]
    df_subset['ncluster'] = df_subset.groupby([df_subset.index.year, df_subset.index.month]).ngroup()

    df_subset_2020 = df_subset['2020']

    # create dependent and independent variables matrices
    y, x = patsy.dmatrices('np.log(consumption) ~ 1 + C(holiday) + C(hod) + C(dow) + C(woy) + '
                           'np.maximum(temperature - 18, 0)',
                           data=df_subset,
                           return_type='dataframe')

    x_interactions = patsy.dmatrix('C(df_subset_2020.index.dayofyear):C(df_subset_2020.index.year) - 1',
                                   data=df_subset_2020,
                                   return_type='dataframe')  # '-1' removes the constant and allows for the inclusion of
    # the variable C(df_subset_2020.index.dayofyear)[1]:C(df_subset_2020.index.year)[2020]

    x = pd.concat([x, x_interactions], axis=1)
    x = x.fillna(0)  # 0 for years!=2020

    if x['C(woy)[T.53]'].sum() == 0:
        x = x.drop(columns='C(woy)[T.53]')  # avoid multicollinearity by removing a vector of zeros

    df_subset = df_subset.dropna()  # set(df_subset.index) - set(x.index) = {Timestamp('2018-11-04 00:00:00')}

    # check if independent variable matrix has full rank
    if len(x.columns) == np.linalg.matrix_rank(x.to_numpy()):
        print('The independent variables matrix x has full rank.')
    else:
        print('The independent variables matrix x does not have full rank.')

    # # run regressions
    # regression = sm.OLS(y, x).fit(cov_type='HC1')  # Huber–White (heteroskedastic robust) standard errors
    # print(regression.summary())

    regression_cluster = sm.OLS(y, x).fit(cov_type='cluster', cov_kwds={'groups': df_subset['ncluster']})  # standard
    # errors clustered at the year-month level
    print(regression_cluster.summary())

    # # results, HC1 standard errors
    # beta = regression.params
    # ci = regression.conf_int(alpha=0.05, cols=None)  # 95% confidence intervals for standard errors
    #
    # results = pd.concat([beta, ci], axis=1).reset_index()
    # results = results.loc[84:].reset_index(drop=True)
    # results.columns = ['variable', 'beta', 'ci_lb', 'ci_ub']
    #
    # beta_mean = results.loc[:60, 'beta'].mean()
    # results[['beta', 'ci_lb', 'ci_ub']] = results[['beta', 'ci_lb', 'ci_ub']] - beta_mean  # set pre-covid period
    # # (01-01-2020 to 02-29-2020) as the baseline
    #
    # results[['beta', 'ci_lb', 'ci_ub']] = np.exp(results[['beta', 'ci_lb', 'ci_ub']]) - 1  # adjustment for correct
    # # interpretation of coefficients of log-level regressions
    #
    # results.to_pickle(os.path.join(output, f'results_2020_{region_name}.pkl'))

    # results, clustered standard errors
    beta = regression_cluster.params
    ci = regression_cluster.conf_int(alpha=0.05, cols=None)  # 95% confidence intervals for standard errors

    results_cluster = pd.concat([beta, ci], axis=1).reset_index()
    results_cluster = results_cluster.loc[84:].reset_index(drop=True)
    results_cluster.columns = ['variable', 'beta', 'ci_lb', 'ci_ub']

    beta_mean = results_cluster.loc[:59, 'beta'].mean()
    results_cluster[['beta', 'ci_lb', 'ci_ub']] = results_cluster[['beta', 'ci_lb', 'ci_ub']] - beta_mean  # set
    # pre-covid period (01-01-2020 to 02-29-2020) as the baseline

    results_cluster[['beta', 'ci_lb', 'ci_ub']] = np.exp(results_cluster[['beta', 'ci_lb', 'ci_ub']]) - 1  # adjustment
    # for correct interpretation of coefficients of log-level regressions

    results_cluster.to_pickle(os.path.join(output, f'results_cluster_2020_{region_name}.pkl'))
