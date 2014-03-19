__author__ = 'Ronaldo'

from mpl_toolkits.mplot3d import Axes3D
from matplotlib import cm
from matplotlib.ticker import LinearLocator, FormatStrFormatter
import matplotlib.pyplot as plt
import numpy as np

plot = plt


#import matplotlib.pyplot as plt
#from pandas.tools.plotting import bootstrap_plot
#ts = pandas.Series(np.random.random(1000))
#bootstrap_plot(ts, color='grey')
#plt.show()



def plotChart(X,Y,Z):

    fig = plt.figure()
    ax = fig.gca(projection='3d')

    surf = ax.plot_surface(X, Y, Z, rstride=1, cstride=1, cmap=cm.coolwarm, linewidth=0, antialiased=False)
    #surf = ax.contour(X, Y, Z, cmap=cm.coolwarm)
    #ax.set_zlim(-1.01, 1.01)


    cset = ax.contour(X, Y, Z, zdir='z', offset=0, cmap=cm.coolwarm)
    cset = ax.contour(X, Y, Z, zdir='x', offset=X.min(), cmap=cm.coolwarm)
    cset = ax.contour(X, Y, Z, zdir='y', offset=Y.max(), cmap=cm.coolwarm)

    ax.zaxis.set_major_locator(LinearLocator(10))
    ax.zaxis.set_major_formatter(FormatStrFormatter('%.02f'))

    fig.colorbar(surf, shrink=0.5, aspect=5)

    ax.set_xlabel('Economy Fare')
    ax.set_ylabel('Business Fare')
    ax.set_zlabel('Profits')
    #ax.set_xlim(-40, 40)
    #ax.set_ylim(-40, 40)
    #ax.set_zlim(-100, 100)


    #plt.show()
    #plt.savefig(".png")