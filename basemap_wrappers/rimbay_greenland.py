#! /opt/local/bin/python
"""
rimbay_greenland.py
Lives:	/Users/Paul/MyPythonModules/basemap_wrappers/rimbay_greenland.py

Contains map_greenland function: Makes a basemap instance centered around
greenland and returns it for further plotting

Paul Gierz Mon Sep  1 10:57:29 2014
"""
import sys
sys.path.append('/Users/Paul/MyPythonModules/')

import numpy as np
import scipy as sp
import matplotlib.pyplot as plt

from scipy.io import netcdf
from mpl_toolkits.basemap import Basemap, shiftgrid, addcyclic

def map_greenland(ax = plt.gca(), coastlines = True, fill_color = 'aqua', cont_color = 'coral'):
    """
    Generates a basemap instance with a focus around greenland, fills coastlines and background colors
    
    Arguments:
    - `ax`: which axis to use; defaults to current axis
    - `coastlines`: plot coastlines, defaults to True
    - `fill_color`: which color to plot missing values in, defaults to aqua (ocean blue)
    """
    map = Basemap(projection = 'stere',
                  lat_0 = 72.0,
                  lon_0 = -40.0,
                  lat_ts = 72.0,
                  height = 3000000,
                  width = 3500000,
                  resolution = 'l',
                  ax = ax)
    if coastlines:
        map.drawcoastlines(linewidth = 0.5)
    map.fillcontinents(color = cont_color, lake_color = fill_color, zorder = 0)	
    map.drawmapboundary(fill_color = fill_color)	   
    return map
