import matplotlib.pyplot as plt
import matplotlib as mpl
import numpy as np
from matplotlib import cm
from matplotlib.ticker import LinearLocator, FormatStrFormatter
from mpl_toolkits.mplot3d import Axes3D
import os

mpl.rcParams['font.family'] = 'STIXGeneral'
plt.rcParams['xtick.labelsize'] = 16
plt.rcParams['ytick.labelsize'] = 16
plt.rcParams['font.size'] = 15
plt.rcParams['figure.figsize'] = [15, 5]
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

for i in range(100, 150, 1):
    fig = plt.figure()
    ax1 = fig.add_subplot(1, 2, 1, projection='3d')
    # ax1 = fig.gca()
    ax2 = fig.add_subplot(1, 2, 2)
    ax2.xaxis.set_tick_params(which='major',
                              size=10, width=2,
                              direction='in',
                              top='on')
    ax2.yaxis.set_tick_params(which='major',
                              size=10, width=2,
                              direction='in',
                              right='on')
    number = '{0:04}'.format(i)
    filename = 'field/Ez/' + str(number) + '.dat'
    x, y, z = np.loadtxt(filename, unpack=True)
    x = np.reshape(x, (60, 60))
    y = np.reshape(y, (60, 60))
    z = np.reshape(z, (60, 60))
    surf = ax1.plot_surface(x, y, z, cmap=cm.plasma,
                            vmin=0, vmax=0.5)
    ax1.set_zlim(0, 0.5)

    cs1 = ax2.contourf(x, y, z, 20, cmap=cm.plasma,
                       vmin=0, vmax=0.5)
    ax2.set_xlabel('cm')
    ax2.set_ylabel('cm')
    cb = fig.colorbar(cs1)

    fig.suptitle(r'$T=$'+str(i))
    plt.savefig('animation/'+str(number)+'.png', dpi=500)
    ax1.clear()
    ax2.clear()
    ax1.clear()
    plt.close()
# os.system('ffmpeg -r 10 -f image2 -s 750x250 -i animation/%04d.png -vcodec libx265 -crf 20 -pix_fmt yuv420p 2d.mp4')
os.system('ffmpeg -r 10 -i animation/%04d.png -c:v ffv1 -qscale:v 0 2d.avi')
