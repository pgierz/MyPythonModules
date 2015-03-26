# Ok, lets see if I can successfully figure out how to use decorators today...

# Let us start by making a function as we would regulalry want it to be in the plot absolute case for a global map:

def plot_nc_map_global(file, variable):
    # This all happens before the actual plot command
    f = get_remote_data(file)
    v = f.variables[variable].data.squeeze()
    lon = f.variables['lon'].data.squeeze()
    lat = f.variables['lat'].data.squeeze()
    v, lon = shiftgrid(180., v, lon, start=False)
    v, lon = addcyclic(v, lon)
    lons, lats = np.meshgrid(lon, lat)
    # This is where we actually say things that control the contourf plot: basemap type and contourf args
    mm = map_global(fill_color=None)
    mm.drawmapboundary(fill_color='gray')
    cf = mm.contourf(lons, lats, anom, latlon=True,
                     levels=assign_contourf_level_opts(args),
                     cmap=assign_colormap_opts(args),
                     extend='both')
    mm.colorbar(cf)
    # This happens after the plot


def wrapper_for_basemap_plots(func):
    
    def _wrapper_for_basemap_plots(*args, **kwargs):
        # This all happens before the actual plot command
        f = get_remote_data(file)
        v = f.variables[variable].data.squeeze()
        lon = f.variables['lon'].data.squeeze()
        lat = f.variables['lat'].data.squeeze()
        v, lon = shiftgrid(180., v, lon, start=False)
        v, lon = addcyclic(v, lon)
        lons, lats = np.meshgrid(lon, lat)
        
        ret = func(*args, **kwargs)
        
        return ret

    return _wrapper_for_basemap_plots

### Alright fuck it I have actual work I should be doing...
