"""
Some useful plot tools that are needed frequently

Paul J. Gierz, Wed Jul 15 15:46:00 2015
"""
import numpy as np
import matplotlib.pyplot
import scipy.io.netcdf
from mpl_toolkits.basemap import shiftgrid, addcyclic
import os
import scipy.stats
import cdo
from proxy_tools import Kim_ONeill_after_MW, convert_SMOW_to_PDB

CDO = cdo.Cdo()


def _decorate_x_axes_for_ymonmean(ax):
    # Some decoration stuff
    ax.set_xlabel("Month")
    ax.set_xlim(-1, 12)
    ax.xaxis.set_ticks(np.arange(12))
    ax.xaxis.set_ticklabels(
        ["J", "F", "M", "A", "M", "J", "J", "A", "S", "O", "N", "D"])
    return ax


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
    unit_string = unit_string.split(
        "**")[0] + "$^{" + unit_string.split("**")[1] + "}$"

    ###################################################################
    # NOTE:
    ###################################################################
    # This isn't done yet. It needs to do something like astropy does,
    # but netcdf apparently isn't that sexy from what I can
    # tell. Since I don't do this often, I can convert the final unit
    # to nice latex by hand right before publication, but it'd be nice
    # if it happened automatically.
    ###################################################################


def _find_nearest_idx(array, value):
    idx = (np.abs(array - value)).argmin()
    return idx


def plot_var_from_ncdf_file(varname, file, mm, factor=1, **cfopts):
    RUN = file
    if hasattr(RUN.variables[varname], "_FillValue"):
        var = np.ma.masked_equal(
            RUN.variables[varname].data.squeeze(), RUN.variables[varname]._FillValue)
    else:
        var = RUN.variables[varname].data.squeeze()
    lon = RUN.variables['lon'].data.squeeze()
    lat = RUN.variables['lat'].data.squeeze()
    var, lon = shiftgrid(180., var, lon, start=False)
    var, lon = addcyclic(var, lon)
    mm.drawmapboundary(fill_color='gray')
    lons, lats = np.meshgrid(lon, lat)
    var = var * factor
    cf = mm.contourf(lons, lats, var, latlon=True,
                     extend='both',
                     **cfopts)
    return cf


def pcolormesh_var_from_ncdf_file(varname, file, mm, **cfopts):
    RUN = file
    if hasattr(RUN.variables[varname], "_FillValue"):
        var = np.ma.masked_equal(
            RUN.variables[varname].data.squeeze(), RUN.variables[varname]._FillValue)
    else:
        var = RUN.variables[varname].data.squeeze()
    lon = RUN.variables['lon'].data.squeeze()
    lat = RUN.variables['lat'].data.squeeze()
    var, lon = shiftgrid(180., var, lon, start=False)
    var, lon = addcyclic(var, lon)
    mm.drawmapboundary(fill_color='gray')
    lons, lats = np.meshgrid(lon, lat)
    cf = mm.pcolormesh(lons, lats, var, latlon=True,
                       edgecolor="gray", linestyle=":",
                       lw=0.15,
                       **cfopts)
    return cf


def pcolormesh_var_from_ncdf_file_nogrid(varname, file, mm, **cfopts):
    RUN = file
    if hasattr(RUN.variables[varname], "_FillValue"):
        var = np.ma.masked_equal(
            RUN.variables[varname].data.squeeze(), RUN.variables[varname]._FillValue)
    else:
        var = RUN.variables[varname].data.squeeze()
    lon = RUN.variables['lon'].data.squeeze()
    lat = RUN.variables['lat'].data.squeeze()
    var, lon = shiftgrid(180., var, lon, start=False)
    var, lon = addcyclic(var, lon)
    mm.drawmapboundary(fill_color='gray')
    lons, lats = np.meshgrid(lon, lat)
    cf = mm.pcolormesh(lons, lats, var, latlon=True,
                       edgecolor="gray", linestyle=":",
                       lw=0,
                       **cfopts)
    return cf


