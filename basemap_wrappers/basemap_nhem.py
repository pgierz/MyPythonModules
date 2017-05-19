import matplotlib.pyplot as plt
from mpl_toolkits.basemap import Basemap


def map_nhem(coastlines=True, thisax=plt.gca(), fill_color='aqua'):
    """
    Makes a basemap instance of Greenland
    
    Paul J. Gierz
    """
    m = Basemap(projection='npstere', boundinglat=55, lon_0=0, ax=thisax)
    if coastlines:
        m.drawcoastlines(linewidth=0.33)
    if fill_color is not None:
        m.fillcontinents(color='coral', lake_color='aqua')
        m.drawmapboundary(fill_color=fill_color)
    return m


