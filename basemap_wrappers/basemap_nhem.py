def map_nhem(coastlines=True, thisax=plt.gca(), fill_color='aqua'):
    """
    Makes a basemap instance of Greenland
    
    Paul J. Gierz
    """
    m = Basemap(projection='npstere', boundinglat=45, lon_0=0, ax=thisax)
    if coastlines:
        m.drawcoastlines()
    if fill_color is not None:
        m.fillcontinents(color='coral',lake_color='aqua')
        m.drawmapboundary(fill_color=fill_color)
    return m