def plot_var_mean_from_ncdf_file(varname, file, mm, **cfopts):
    RUN = file
    if hasattr(RUN.variables[varname], "_FillValue"):
        var = np.ma.masked_equal(
            RUN.variables[varname].data.squeeze(), RUN.variables[varname]._FillValue)
    else:
        var = RUN.variables[varname].data.squeeze()
    lon = RUN.variables['lon'].data.squeeze()
    lat = RUN.variables['lat'].data.squeeze()
    var, lon = shiftgrid(180., var, lon, start=False)
    var, lon = addcyclic(var, lon)
    mm.drawmapboundary(fill_color='gray')
    lons, lats = np.meshgrid(lon, lat)
    var = var.mean(axis=0)
    cf = mm.contourf(lons, lats, var, latlon=True,
                     extend='both',
                     **cfopts)
    return cf


def plot_var_anom_from_ncdf_file(varname, file, cfile, mm, factor=1, ovarname=None, **cfopts):
    if ovarname is None:
        ovarname = varname
    RUN = file
    CTL = cfile
    if hasattr(RUN.variables[varname], "_FillValue"):
        var = np.ma.masked_equal(
            RUN.variables[varname].data.squeeze(), RUN.variables[varname]._FillValue)
    else:
        var = RUN.variables[varname].data.squeeze()
    if hasattr(CTL.variables[ovarname], "_FillValue"):
        ctl = np.ma.masked_equal(
            CTL.variables[ovarname].data.squeeze(), CTL.variables[ovarname]._FillValue)
    else:
        ctl = CTL.variables[ovarname].data.squeeze()
    lon = RUN.variables['lon'].data.squeeze()
    lat = RUN.variables['lat'].data.squeeze()
    var = var * factor
    ctl = ctl * factor
    var = var - ctl
    print var.shape
    var, lon = shiftgrid(180., var, lon, start=False)
    var, lon = addcyclic(var, lon)
    mm.drawmapboundary(fill_color='gray')
    lons, lats = np.meshgrid(lon, lat)
    cf = mm.contourf(lons, lats, var, latlon=True,
                     extend='both',
                     **cfopts)
    return cf




def plot_var_1D_timeseries_from_ncdf_file(varname, RUN, ax, plotlev=None, runmean_interval=None, **pltopts):
    if runmean_interval is not None:
        var = CDO.runmean(str(runmean_interval), input=RUN.filename, returnCdf=True).variables[varname][:].squeeze()
    else:
        if hasattr(RUN.variables[varname], "_FillValue"):
            var = np.ma.masked_equal(
                RUN.variables[varname].data.squeeze(), RUN.variables[varname]._FillValue)
        else:
            var = RUN.variables[varname].data.squeeze()
    if plotlev is not None:
        var = var[:, plotlev].squeeze()
    if runmean_interval is not None:
        lp = ax.plot(np.arange(len(var)) + runmean_interval/2.0, var, **pltopts) 
    else:
        lp = ax.plot(var, **pltopts)  # lp for "line plot"
    return


def plot_var_from_ncdf_file_timestep(varname, ts, file, mm, ovarname=None, **cfopts):
    if ovarname is None:
        ovarname=varname
    RUN = file
    if hasattr(RUN.variables[varname], "_FillValue"):
        var = np.ma.masked_equal(
            RUN.variables[varname].data.squeeze(), RUN.variables[varname]._FillValue)
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


def plot_var_anom_from_ncdf_file_timestep(varname, ts, file, cfile, mm, ovarname=None, **cfopts):
    if ovarname is None:
        ovarname = varname
    RUN = file
    CTL = cfile
    if hasattr(RUN.variables[varname], "_FillValue"):
        var = np.ma.masked_equal(
            RUN.variables[varname].data.squeeze(), RUN.variables[varname]._FillValue)
    else:
        var = RUN.variables[varname].data.squeeze()

    if hasattr(CTL.variables[ovarname], "_FillValue"):
        ctl = np.ma.masked_equal(
            CTL.variables[ovarname].data.squeeze(), CTL.variables[ovarname]._FillValue)
    else:
        ctl = CTL.variables[ovarname].data.squeeze()
    var = var.squeeze()
    ctl = ctl.squeeze()
    print "Beginning of selection:"
    print "Var has shape:"
    print var.shape
    print "Ctl has shape:"
    print ctl.shape
    print "Selecting based upon:" 
    print type(ts)
    if (type(ts) is int) or (type(ts) is float):
        print "selecting timestep!"
        var = var[ts, :, :]
        if len(ctl.shape) != 2:
            ctl = ctl[ts, :, :]
    elif type(ts) is list:
        print "making mean!"
        var = var[ts, :, :].mean(axis=0)
        # print var
        ctl = ctl[ts, :, :].mean(axis=0)
        # print ctl
    else:
        print "Logic error! Check your inputs"
    print var.shape
    print ctl.shape
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


