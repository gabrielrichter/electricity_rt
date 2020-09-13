# title: 6.figures_brazil.py
# author: Gabriel Richter de Almeida (FGV EPGE)
# date: 2020-09-13

# import modules
import os
import matplotlib  # necessary to modify rcParams
import matplotlib.dates as mdates
import matplotlib.pyplot as plt
import pandas as pd
from matplotlib.dates import DateFormatter
from matplotlib.lines import Line2D

# set paths
root = r'C:\Users\gabri\Desktop\electricity_rt'
figures = os.path.join(root, 'figures')
output = os.path.join(root, 'output')

# import dataset
df = pd.read_pickle(os.path.join(output, 'results_cluster_2020_brazil.pkl'))

df = df['2020-03':]

df2 = df['wbeta'].rolling(window=7).mean()

# modify default configurations
matplotlib.rcParams['font.family'] = "sans-serif"
matplotlib.rcParams['font.sans-serif'] = "Open Sans"
plt.rc('xtick', labelsize=10)
plt.rc('ytick', labelsize=10)
plt.rc('axes', labelsize=10)

# plot graphs
fig, ax = plt.subplots()

plt.grid(axis='y',
         color='#d9d9d9',
         linewidth=0.5)

ax.plot(df.index,
        df['wbeta'] * 100,
        color='#ffa600',
        linestyle='solid',
        linewidth=1)

ax.plot(df2.index,
        df2 * 100,
        color='#264653',
        linestyle='dashed',
        linewidth=1)

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
plt.savefig(os.path.join(figures, 'results_2020_brazil_notitle.pdf'))

ax.set_title('Indicador de Consumo de Eletricidade: Brasil', fontsize=10, pad=10)
fig.tight_layout()
plt.savefig(os.path.join(figures, 'results_2020_brazil.pdf'))
