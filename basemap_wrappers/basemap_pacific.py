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
