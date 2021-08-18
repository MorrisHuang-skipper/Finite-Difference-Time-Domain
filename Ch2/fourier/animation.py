import matplotlib.pyplot as plt
import matplotlib as mpl
import numpy as np
from pylab import cm

mpl.rcParams['font.family'] = 'STIXGeneral'
plt.rcParams['xtick.labelsize'] = 16
plt.rcParams['ytick.labelsize'] = 16
plt.rcParams['font.size'] = 15
plt.rcParams['figure.figsize'] = [10, 10]
plt.rcParams['axes.titlesize'] = 16
plt.rcParams['axes.labelsize'] = 17
plt.rcParams['lines.linewidth'] = 2
plt.rcParams['lines.markersize'] = 6
plt.rcParams['legend.fontsize'] = 13
plt.rcParams['mathtext.fontset'] = 'stix'
plt.rcParams['axes.linewidth'] = 2

# Generate 2 colors from the 'tab10' colormap
colors = cm.get_cmap('tab10', 5)
j = 0
for i in range(0, 2500, 5):
    fig = plt.figure()
    ax1 = fig.add_subplot(2, 1, 1)
    ax2 = fig.add_subplot(2, 1, 2)
    ax1.xaxis.set_tick_params(which='major', size=10, width=2,
                              direction='in', top='on')
    ax1.xaxis.set_tick_params(which='minor', size=7, width=2,
                              direction='in', top='on')
    ax1.yaxis.set_tick_params(which='major', size=10, width=2,
                              direction='in', right='on')
    ax1.yaxis.set_tick_params(which='minor', size=7, width=2,
                              direction='in', right='on')
    ax2.xaxis.set_tick_params(which='major', size=10, width=2,
                              direction='in', top='on')
    ax2.xaxis.set_tick_params(which='minor', size=7, width=2,
                              direction='in', top='on')
    ax2.yaxis.set_tick_params(which='major', size=10, width=2,
                              direction='in', right='on')
    ax2.yaxis.set_tick_params(which='minor', size=7, width=2,
                              direction='in', right='on')
# Edit the major and minor tick location
    ax1.xaxis.set_major_locator(mpl.ticker.MultipleLocator(20))
    ax1.xaxis.set_minor_locator(mpl.ticker.MultipleLocator(5))
    ax1.yaxis.set_major_locator(mpl.ticker.MultipleLocator(.5))
    ax1.yaxis.set_minor_locator(mpl.ticker.MultipleLocator(.1))
    ax1.set_ylabel(r'$E_x \quad H_y$')
    ax1.set_xlabel('cell')
    ax1.set_xlim(0, 200)
    ax1.set_ylim(-2.2, 2.2)
    ax1.grid()
    number = '{0:04}'.format(i)
    filename = 'data/Ex_Hy_' + str(number) + '.dat'
    Ex, Hy = np.loadtxt(filename, unpack=True)
    ax1.plot(Ex, color=colors(0), label=r'$E_x$')
    ax1.plot(Hy, color=colors(1), label=r'$H_y$')
    ax1.legend()
    ax1.set_title(r'$T=$'+str(i))
    ax1.axvspan(100, 160, color='grey', alpha=0.5)

    filename = 'data/reflect' + str(number) + '.dat'
    ampn1 = np.loadtxt(filename, unpack=True)
    ax2.plot(range(1, 1001), ampn1**2, color=colors(2), label='refelctence')
    ax2.set_ylim(0, 1.2)

    filename = 'data/trans' + str(number) + '.dat'
    ampn2 = np.loadtxt(filename, unpack=True)
    ax2.plot(range(1, 1001), ampn2**2, color=colors(3), label='transmittance')
    ax2.set_ylim(0, 1.5)

    ax2.plot(range(1, 1001), ampn1**2+ampn2**2, color=colors(4), label='total')

    ax2.legend()
    ax2.set_xlabel(r'$frequency(MHz)$')
    number = '{0:04}'.format(j)
    plt.savefig('animation/'+str(number)+'.pdf')
    ax1.clear()
    plt.close()
    j = j + 1
