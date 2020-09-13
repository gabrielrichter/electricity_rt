# title: 6.figures.py
# author: Gabriel Richter de Almeida (FGV EPGE)
# date: 2020-09-13

# import modules
import os
import matplotlib  # necessary to modify rcParams
from matplotlib.lines import Line2D
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from matplotlib.dates import DateFormatter
import numpy as np
import pandas as pd

# set paths
root = r'C:\Users\gabri\Desktop\electricity_rt'
figures = os.path.join(root, 'figures')
output = os.path.join(root, 'output')

# define dictionaries
region_dic = {'NE': 'Nordeste', 'N': 'Norte', 'SE-CW': 'Sudeste/Centro-Oeste', 'S': 'Sul'}

# run loop
for i in region_dic.keys():
    region_abbrev = i
    region_name = region_dic[i]
    print('Region = ' + region_name)

    # import dataset
    df = pd.read_pickle(os.path.join(output, f'results_cluster_2020_{region_abbrev}.pkl'))

    # set dataset index to timestamp
    df.index = pd.date_range(start='2020-01-01', end='2020-08-31', freq='D')

    df = df['2020-03':]

    df2 = df['beta'].rolling(window=7).mean()

    # modify default configurations
    matplotlib.rcParams['font.family'] = "sans-serif"
    matplotlib.rcParams['font.sans-serif'] = "Open Sans"
    plt.rc('xtick', labelsize=10)
    plt.rc('ytick', labelsize=10)
    plt.rc('axes', labelsize=10)

    # plot graphs with no 95% confidence intervals
    fig, ax = plt.subplots()

    plt.grid(axis='y',
             color='#d9d9d9',
             linewidth=0.5)

    ax.plot(df.index,
            df['beta'] * 100,
            color='#ffa600',
            linestyle='solid',
            linewidth=1)

    ax.plot(df2.index,
            df2 * 100,
            color='#264653',
            linestyle='dashed',
            linewidth=1)

    if region_abbrev == 'S':
        ax.set(xlabel='',
               ylabel='Variação Relativa ao Período Pré-Covid (%)',
               xlim=['2020-03-01', '2020-09-01'],
               ylim=[-25, 15])
    else:
        ax.set(xlabel='',
               ylabel='Variação Relativa ao Período Pré-Covid (%)',
               xlim=['2020-03-01', '2020-09-01'],
               ylim=[-20, 10])

    ax.xaxis.labelpad = 10
    ax.yaxis.labelpad = 10

    for j in ['right', 'left']:
        ax.spines[j].set_visible(False)

    for k in ['top', 'bottom']:
        ax.spines[k].set_linewidth(0.5)
        ax.spines[k].set_color('#d9d9d9')

    plt.tick_params(axis='both',
                    which='both',
                    bottom=True,
                    left=False,
                    direction='inout',
                    width=0.5,
                    color='#d9d9d9')

    if region_abbrev == 'S':
        plt.axhspan(0, -25, alpha=0.05, zorder=1, color='xkcd:terra cotta')
    else:
        plt.axhspan(0, -20, alpha=0.05, zorder=1, color='xkcd:terra cotta')

    ax.axhline(y=0, linestyle='solid', linewidth=0.75, color='#d9d9d9', zorder=0)

    # legend
    lines = [Line2D([0], [0], color='#ffa600', linewidth=1, linestyle='solid'),
             Line2D([0], [0], color='#264653', linewidth=1, linestyle='dashed')]
    labels = ['Diário', 'MM 7 Dias']
    ax.legend(lines, labels)

    date_form = DateFormatter("%b %d")
    ax.xaxis.set_major_formatter(date_form)
    ax.xaxis.set_major_locator(mdates.WeekdayLocator(interval=2))
    plt.xticks(rotation=45)

    fig.tight_layout()
    plt.savefig(os.path.join(figures, f'results_2020_{region_abbrev}_notitle.pdf'))

    ax.set_title(f'Indicador de Consumo de Eletricidade: {region_name}', fontsize=10, pad=10)
    fig.tight_layout()
    plt.savefig(os.path.join(figures, f'results_2020_{region_abbrev}.pdf'))

    # # plot graphs with 95% confidence intervals
    # fig, ax = plt.subplots()
    #
    # plt.grid(axis='y',
    #          color='#d9d9d9',
    #          linewidth=0.5)
    #
    # ax.plot(df.index,
    #         df['beta'] * 100,
    #         color='#ffa600',
    #         linestyle='solid',
    #         linewidth=1)
    #
    # if region_abbrev == 'S':
    #     ax.set(xlabel='',
    #            ylabel='Change Relative to Pre-Covid (%)',
    #            xlim=[df.index[0], df.index[-1]],
    #            ylim=[-25, 20])
    # else:
    #     ax.set(xlabel='',
    #            ylabel='Change Relative to Pre-Covid (%)',
    #            xlim=[df.index[0], df.index[-1]],
    #            ylim=[-20, 15])
    #
    # ax.xaxis.labelpad = 10
    # ax.yaxis.labelpad = 10
    #
    # for j in ['right', 'left']:
    #     ax.spines[j].set_visible(False)
    #
    # for k in ['top', 'bottom']:
    #     ax.spines[k].set_linewidth(0.5)
    #     ax.spines[k].set_color('#d9d9d9')
    #
    # plt.tick_params(axis='both',
    #                 which='both',
    #                 bottom=True,
    #                 left=False,
    #                 direction='inout',
    #                 width=0.5,
    #                 color='#d9d9d9')
    #
    # if region_abbrev == 'S':
    #     plt.axhspan(0, -25, alpha=0.05, zorder=1, color='xkcd:terra cotta')
    # else:
    #     plt.axhspan(0, -20, alpha=0.05, zorder=1, color='xkcd:terra cotta')
    #
    # ax.axhline(y=0, linestyle='solid', linewidth=0.75, color='#d9d9d9', zorder=0)
    #
    # date_form = DateFormatter("%b %d")
    # ax.xaxis.set_major_formatter(date_form)
    # ax.xaxis.set_major_locator(mdates.WeekdayLocator(interval=2))
    # plt.xticks(rotation=45)
    #
    # ax.plot(df.index,
    #         df['ci_lb'] * 100,
    #         color='#ffa600',
    #         linestyle='dotted',
    #         linewidth=0.25,
    #         alpha=0)
    #
    # ax.plot(df.index,
    #         df['ci_ub'] * 100,
    #         color='#ffa600',
    #         linestyle='dotted',
    #         linewidth=0.25,
    #         alpha=0)
    #
    # ax.fill_between(df.index,
    #                 df['ci_lb'] * 100,
    #                 df['ci_ub'] * 100,
    #                 color='#ffa600',
    #                 linewidth=0.5,
    #                 alpha=0.125)
    #
    # # legend
    # colors = ['#ffa600']
    # lines = [Line2D([0], [0], color=c, alpha=0.125, linewidth=5, linestyle='-') for c in colors]
    # labels = ['95% IC']
    # ax.legend(lines, labels)
    #
    # fig.tight_layout()
    # plt.savefig(os.path.join(figures, f'results_2020_{region_abbrev}_notitle_95ic.pdf'))
    #
    # ax.set_title(f'Electricity Consumption Indicator: {region_name} (Brazil)', fontsize=10, pad=10)
    # fig.tight_layout()
    # plt.savefig(os.path.join(figures, f'results_2020_{region_abbrev}_95ic.pdf'))
