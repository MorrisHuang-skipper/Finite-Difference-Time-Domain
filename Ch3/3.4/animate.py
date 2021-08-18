import matplotlib.pyplot as plt
import matplotlib as mpl
import numpy as np
from matplotlib import cm
from matplotlib.ticker import LinearLocator, FormatStrFormatter
from mpl_toolkits.mplot3d import Axes3D
import os
from matplotlib.cm import ScalarMappable

mpl.rcParams['font.family'] = 'STIXGeneral'
plt.rcParams['xtick.labelsize'] = 16
plt.rcParams['ytick.labelsize'] = 16
plt.rcParams['font.size'] = 15
plt.rcParams['figure.figsize'] = [5.6, 4.5]
plt.rcParams['axes.titlesize'] = 16
plt.rcParams['axes.labelsize'] = 17
plt.rcParams['lines.linewidth'] = 2
plt.rcParams['lines.markersize'] = 6
plt.rcParams['legend.fontsize'] = 13
plt.rcParams['mathtext.fontset'] = 'stix'
plt.rcParams['axes.linewidth'] = 2

# Generate 2 colors from the 'tab10' colormap
colors = cm.get_cmap('tab20', 2)

# fig = plt.figure()
# ax1 = fig.gca(projection='3d')

# Edit the major and minor ticks of the x and y
# ax1.xaxis.set_tick_params(which='major', size=10, width=2,
#                           direction='in', top='on')
# ax1.xaxis.set_tick_params(which='minor', size=7, width=2,
#                           direction='in', top='on')
# ax1.yaxis.set_tick_params(which='major', size=10, width=2,
#                           direction='in', right='on')
# ax1.yaxis.set_tick_params(which='minor', size=7, width=2,
#                           direction='in', right='on')

# Edit the major and minor tick location
# ax1.xaxis.set_major_locator(mpl.ticker.MultipleLocator(20))
# ax1.xaxis.set_minor_locator(mpl.ticker.MultipleLocator(5))
# ax1.yaxis.set_major_locator(mpl.ticker.MultipleLocator(.6))
# ax1.yaxis.set_minor_locator(mpl.ticker.MultipleLocator(.2))

# ax1.set_ylabel(r'$E_x$', labelpad=10)
# ax1.set_xlim(0, 200)
# ax1.set_ylim(-1.5, 1.5)

for i in range(0, 150, 1):
    number = '{0:04}'.format(i)
    filename = 'field/Ez/' + str(number) + '.dat'
    x, y, z = np.loadtxt(filename, unpack=True)
    x = np.reshape(x, (60, 60))
    y = np.reshape(y, (60, 60))
    z = np.reshape(z, (60, 60))

    # 3d
    fig = plt.figure()
    ax1 = fig.add_subplot(1, 1, 1, projection='3d')
    surf = ax1.plot_surface(y, x, z, cmap=cm.RdBu,
                            vmin=-1, vmax=1)
    ax1.set_zlim(-1, 1)
    fig.suptitle(r'$T=$'+str(i))
    plt.savefig('animation/3d/'+str(number)+'.png', dpi=500)
    ax1.clear()
    plt.close()

    # 2d
    fig = plt.figure()
    ax2 = fig.add_subplot(1, 1, 1)

    ax2.xaxis.set_tick_params(which='major', size=10,
                              width=2, direction='in',
                              top='on')
    ax2.xaxis.set_tick_params(which='minor', size=7,
                              width=2, direction='in',
                              top='on')
    ax2.yaxis.set_tick_params(which='major', size=10,
                              width=2, direction='in',
                              right='on')
    ax2.yaxis.set_tick_params(which='minor', size=7,
                              width=2, direction='in', right='on')
    ax2.xaxis.set_major_locator(mpl.ticker.MultipleLocator(10))
    ax2.xaxis.set_minor_locator(mpl.ticker.MultipleLocator(5))
    ax2.yaxis.set_major_locator(mpl.ticker.MultipleLocator(10))
    ax2.yaxis.set_minor_locator(mpl.ticker.MultipleLocator(5))
    levels = 1000
    vmin, vmax = -1, 1
    level_boundaries = np.linspace(vmin, vmax, levels + 1)
    cs1 = ax2.contourf(y, x, z, level_boundaries,
                       cmap=cm.RdBu, vmin=-1, vmax=1)
    ax2.set_xlabel('cm')
    ax2.set_ylabel('cm')
    # cb = fig.colorbar(cs1, extend='both')

    # Start of solution

    # quadcontourset = ax2.contourf(
    #     y, x, z, level_boundaries, vmin=vmin, vmax=vmax
    # )

    fig.colorbar(ScalarMappable(norm=cs1.norm,
                                cmap=cm.RdBu),
                 ticks=np.arange(vmin, vmax+0.1, 0.2),
                 boundaries=level_boundaries,
                 values=(level_boundaries[:-1] +
                         level_boundaries[1:]) / 2,)

    plt.gca().set_aspect('equal', adjustable='box')
    ax2.set_xlim(0, 60)
    ax2.set_ylim(0, 60)
    ax2.vlines(x=8, ymin=0, ymax=60, ls='--', color='grey')
    ax2.vlines(x=52, ymin=0, ymax=60, ls='--', color='grey')
    ax2.hlines(y=8, xmin=0, xmax=60, ls='--', color='grey')
    ax2.hlines(y=52, xmin=0, xmax=60, ls='--', color='grey')
    fig.suptitle(r'$T=$'+str(i))
    plt.savefig('animation/2d/'+str(number)+'.png', dpi=500)
    ax2.clear()
    plt.close()
os.system('ffmpeg -i animation/2d/%04d.png -c:v ffv1 -qscale:v 0 2d.avi')
os.system('ffmpeg -i animation/3d/%04d.png -c:v ffv1 -qscale:v 0 3d.avi')
