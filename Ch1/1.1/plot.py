import matplotlib.pyplot as plt
import matplotlib as mpl
import numpy as np
from pylab import cm

mpl.rcParams['font.family'] = 'STIXGeneral'
plt.rcParams['xtick.labelsize'] = 16
plt.rcParams['ytick.labelsize'] = 16
plt.rcParams['font.size'] = 15
plt.rcParams['figure.figsize'] = [10, 5]
plt.rcParams['axes.titlesize'] = 16
plt.rcParams['axes.labelsize'] = 17
plt.rcParams['lines.linewidth'] = 2
plt.rcParams['lines.markersize'] = 6
plt.rcParams['legend.fontsize'] = 13
plt.rcParams['mathtext.fontset'] = 'stix'
plt.rcParams['axes.linewidth'] = 2

# Generate 2 colors from the 'tab10' colormap
colors = cm.get_cmap('tab10', 4)
j = 0
for i in range(0, 1000, 5):
    fig = plt.figure()
    ax1 = fig.add_subplot(1, 1, 1)
    ax1.xaxis.set_tick_params(which='major', size=10, width=2,
                              direction='in', top='on')
    ax1.xaxis.set_tick_params(which='minor', size=7, width=2,
                              direction='in', top='on')
    ax1.yaxis.set_tick_params(which='major', size=10, width=2,
                              direction='in', right='on')
    ax1.yaxis.set_tick_params(which='minor', size=7, width=2,
                              direction='in', right='on')
# Edit the major and minor tick location
    ax1.xaxis.set_major_locator(mpl.ticker.MultipleLocator(20))
    ax1.xaxis.set_minor_locator(mpl.ticker.MultipleLocator(5))
    ax1.yaxis.set_major_locator(mpl.ticker.MultipleLocator(.5))
    ax1.yaxis.set_minor_locator(mpl.ticker.MultipleLocator(.1))

    ax1.set_ylabel(r'$E_x \quad H_y$', labelpad=10)
    ax1.set_xlabel('cell', labelpad=10)
    ax1.set_xlim(0, 200)
    ax1.set_ylim(-2.2, 2.2)
    ax1.grid()
    number = '{0:04}'.format(i)
    filename = 'periodic/Ex_Hy_' + str(number) + '.dat'
    Ex, Hy = np.loadtxt(filename, unpack=True)
    ax1.plot(Ex, color=colors(0), label=r'$E_x$')
    ax1.plot(Hy, color=colors(1), label=r'$H_y$')
    ax1.legend()
    ax1.set_title(r'$T=$'+str(i))
    number = '{0:04}'.format(j)
    plt.savefig('animation_periodic/'+str(number)+'.pdf')
    ax1.clear()
    plt.close()
    j = j + 1
