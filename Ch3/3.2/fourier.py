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
colors = cm.get_cmap('tab20', 5)

fig = plt.figure()
ax1 = fig.add_subplot(5, 1, 1)
ax2 = fig.add_subplot(5, 1, 2)
ax3 = fig.add_subplot(5, 1, 3)
ax4 = fig.add_subplot(5, 1, 4)
ax5 = fig.add_subplot(5, 1, 5)

# Edit the major and minor ticks of the x and y
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
ax3.xaxis.set_tick_params(which='major', size=10, width=2,
                          direction='in', top='on')
ax3.xaxis.set_tick_params(which='minor', size=7, width=2,
                          direction='in', top='on')
ax3.yaxis.set_tick_params(which='major', size=10, width=2,
                          direction='in', right='on')
ax3.yaxis.set_tick_params(which='minor', size=7, width=2,
                          direction='in', right='on')
ax4.xaxis.set_tick_params(which='major', size=10, width=2,
                          direction='in', top='on')
ax4.xaxis.set_tick_params(which='minor', size=7, width=2,
                          direction='in', top='on')
ax4.yaxis.set_tick_params(which='major', size=10, width=2,
                          direction='in', right='on')
ax4.yaxis.set_tick_params(which='minor', size=7, width=2,
                          direction='in', right='on')
ax5.xaxis.set_tick_params(which='major', size=10, width=2,
                          direction='in', top='on')
ax5.xaxis.set_tick_params(which='minor', size=7, width=2,
                          direction='in', top='on')
ax5.yaxis.set_tick_params(which='major', size=10, width=2,
                          direction='in', right='on')
ax5.yaxis.set_tick_params(which='minor', size=7, width=2,
                          direction='in', right='on')

# Edit the major and minor tick location
ax1.xaxis.set_major_locator(mpl.ticker.MultipleLocator(20))
ax1.xaxis.set_minor_locator(mpl.ticker.MultipleLocator(5))
ax1.yaxis.set_major_locator(mpl.ticker.MultipleLocator(.5))
ax1.yaxis.set_minor_locator(mpl.ticker.MultipleLocator(.1))
ax2.xaxis.set_major_locator(mpl.ticker.MultipleLocator(20))
ax2.xaxis.set_minor_locator(mpl.ticker.MultipleLocator(5))
ax2.yaxis.set_major_locator(mpl.ticker.MultipleLocator(.5))
ax2.yaxis.set_minor_locator(mpl.ticker.MultipleLocator(.1))
ax3.xaxis.set_major_locator(mpl.ticker.MultipleLocator(20))
ax3.xaxis.set_minor_locator(mpl.ticker.MultipleLocator(5))
ax3.yaxis.set_major_locator(mpl.ticker.MultipleLocator(.5))
ax3.yaxis.set_minor_locator(mpl.ticker.MultipleLocator(.1))
ax4.xaxis.set_major_locator(mpl.ticker.MultipleLocator(20))
ax4.xaxis.set_minor_locator(mpl.ticker.MultipleLocator(5))
ax4.yaxis.set_major_locator(mpl.ticker.MultipleLocator(.5))
ax4.yaxis.set_minor_locator(mpl.ticker.MultipleLocator(.1))
ax5.xaxis.set_major_locator(mpl.ticker.MultipleLocator(20))
ax5.xaxis.set_minor_locator(mpl.ticker.MultipleLocator(5))
ax5.yaxis.set_major_locator(mpl.ticker.MultipleLocator(.5))
ax5.yaxis.set_minor_locator(mpl.ticker.MultipleLocator(.1))

ax1.set_xlim(0, 200)
ax2.set_xlim(0, 200)
ax3.set_xlim(0, 200)
ax4.set_xlim(0, 200)
ax5.set_xlim(0, 200)
ax1.set_ylim(-0.4, 1)
# ax2.set_ylim(-.004, .002)
ax3.set_ylim(0, 2)
ax4.set_ylim(0, 2)
ax5.set_ylim(0, 2)
ax1.set_ylabel(r'$E_x$', labelpad=10)
ax2.set_ylabel(r'$E_x$', labelpad=10)
ax3.set_ylabel(r'$amp_0$', labelpad=10)
ax4.set_ylabel(r'$amp_1$', labelpad=10)
ax5.set_ylabel(r'$amp_2$', labelpad=10)
ax5.set_xlabel('FDTD cell', labelpad=10)

ax1.vlines(x=100, ymin=-1, ymax=1, color='grey')
# ax2.vlines(x=100, ymin=0, ymax=1.5, color='grey')
ax3.vlines(x=100, ymin=0, ymax=2, color='grey')
ax4.vlines(x=100, ymin=0, ymax=2, color='grey')
ax5.vlines(x=100, ymin=0, ymax=2, color='grey')

ax1.set_title(r'Time Domain $T = 200$')
ax2.set_title(r'Time Domain $T = 1000$')
ax3.set_title(r'Freq. Domain at 50MHz')
ax4.set_title(r'Freq. Domain at 200MHz')
ax5.set_title(r'Freq. Domain at 500MHz')

Ex, Hy = np.loadtxt('field/Ex_Hy_0250.dat', unpack=True)
ax1.plot(Ex, color=colors(0))
Ex, Hy = np.loadtxt('field/Ex_Hy_1000.dat', unpack=True)
ax2.plot(Ex, color=colors(1))
amp0 = np.loadtxt('fourier/1000step/amp0')
amp1 = np.loadtxt('fourier/1000step/amp1')
amp2 = np.loadtxt('fourier/1000step/amp2')
ax3.plot(amp0, color=colors(2))
ax4.plot(amp1, color=colors(3))
ax5.plot(amp2, color=colors(4))

plt.tight_layout()
plt.savefig('Fig2.3.svg')
plt.show()
