def map_carrib(coastlines = True, thisax = plt.gca(), fill_color = 'aqua'):
    """
    Makes a basemap instance of Greenland
    
    Paul J. Gierz
    """
    from mpl_toolkits.basemap import Basemap
    # setup Robinson basemap.
    m = Basemap(llcrnrlat=0, llcrnrlon=-90, urcrnrlat=30, urcrnrlon=-60, resolution = 'c')
    if coastlines:
        m.drawcoastlines()
    if fill_color is not None:
        m.fillcontinents(color='coral',lake_color='aqua')
        m.drawmapboundary(fill_color=fill_color)
    return m
