import matplotlib.pyplot as plt
import matplotlib as mpl
from matplotlib.animation import FuncAnimation
import numpy as np
from pylab import cm
from celluloid import Camera

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
colors = cm.get_cmap('tab20', 2)

fig = plt.figure()
camera = Camera(fig)
ax1 = fig.add_subplot(2, 1, 1)
ax2 = fig.add_subplot(2, 1, 2)

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

# Edit the major and minor tick location
ax1.xaxis.set_major_locator(mpl.ticker.MultipleLocator(20))
ax1.xaxis.set_minor_locator(mpl.ticker.MultipleLocator(5))
ax1.yaxis.set_major_locator(mpl.ticker.MultipleLocator(.2))
ax1.yaxis.set_minor_locator(mpl.ticker.MultipleLocator(.05))
ax2.xaxis.set_major_locator(mpl.ticker.MultipleLocator(20))
ax2.xaxis.set_minor_locator(mpl.ticker.MultipleLocator(5))
ax2.yaxis.set_major_locator(mpl.ticker.MultipleLocator(.4))
ax2.yaxis.set_minor_locator(mpl.ticker.MultipleLocator(.1))


ax1.set_ylabel(r'$E_x$', labelpad=10)
ax2.set_ylabel(r'$H_y$', labelpad=10)
ax2.set_xlabel('FDTD cells', labelpad=10)
ax1.set_xlim(0, 200)
ax2.set_xlim(0, 200)
ax1.set_ylim(-0.5, 1.1)
ax2.set_ylim(-0.5, 1.5)


for i in range(0, 801, 10):
    number = '{0:03}'.format(i)
    filename = 'field/Ex_Hy_' + str(number) + '.dat'
    Ex, Hy = np.loadtxt(filename, unpack=True)
    ax1.plot(Ex, color=colors(0))
    ax2.plot(Hy, color=colors(1))
    ax1.vlines(x=100, ymin=-0.5, ymax=1.1, color='grey')
    ax2.vlines(x=100, ymin=-0.5, ymax=1.5, color='grey')
    camera.snap()

animation = camera.animate()
animation.save('field.mp4')
