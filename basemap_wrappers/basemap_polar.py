from mpl_toolkits.basemap import Basemap
import matplotlib.pyplot as plt


def map_nhem(coastlines=True, thisax=plt.gca(), fill_color='aqua'):
    m = Basemap(projection='npstere', boundinglat=55, lon_0=0, ax=thisax)
    if coastlines:
        m.drawcoastlines()
    if fill_color is not None:
        m.fillcontinents(color='coral', lake_color='aqua')
        m.drawmapboundary(fill_color=fill_color)
    return m


def map_shem(coastlines=True, thisax=plt.gca(), fill_color='aqua'):
    m = Basemap(projection='spstere', boundinglat=-55, lon_0=180, ax=thisax)
    if coastlines:
        m.drawcoastlines()
    if fill_color is not None:
        m.fillcontinents(color='coral', lake_color='aqua')
        m.drawmapboundary(fill_color=fill_color)
    return m
