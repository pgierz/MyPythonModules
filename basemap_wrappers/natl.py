import sys
sys.path.append('/Users/Paul/MyPythonModules/')

import numpy as np
import scipy as sp
import matplotlib.pyplot as plt

from scipy.io import netcdf
from mpl_toolkits.basemap import Basemap, shiftgrid, addcyclic

def map_natl(ax = plt.gca(), coastlines = True, fill_color = 'aqua', cont_color = 'coral'):
    map = Basemap(width=12000000,height=9000000,
            rsphere=(6378137.00,6356752.3142),\
            resolution='l',area_thresh=1000., projection='lcc',
            lat_1=50.,lat_2=65,lat_0=55,lon_0=-45., ax = ax)
    if coastlines:
       map.drawcoastlines(linewidth = 0.5)
    map.fillcontinents(color = cont_color, lake_color = fill_color, zorder = 0)
    map.drawmapboundary(fill_color = fill_color)
    return map
