from mpl_toolkits.basemap import Basemap


def map_global(coastlines=True, thisax=None, fill_color='aqua', focus=0):
    """
    Makes a basemap instance for a global robinson map
    Paul J. Gierz
    """
    # setup Robinson basemap.
    m = Basemap(projection='robin', lon_0=focus, resolution='c', ax=thisax)
    # print dir(m)
    if coastlines:
        m.drawcoastlines(linewidth=0.33)
    if fill_color is not None:
        m.fillcontinents(color='coral', lake_color='aqua')
        m.drawmapboundary(fill_color=fill_color)
    return m


def map_natl(coastlines=True, thisax=None, fill_color='aqua', fancy=False):
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
            m.fillcontinents(color='coral', lake_color='aqua')
        m.drawmapboundary(fill_color=fill_color)
    return m


def map_europe(coastlines=True, thisax=None, fill_color='aqua'):
    """
    Makes a basemap instance of Greenland

    Paul J. Gierz
    """
    x1 = -20.
    x2 = 40.
    y1 = 32.
    y2 = 64.
    m = Basemap(resolution='c', projection='merc', llcrnrlat=y1,
                urcrnrlat=y2, llcrnrlon=x1, urcrnrlon=x2, lat_ts=(x1 + x2) / 2,
                ax=thisax)
    if coastlines:
        m.drawcoastlines(linewidth=0.33)
    if fill_color is not None:
        m.fillcontinents(color='coral', lake_color='aqua')
        m.drawmapboundary(fill_color=fill_color)
    return m


def map_shem(coastlines=True, thisax=None, fill_color='aqua'):
    """
    Makes a basemap instance of Greenland

    Paul J. Gierz
    """
    from mpl_toolkits.basemap import Basemap
    m = Basemap(projection='spstere', boundinglat=-55,
                lon_0=180, resolution='l', ax=thisax)
    if coastlines:
        m.drawcoastlines()
    if fill_color is not None:
        m.fillcontinents(color='coral', lake_color='aqua')
        m.drawmapboundary(fill_color=fill_color)
    return m


def map_pacific(coastlines=True, thisax=None, fill_color=None):
    m = Basemap(projection="cyl",
                llcrnrlon=-260.0, llcrnrlat=10.0, urcrnrlon=0.0, urcrnrlat=75.0,
                ax=thisax, resolution='l')
    if coastlines:
        m.drawcoastlines(linewidth=0.33)
    if fill_color is not None:
        m.fillcontinents(color='coral', lake_color='aqua')
        m.drawmapboundary(fill_color=fill_color)
    return m


def map_carrib(coastlines=True, thisax=None, fill_color=None):
    m = Basemap(llcrnrlat=-10, llcrnrlon=-110, urcrnrlat=40, urcrnrlon=-10,
                resolution='c', ax=thisax)
    if coastlines:
        m.drawcoastlines(linewidth=0.33)
    if fill_color is not None:
        m.fillcontinents(color='coral', lake_color='aqua')
        m.drawmapboundary(fill_color=fill_color)
    return m
        
