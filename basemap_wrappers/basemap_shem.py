import matplotlib.pyplot as plt
def map_shem(coastlines=True, thisax=plt.gca(), fill_color='aqua'):
    """
    Makes a basemap instance of Greenland

    Paul J. Gierz
    """
    from mpl_toolkits.basemap import Basemap
    m = Basemap(projection='spstere', boundinglat=-40,
                lon_0=180, resolution='l', ax=thisax)
    if coastlines:
        m.drawcoastlines()
    if fill_color is not None:
        m.fillcontinents(color='coral', lake_color='aqua')
        m.drawmapboundary(fill_color=fill_color)
    return m