def add_subplot_axes(ax, rect, axisbg='w', fig=None, transform=True):
    """ 
    What does this function do?

    From what I can tell, it adds an inset axes.

    Paul J. Gierz, Tue Mar  1 10:57:37 2016
    """
    if fig is None:
        fig = matplotlib.pyplot.gcf()
    box = ax.get_position()
    width = box.width
    height = box.height
    inax_position = ax.transAxes.transform(rect[0:2])
    # inax_position = rect[0:2]
    transFigure = fig.transFigure.inverted()
    infig_position = transFigure.transform(inax_position)
    x = infig_position[0]
    y = infig_position[1]
    width *= rect[2]
    height *= rect[3]  # <= Typo was here
    if transform:
        subax = fig.add_axes(
            [x, y, width, height], axisbg=axisbg, transform=ax.transAxes)
    else:
        subax = fig.add_axes(
            [x, y, width, height], axisbg=axisbg)
    # x_labelsize = subax.get_xticklabels()[0].get_size()
    # y_labelsize = subax.get_yticklabels()[0].get_size()
    # x_labelsize *= rect[2] ** 0.5
    # y_labelsize *= rect[3] ** 0.5
    # subax.xaxis.set_tick_params(labelsize=x_labelsize)
    # subax.yaxis.set_tick_params(labelsize=y_labelsize)
    return subax

##########################################################################
##########################################################################
##########################################################################
# Stuff for the anomaly hatching:


def estimated_autocorrelation(x):
    """
    Since I don't like black boxes, I use my own autocorrelation so
    we know what is happening with the stats. Sources are given below:

    http://stackoverflow.com/q/14297012/190597
    http://en.wikipedia.org/wiki/Autocorrelation#Estimation

    Paul J. Gierz, Thu Jan 15 14:36:32 2015
    """
    n = len(x)
    variance = x.var()
    x = x - x.mean()
    r = np.correlate(x, x, mode='full')[-n:]
    result = r / (variance * (np.arange(n, 0, -1)))
    return result

##########################################################################


def compute_significance(file1, cfile, var, mask_cutoff, verbose=False):
    x = file1.variables[var].data.squeeze()
    y = cfile.variables[var].data.squeeze()
    dimnames = file1.variables[var].dimensions
    dimshape = file1.variables[var].data.shape
    dims = {}
    for i, j in zip(dimnames, dimshape):
        dims[i] = j
    sig_mask = np.zeros((dims['lat'], dims['lon']))
    for i in range(dims['lon']):
        for j in range(dims['lat']):
            xx = x[:, j, i]
            yy = y[:, j, i]
            autocorrx = max(estimated_autocorrelation(xx)[1], 0)
            autocorry = max(estimated_autocorrelation(yy)[1], 0)
            eff_dof1 = dims['time'] * (1 - autocorrx) / (1 + autocorrx)
            eff_dof2 = dims['time'] * (1 - autocorry) / (1 + autocorry)
            eff_dof_comb = min(eff_dof1, eff_dof2)
            cutoff = scipy.stats.t.ppf(mask_cutoff, eff_dof_comb)
            t_test = abs(
                xx.mean() - yy.mean()) / ((xx.var() / dims['time'] + yy.var() / dims['time']) ** 0.5)
            if t_test < cutoff:
                sig_mask[j, i] = 1
                # print "a nonsignificant change was masked!"
            else:
                sig_mask[j, i] = 0  # float("NaN")
            if verbose:
                print i, j
                print "#########################################################################"
                print cutoff, t_test
                print t_test < cutoff
    return sig_mask


