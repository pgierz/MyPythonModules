import matplotlib.pyplot as plt
from mpl_toolkits.basemap import Basemap
def map_natl(coastlines=True, thisax=plt.gca(), fill_color='aqua', fancy=False):
    """
    Makes a basemap instance of Greenland
    
    Paul J. Gierz
    """
    if not fancy:
        m = Basemap(width=12000000, height=9000000,
                    rsphere=(6378137.00, 6356752.3142),
                    resolution='l', area_thresh=1000., projection='lcc',
                    lat_1=50., lat_2=65, lat_0=55, lon_0=-45., ax=thisax)
    else:
        m = Basemap(projection="ortho", lat_0=55, lon_0=-45,
                    resolution='c', ax=thisax)
    if coastlines:
        m.drawcoastlines()
    if fill_color is not None:
        m.fillcontinents(color='coral',lake_color='aqua')
        m.drawmapboundary(fill_color=fill_color)
    return m


