import matplotlib.pyplot as plt
from mpl_toolkits.basemap import Basemap

def map_pacif(coastlines=True, thisax=plt.gca(), fill_color='aqua'):
    m = Basemap(projection='cyl',
                llcrnrlat=-60, urcrnrlat=60,
                llcrnrlon=-270, urcrnrlon=-60,
                resolution='c', ax=thisax)
    if coastlines:
        m.drawcoastlines()
    if fill_color is not None:
        m.fillcontinents(color='black', lake_color='black')
        m.drawmapboundary(fill_color=fill_color)
    return m



def map_npacif(coastlines=True, thisax=plt.gca(), fill_color='aqua', fancy=False):
    if fancy:
        print "fancy version"
        m = Basemap(projection='ortho',
                    lat_0=60, lon_0=180,
                    resolution='c', ax=thisax)
    else:        
        m = Basemap(projection='cyl',
                    llcrnrlat=-30, urcrnrlat=90,
                    llcrnrlon=-270, urcrnrlon=-60,
                    resolution='c', ax=thisax)
        
    if coastlines:
        m.drawcoastlines()
    if fill_color is not None:
        m.fillcontinents(color='black', lake_color='black')
        m.drawmapboundary(fill_color=fill_color)
    return m



def map_pacific_enso_region(coastlines=True, thisax=plt.gca(), fill_color='aqua'):
    m = Basemap(projection='cyl',
                llcrnrlat=-20, urcrnrlat=20,
                llcrnrlon=100.0, urcrnrlon=360.0-80.0,
                resolution='c', ax=thisax)
    if coastlines:
        m.drawcoastlines()
    if fill_color is not None:
        m.fillcontinents(color='black', lake_color='black')
        m.drawmapboundary(fill_color=fill_color)
    return m
