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
plt.rcParams['figure.figsize'] = [13, 10]
plt.rcParams['axes.titlesize'] = 16
plt.rcParams['axes.labelsize'] = 17
plt.rcParams['lines.linewidth'] = 2
plt.rcParams['lines.markersize'] = 6
plt.rcParams['legend.fontsize'] = 13
plt.rcParams['mathtext.fontset'] = 'stix'
plt.rcParams['axes.linewidth'] = 2

# Generate 2 colors from the 'tab10' colormap
colors = cm.get_cmap('tab20', 2)

for i in range(0, 500, 1):
    fig = plt.figure()
    ax1 = fig.add_subplot(1, 1, 1)
    ax1.xaxis.set_tick_params(which='major',
                              size=10, width=2,
                              direction='in',
                              top='on')
    ax1.yaxis.set_tick_params(which='major',
                              size=10, width=2,
                              direction='in',
                              right='on')
    number = '{0:04}'.format(i)
    filename = 'field/Ez/' + str(number) + '.dat'
    x, y, z = np.loadtxt(filename, unpack=True)
    x = np.reshape(x, (60, 60))
    y = np.reshape(y, (60, 60))
    z = np.reshape(z, (60, 60))
    # ax1.contour(x, y, z, cmap=cm.plasma)
    # ax1.pcolormesh(x, y, z, cmap=cm.plasma)
    cs1 = ax1.contourf(x, y, z, 20, cmap=cm.plasma,
                       vmin=0, vmax=0.5)
    ax1.set_title(r'$T=$'+str(i))
    ax1.set_xlabel('cm')
    ax1.set_ylabel('cm')
    cb = fig.colorbar(cs1)
    plt.savefig('contour/'+str(number)+'.png',
                dpi=500)
    ax1.clear()
    plt.close()
os.system('ffmpeg -r 10 -i contour/%04d.png -c:v ffv1 -qscale:v 0 2d.avi')