def plot_var_anom_hatching_from_ncdf_file(varname, RUN, CTL, mm, mask_cutoff=0.975, verbosity=False, **cfopts):
    sig_mask = compute_significance(RUN, CTL, varname, mask_cutoff, verbose=verbosity)
    if hasattr(RUN.variables[varname], "_FillValue"):
        var = np.ma.masked_equal(
            RUN.variables[varname].data.squeeze(), RUN.variables[varname]._FillValue)
        ctl = np.ma.masked_equal(
            CTL.variables[varname].data.squeeze(), CTL.variables[varname]._FillValue)
    else:
        var = RUN.variables[varname].data.squeeze()
        ctl = CTL.variables[varname].data.squeeze()
    var = var - ctl
    lon = RUN.variables['lon'].data.squeeze()
    lon2 = lon
    lat = RUN.variables['lat'].data.squeeze()
    var, lon = shiftgrid(180., var, lon, start=False)
    var, lon = addcyclic(var, lon)
    mm.drawmapboundary(fill_color='gray')
    lons, lats = np.meshgrid(lon, lat)
    # print sig_mask
    var = var.mean(axis=0)
    cf = mm.contourf(lons, lats, var, latlon=True,
                     extend='both',
                     **cfopts)
    mask = np.ma.masked_not_equal(sig_mask, 1)
    # mask = sig_mask
    mask, lon2 = shiftgrid(180., mask, lon2, start=False)
    mask, lon2 = addcyclic(mask, lon2)
    mm.contourf(
        lons, lats, mask, 1, colors="none",  hatches=["\\\\\\\\"], latlon=True)
    mm.contourf(
        lons, lats, mask, 1, colors="none", hatches=["////////"], latlon=True)
    return cf


def plot_insolation(ax, run, ctl, cb=False, **kwargs):
    time = (1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24)
    var = "srad0d"
    inso = np.append(run.variables[var].data.squeeze(), run.variables[var].data.squeeze(), axis=0) - np.append(ctl.variables[var].data.squeeze(), ctl.variables[var].data.squeeze(), axis=0)
    lat = run.variables['lat'].data.squeeze()
    cf = ax.contourf(time, lat, inso.transpose(), **kwargs)
    ax.xaxis.set_ticks((1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13))
    ax.xaxis.set_ticklabels(("J", "F", "M", "A", "M", "J", "J", "A", "S", "O", "N", "D", "J"))
    ax.set_xlim(1, 13)
    ax.yaxis.set_ticks((-85, -45, 0, 45, 85))
    ax.yaxis.set_ticklabels((-90, -45, 0, 45, 90))
    return cf


def plot_d18O_calcite_from_ncfiles_anom(file_temp, file_d18Op, cfile_temp, cfile_d18Op, mm,
                                        temp_name="temp2", ctemp_name="temp2", d18Op_name="wisoaprt_d", cd18Op_name="wisoaprt_d",
                                        use_Celsius=False,
                                        **cfopts):
    T = file_temp.variables[temp_name].data.squeeze()
    W = file_d18Op.variables[d18Op_name].data.squeeze()
    if use_Celsius:
        C = convert_SMOW_to_PDB(Kim_ONeill_after_MW(T+273.15, W))
    else:
        C = convert_SMOW_to_PDB(Kim_ONeill_after_MW(T, W))
    CT = cfile_temp.variables[ctemp_name].data.squeeze()
    CW = cfile_d18Op.variables[cd18Op_name].data.squeeze()
    if use_Celsius:
        CC = convert_SMOW_to_PDB(Kim_ONeill_after_MW(CT+273.15, CW))
    else:
        CC = convert_SMOW_to_PDB(Kim_ONeill_after_MW(CT, CW))
    lon = file_temp.variables['lon'].data.squeeze()
    lat = file_temp.variables['lat'].data.squeeze()
    var = C - CC

    var, lon = shiftgrid(180., var, lon, start=False)
    var, lon = addcyclic(var, lon)
    mm.drawmapboundary(fill_color='gray')
    lons, lats = np.meshgrid(lon, lat)
    cf = mm.contourf(lons, lats, var, latlon=True,
                     extend='both',
                     **cfopts)
    return cf

