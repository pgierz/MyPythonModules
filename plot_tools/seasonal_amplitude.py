import numpy
import matplotlib.pyplot
import scipy.io.netcdf
from . import _find_nearest_idx
from mpl_toolkits.basemap import shiftgrid, addcyclic


def _decorate_x_axes_for_ymonmean(ax):
    # Some decoration stuff
    ax.set_xlabel("Month")
    ax.set_xlim(-1, 12)
    ax.xaxis.set_ticks(numpy.arange(12))
    ax.xaxis.set_ticklabels(
        ["J", "F", "M", "A", "M", "J", "J", "A", "S", "O", "N", "D"])
    return ax


def determine_seasonal_amplitude(arr, ax=0):
    return arr.max(axis=ax) - arr.min(axis=ax)


def plot_seasonal_amplitude_from_ncdf_file(varname, filename, mm, **kwargs):
    """Plots the seasonal amplitude of varname from filename onto a map instance given by mm
    Keyword Arguments:
    varname  -- (str) the variable name to use
    filename -- (scipy.io.netcdf.netcdf_file) the file to use
    mm       -- the map instance to use
    **kwargs -- extra keyword arguments to the contourf instance

    Paul J. Gierz, Thu Jan  7 15:30:20 2016
    """
    time_index = filename.variables[varname].dimensions.index("time")
    assert type(filename) is scipy.io.netcdf.netcdf_file
    assert filename.variables[varname].data.shape[time_index] == 12
    RUN = filename
    if hasattr(RUN.variables[varname], "_FillValue"):
        var = numpy.ma.masked_equal(determine_seasonal_amplitude(RUN.variables[varname].data.squeeze(),
                                                                 time_index),
                                    RUN.variables[varname]._FillValue)
    else:
        var = determine_seasonal_amplitude(RUN.variables[varname].data.squeeze(),
                                           time_index)
    lon = RUN.variables['lon'].data.squeeze()
    lat = RUN.variables['lat'].data.squeeze()
    var, lon = shiftgrid(180., var, lon, start=False)
    var, lon = addcyclic(var, lon)
    mm.drawmapboundary(fill_color='gray')
    lons, lats = numpy.meshgrid(lon, lat)
    cf = mm.contourf(lons, lats, var, latlon=True,
                     extend='both',
                     **kwargs)
    return cf


def plot_seasonal_amplitude_anom_from_ncdf_file(varname, filename, controlfile, mm, **kwargs):
    """Plots the seasonal amplitude of varname from filename onto a map instance given by mm
    Keyword Arguments:
    varname  -- (str) the variable name to use
    filename -- (scipy.io.netcdf.netcdf_file) the file to use
    mm       -- the map instance to use
    **kwargs -- extra keyword arguments to the contourf instance

    Paul J. Gierz, Thu Jan  7 17:40:36 2016
    """
    time_index = filename.variables[varname].dimensions.index("time")
    assert type(filename) is scipy.io.netcdf.netcdf_file
    assert filename.variables[varname].data.shape[time_index] == 12
    RUN = filename
    CTL = controlfile
    if hasattr(RUN.variables[varname], "_FillValue"):
        run = numpy.ma.masked_equal(determine_seasonal_amplitude(RUN.variables[varname].data.squeeze(),
                                                                 time_index),
                                    RUN.variables[varname]._FillValue)
        ctl = numpy.ma.masked_equal(determine_seasonal_amplitude(CTL.variables[varname].data.squeeze(),
                                                                 time_index),
                                    CTL.variables[varname]._FillValue)
    else:
        run = determine_seasonal_amplitude(RUN.variables[varname].data.squeeze(),
                                           time_index)
        ctl = determine_seasonal_amplitude(CTL.variables[varname].data.squeeze(),
                                           time_index)
    var = run - ctl
    lon = RUN.variables['lon'].data.squeeze()
    lat = RUN.variables['lat'].data.squeeze()
    var, lon = shiftgrid(180., var, lon, start=False)
    var, lon = addcyclic(var, lon)
    mm.drawmapboundary(fill_color='gray')
    lons, lats = numpy.meshgrid(lon, lat)
    cf = mm.contourf(lons, lats, var, latlon=True,
                     extend='both',
                     **kwargs)
    return cf


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
    assert dat.variables[var].data.shape[
        dat.variables[var].dimensions.index("time")] == 12
    plot_dat = dat.variables[var].data.squeeze()
    lon_list = dat.variables['lon'].data.squeeze()
    lat_list = dat.variables['lat'].data.squeeze()
    time = numpy.arange(12)
    llon, llat = numpy.meshgrid(lons, lats)
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
    ax.set_ylabel(
        dat.variables[var].long_name + " (" + dat.variables[var].units + ")")
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
    assert dat.variables[var].data.shape[
        dat.variables[var].dimensions.index("time")] == 12
    plot_dat = dat.variables[var].data.squeeze()
    time = numpy.arange(12)
    p = ax.plot(time, plot_dat, **kwargs)
    # Some decoration stuff
    ax = _decorate_x_axes_for_ymonmean(ax)
    ax.set_ylabel(
        dat.variables[var].long_name + " (" + dat.variables[var].units + ")")
    return p

