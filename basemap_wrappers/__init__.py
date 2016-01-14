def map_global(coastlines=True, thisax=None, fill_color='aqua'):
    """
    Makes a basemap instance for a global robinson map
    Paul J. Gierz
    """
    from mpl_toolkits.basemap import Basemap
    # setup Robinson basemap.
    m = Basemap(projection='robin', lon_0=0, resolution='c', ax=thisax)
    if coastlines:
        m.drawcoastlines(linewidth=0.33)
    if fill_color is not None:
        m.fillcontinents(color='coral', lake_color='aqua')
        m.drawmapboundary(fill_color=fill_color)
    return m
