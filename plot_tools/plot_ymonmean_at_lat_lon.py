import numpy as np
import matplotlib
import scipy.io.netcdf.netcdf_variable
from . import parse_units_to_latex

# This function could be easily abstracted to make a plot timeseries
# at any lon lat of 3D dataset function. A monthly cycle is just a
# special case of that.

def plot_ymonmean_at_lat_lon(dat, lats, lons, ax=matplotlib.pyplot.cga(), **kwargs):
    """This function plots and dataset of a ymonmean input file in 3
    dimensions (lat, lon, time) and plots a monthly cycle of that
    variable at a specified lat and lon.

    If multiple (lats, lons) are given, a mean is made over those lats
    and lons.

    Paul J. Gierz, Tue Aug 11 20:58:15 2015

    Keyword Arguments:
    dat  -- the data to plot. Should be a netcdf.netcdf_variable instance!
    lats -- the lat or lats to look at
    lons -- the lon or lons to look at
    ax   -- (default matplotlib.pyplot.cga())
    **kwargs -- matplotlib.pyplot.plot keywords

    returns the plt.plot instance.
    """
    # This is wrong. We NEED to have dat in 3 dimensions. I need to
    # instead test if lats, lons are only len 1 or many
    
    assert type(dat) is scipy.io.netcdf.netcdf_variable
    assert dat.data.shape[dat.data.dimensions.index("time")] == 12
    plot_dat = dat.data.squeeze()
    time = np.arange(12)
    p = ax.plot(time, dat, **kwargs)
    if np.ndim(dat) == 3:
        llon, llat = np.meshgrid(lons, lats)
        use_lons, use_lats = np.where(llon == lons), np.where(llat == lats)
        dat = dat[:, use_lons, use_lats].mean(axis=(1, 2))
        p = ax.plot(time, dat, **kwargs)

    # Some decoration stuff
    ax.set_xlabel("Month")
    ax.xaxis.set_ticks(time)
    ax.xaxis.set_xticklabels(["J", "F", "M", "A", "M", "J", "J", "A", "S", "O", "N", "D"])
    ax.set_ylabel(dat.long_name+" ("+dat.units+")")
    return p
