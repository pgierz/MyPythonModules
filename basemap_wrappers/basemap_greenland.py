from mpl_toolkits.basemap import Basemap
import matplotlib.pyplot as plt

def map_greenland(coastlines = True, thisax = plt.gca(), fill_color = 'aqua'):
    """
    Makes a basemap instance of Greenland
    
    Paul J. Gierz
    """
    # setup stereographic basemap.
    # lat_ts is true latitude.
    # lon_0,lat_0 is central point.
    # rsphere=(6378137.00,6356752.3142) specifies WGS4 ellipsoid
    # area_thresh=1000 means don't plot coastline features less
    # than 1000 km^2 in area.
    m = Basemap(width=2000000,height=3000000,
                rsphere=(6378137.00,6356752.3142),\
                resolution='l',area_thresh=1000.,projection='stere',\
                lat_ts=72., lat_0=72, lon_0=-40., ax = thisax)
    if coastlines:
        m.drawcoastlines()
    if fill_color is not None:
        m.fillcontinents(color='coral',lake_color='aqua')
        m.drawmapboundary(fill_color=fill_color)
    return m


map_greenland()
plt.show()
