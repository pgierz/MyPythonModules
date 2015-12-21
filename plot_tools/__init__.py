"""
Some useful plot tools that are needed frequently

Paul J. Gierz, Wed Jul 15 15:46:00 2015
"""
import numpy as np
import matplotlib.pyplot
import scipy.io.netcdf
from mpl_toolkits.basemap import shiftgrid, addcyclic


def mask_out_zeros(dat, tolerance, verbose=False):
    """
    Masks out zeros of a dat with a padding given by tolerance

    Keyword Arguments:
    dat       -- the data array
    tolerance -- the padding range (either as tuple, or float)


    # TODO: Some example
    # TODO: tests
    """
    if type(tolerance) is tuple:
        if len(tolerance) is 2:
            dat = np.ma.masked_inside(dat, tolerance[0], tolerance[1])
            toleranceprint = (tolerance[0], tolerance[1])
        # TODO: else: raise error
    elif type(tolerance) in [float, int, np.float64]:
        dat = np.ma.masked_inside(dat, tolerance * -1, tolerance)
        toleranceprint = tolerance
    if type(tolerance) is str:
        if tolerance is "auto":
            percent = 0.01
        else:
            percent = float(tolerance)
        dat = np.ma.masked_inside(
            dat, percent * (dat.max() - dat.min()), -1 * percent * (dat.max() - dat.min()))
        toleranceprint = percent * (dat.max() - dat.min())
    else:
        print "Something went wrong, nothing masked!"
        print type(tolerance)
    if verbose:
        print "PG: percent was:", percent
        print "PG: Range was: ", (dat.max() - dat.min())
        print "PG: Masked out ", sum(sum(dat.mask)), "values that are inside of ", toleranceprint
        # PG: I don't know why this needs to be a double sum, for
        # some reason sum(dat.mask) produces a list
    return dat, dat.mask


def parse_units_to_latex(unit_string):
    """ Converts common typing into latex
    Keyword Arguments:
    unit_string -- 
    """
    # ** is $^{}$
    unit_string = unit_string.split("**")[0]+"$^{"+unit_string.split("**")[1]+"}$"

    ###################################################################
    # NOTE:
    ###################################################################
    # This isn't done yet. It needs to do something like astropy does,
    # but netcdf apparently isn't that sexy from what I can
    # tell. Since I don't do this often, I can convert the final unit
    # to nice latex by hand right before publication, but it'd be nice
    # if it happened automatically.
    ###################################################################


def _decorate_x_axes_for_ymonmean(ax):
    # Some decoration stuff
    ax.set_xlabel("Month")
    ax.set_xlim(-1, 12)
    ax.xaxis.set_ticks(np.arange(12))
    ax.xaxis.set_ticklabels(["J", "F", "M", "A", "M", "J", "J", "A", "S", "O", "N", "D"])
    return ax

    
def _find_nearest_idx(array, value):
    idx = (np.abs(array - value)).argmin()
    return idx


def plot_ymonmean_at_lat_lon(dat, var, lats, lons, ax=matplotlib.pyplot.gca(), **kwargs):
    """This function plots and dataset of a ymonmean input file in 3
    dimensions (lat, lon, time) and plots a monthly cycle of that
    variable at a specified lat and lon.

    If multiple (lats, lons) are given, a mean is made over those lats
    and lons.

    Paul J. Gierz, Tue Aug 11 20:58:15 2015

    Keyword Arguments:
    dat  -- the data to plot. Should be a netcdf.netcdf_file instance!
    var  -- the variable string
    lats -- the lat or lats to look at (should be between -90 and 90)
    lons -- the lon or lons to look at (should be between 0 and 360)
    ax   -- (default matplotlib.pyplot.cga())
    **kwargs -- matplotlib.pyplot.plot keywords

    returns the plt.plot instance.
    """
    # This is wrong. We NEED to have dat in 3 dimensions. I need to
    # instead test if lats, lons are only len 1 or many
    assert type(dat) is scipy.io.netcdf.netcdf_file
    assert dat.variables[var].data.shape[dat.variables[var].dimensions.index("time")] == 12
    plot_dat = dat.variables[var].data.squeeze()
    lon_list = dat.variables['lon'].data.squeeze()
    lat_list = dat.variables['lat'].data.squeeze()
    time = np.arange(12)
    llon, llat = np.meshgrid(lons, lats)
    use_lons, use_lats = [], []
    if type(lats) in [int, float]:
        lats = [lats]
    if type(lons) in [int, float]:
        lons = [lons]    
    for i, j in zip(range(len(lats)), range(len(lons))):
        use_lats.append(_find_nearest_idx(lat_list, lats[i]))
        use_lons.append(_find_nearest_idx(lon_list, lons[j]))
    plot_dat = plot_dat[:, use_lats, use_lons]
    plot_dat.reshape((plot_dat.shape[0], -1)).mean(axis=1)
    # plot_dat = plot_dat[:, use_lats, use_lons].mean(axis=(1, 2))
    p = ax.plot(time, plot_dat, **kwargs)

    # Some decoration stuff
    ax = _decorate_x_axes_for_ymonmean(ax)
    ax.set_ylabel(dat.variables[var].long_name+" ("+dat.variables[var].units+")")
    return p


