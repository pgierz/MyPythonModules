def map_europe(coastlines=True, thisax=plt.gca(), fill_color='aqua'):
    """
    Makes a basemap instance of Greenland

    Paul J. Gierz
    """
    from mpl_toolkits.basemap import Basemap
    # setup Robinson basemap.
    m = Basemap(width=12000000,height=9000000,projection='lcc',
                resolution='c',lat_1=45.,lat_2=55,lat_0=50,lon_0=15.)
    if coastlines:
        m.drawcoastlines()
    if fill_color is not None:
        m.fillcontinents(color='coral', lake_color='aqua')
        m.drawmapboundary(fill_color=fill_color)
    return m
