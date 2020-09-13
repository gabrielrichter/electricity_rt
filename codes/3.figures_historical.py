# title: 3.figures_historical.py
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
df = pd.read_pickle(os.path.join(output, 'historical.pkl'))

df = df['2004':]  # subset less volatile period of electricity consumption

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
        df['consumption_yoy'],
        color='#ffa600',
        linestyle='solid',
        linewidth=1.25)

ax.plot(df.index,
        df['gdp_yoy'],
        color='#665191',
        linestyle='solid',
        linewidth=1.25)

ax.set(xlabel='',
       ylabel='Variação YoY (%)',
       xlim=['2003-12-01', '2021-01-01'],
       ylim=[-15, 15])

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

plt.xticks(rotation=45)

ax.axhline(y=0, linestyle='solid', linewidth=0.75, color='#d9d9d9', zorder=0)

plt.axvspan('2007-12-01', '2009-06-30', alpha=0.05, zorder=1, color='xkcd:terra cotta')
plt.axvspan('2020-02-29', '2020-09-01', alpha=0.05, zorder=1, color='xkcd:terra cotta')

ax.text('2007-05-01', -9.5, 'Crise de 2008', ha='left', size=10)

ax.annotate(text='– 9.5%', xy=('2020-06-01', -9.5),  xycoords='data', color='#ffa600', size=10,
            xytext=(-50, -25), textcoords='offset points',
            arrowprops=dict(arrowstyle='->', color='#ffa600', connectionstyle='angle3,angleA=0,angleB=-120'))

ax.annotate(text='– 11.4%', xy=('2020-06-01', -11.4),  xycoords='data', color='#665191', size=10,
            xytext=(-60, -25), textcoords='offset points',
            arrowprops=dict(arrowstyle='->', color='#665191', connectionstyle='angle3,angleA=0,angleB=-120'))

# legend
colors = ['#ffa600', '#665191']
lines = [Line2D([0], [0], color=c, linewidth=5, linestyle='-') for c in colors]
labels = ['Eletricidade', 'PIB']
ax.legend(lines, labels, bbox_to_anchor=(0.925, 1))

fig.tight_layout()
plt.savefig(os.path.join(figures, 'historical_notitle.pdf'))

ax.set_title(r'Consumo de Eletricidade vs. PIB: Brasil, por Trimestre', fontsize=10, pad=10)
fig.tight_layout()
plt.savefig(os.path.join(figures, 'historical.pdf'))