def plot_ymonmean_from_ncdf_var(dat, var, ax=matplotlib.pyplot.gca(), **kwargs):
    """This function plots and dataset of a ymonmean input file in 2
    dimensions (time, val) and plots a monthly cycle of that
    variable

    Paul J. Gierz, Wed Aug 12 10:54:12 2015

    Keyword Arguments:
    dat  -- the data to plot. Should be a netcdf.netcdf_file
    var  -- the variable string
    ax   -- (default matplotlib.pyplot.cga())
    **kwargs -- matplotlib.pyplot.plot keywords

    returns the plt.plot instance.
    """
    # This is wrong. We NEED to have dat in 3 dimensions. I need to
    # instead test if lats, lons are only len 1 or many
    assert type(dat) is scipy.io.netcdf.netcdf_file
    assert dat.variables[var].data.shape[dat.variables[var].dimensions.index("time")] == 12
    plot_dat = dat.variables[var].data.squeeze()
    time = np.arange(12)
    p = ax.plot(time, plot_dat, **kwargs)
    # Some decoration stuff
    ax = _decorate_x_axes_for_ymonmean(ax)
    ax.set_ylabel(dat.variables[var].long_name+" ("+dat.variables[var].units+")")
    return p


def plot_var_from_ncdf_file(varname, file, mm, **cfopts):
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


def plot_var_anom_from_ncdf_file(varname, file, cfile, mm, **cfopts):
    RUN = file
    CTL = cfile
    if hasattr(RUN.variables[varname], "_FillValue"):
        var = np.ma.masked_equal(RUN.variables[varname].data.squeeze(), RUN.variables[varname]._FillValue)
    else:
        var = RUN.variables[varname].data.squeeze()
    if hasattr(CTL.variables[varname], "_FillValue"):
        ctl = np.ma.masked_equal(CTL.variables[varname].data.squeeze(), CTL.variables[varname]._FillValue)
    else:
        ctl = CTL.variables[varname].data.squeeze()
    lon = RUN.variables['lon'].data.squeeze()
    lat = RUN.variables['lat'].data.squeeze()
    var = var - ctl
    var, lon = shiftgrid(180., var, lon, start=False)
    var, lon = addcyclic(var, lon)
    mm.drawmapboundary(fill_color='gray')
    lons, lats = np.meshgrid(lon, lat)
    cf = mm.contourf(lons, lats, var, latlon=True,
                     extend='both',
                     **cfopts)
    return cf


def plot_var_from_ncdf_file_timestep(varname, ts, file, mm, **cfopts):
    RUN = file
    if hasattr(RUN.variables[varname], "_FillValue"):
        var = np.ma.masked_equal(RUN.variables[varname].data.squeeze(), RUN.variables[varname]._FillValue)
    else:
        var = RUN.variables[varname].data.squeeze()
    var = var[ts, :, :]
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


def plot_array_on_ncdf_file_lon_lat_grid(var, file, mm, **cfopts):
    RUN = file
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
