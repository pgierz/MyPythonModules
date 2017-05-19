def plot_var_from_ncdf_file(varname, file, mm, **cfopts):
    import numpy as np
    from mpl_toolkits.basemap import shiftgrid, addcyclic
    RUN = file
    if hasattr(RUN.variables[varname], "_FillValue"):
        var = np.ma.masked_equal(RUN.variables[varname].data.squeeze(), RUN.variables[varname]._FillValue)
    else:
        var = RUN.variables[varname].data.squeeze()
    lon = RUN.variables['lon'].data.squeeze()
    lat = RUN.variables['lat'].data.squeeze()
    var, lon = shiftgrid(180., var, lon, start=False)
    var, lon = addcyclic(var, lon)
    mm.drawmapboundary(fill_color='gray')
    lons, lats = np.meshgrid(lon, lat)
    cf = mm.contourf(lons, lats, var, latlon=True,
                     extend='both',
                     **cfopts)
    return cf

