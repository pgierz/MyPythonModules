"""
    significance_test.py
Lives: /Users/paulgierz/Repos/MyPythonModules/analysis/significance_test.py

A reimpliemtation of the significance test introduced by M. Pfeiffer

Paul J. Gierz Wed Feb 11 11:28:39 2015

# TODO: MODULE DOCUMENTATION!!!

"""
######################################################################
# Module Things, probably best if private and not imported
######################################################################

# Notes:
# I can probably redo this whole this as a class! Is that smart? Probably
from mpl_toolkits.basemap import shiftgrid, addcyclic
import numpy as np
from scipy.io import netcdf
import scipy.stats
import sys
import time


def _load_data(path):
    # TODO: This is living in a different module now, it should be loaded from
    # custom_io
    """Loads any *netcdf* file into the workspace. Can also load remote
    files using sftp.

    Keyword Arguments:
    path -- path to the file you wish to load

    Paul J. Gierz, Thu Jan 15 13:52:08 2015

    """
    from custom_io.get_remote_data import get_remote_data
    if type(path) is netcdf.netcdf_file:
        return path
    elif type(path) is str:
        if "@" in path:
            # POTENTIAL BUG: This could be a bad logical condition, if
            # people are silly enough to put @ in their filenames it
            # could cause problems. However, I'm going to assume
            # people aren't that silly, plus many people won't want to
            # load data remotely necessarily
            return get_remote_data(path)
        else:
            return netcdf.netcdf_file(path)
    else:
        # Fail horribly
        sys.exit("Please give a string!!")


def _data_prep_for_plotting(variablename, ncdf_file):
    if type(ncdf_file) is not netcdf.netcdf_file:
        if type(ncdf_file) is str:
            ncdf_file = _load_data(ncdf_file)
        else:
            sys.exit(
                "You've broken the data_prep_for_plotting function, please pay 3, \
                tokens to continue")
    if type(variablename) is np.ndarray:
        dat = variablename
    else:
        # This is a contains statement in python. It's fucking weird, but
        # whatever
        if not [variablename, 'lon', 'lat'] <= ncdf_file.variables.keys():
            sys.exit(
                "The variable you've requested doesn't exist, or lon/lat are incorrectly named in your netcdf file. Please pay 2 tokens to continue")
        else:
            dat = ncdf_file.variables[variablename].data.squeeze()
    # Mask dat1
    dat = np.ma.masked_equal(dat, -9e+33)
    lon = ncdf_file.variables['lon'].data.squeeze()
    lat = ncdf_file.variables['lat'].data.squeeze()
    dat, lon = shiftgrid(180., dat, lon, start=False)
    dat, lon = addcyclic(dat, lon)
    lons, lats = np.meshgrid(lon, lat)
    return lons, lats, dat

######################################################################
# NON-PRIVATE THINGS
######################################################################


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


class significance_test(object):

    """Documentation for significance_test

    """

    def __init__(self, file1, file2, variable1, variable2):
        super(significance_test, self).__init__()
        time_start = time.time()
        self.f1 = _load_data(file1)
        print "Loaded %(file)s in %(time)s seconds" % {'file': file1, 'time': time.time() - time_start}
        time_start = time.time()
        self.f2 = _load_data(file2)
        print "Loaded %(file)s in %(time)s seconds" % {'file': file2, 'time': time.time() - time_start}
        self._lons, self._lats, self.variable1 = _data_prep_for_plotting(
            variable1, file1)
        self._lons, self._lats, self.variable2 = _data_prep_for_plotting(
            variable2, file2)
        self.anom = self.variable1.mean(axis=0) - self.variable2.mean(axis=0)
        dimnames = self.f1.variables[variable1].dimensions
        dimshape = self.f1.variables[variable1].data.shape
        dims = {}
        for i, j in zip(dimnames, dimshape):
            dims[i] = j
        self.sig_mask = np.zeros((dims['lat'], dims['lon']))
        for i in range(dims['lon']):
            for j in range(dims['lat']):
                xx = self.variable1[:, j, i]
                yy = self.variable2[:, j, i]
                autocorrx = max(estimated_autocorrelation(xx)[1], 0)
                autocorry = max(estimated_autocorrelation(yy)[1], 0)
                eff_dof1 = dims['time'] * (1 - autocorrx) / (1 + autocorrx)
                eff_dof2 = dims['time'] * (1 - autocorry) / (1 + autocorry)
                eff_dof_comb = min(eff_dof1, eff_dof2)
                cutoff = scipy.stats.t.ppf(0.975, eff_dof_comb)
                t_test = abs(
                    xx.mean() - yy.mean()) / ((xx.var() / dims['time'] + yy.var() / dims['time']) ** 0.5)
                if t_test < cutoff:
                    self.sig_mask[j, i] = 1
                else:
                    self.sig_mask[j, i] = 0  # float("NaN")
        self.sig_mask = _data_prep_for_plotting(self.sig_mask, file1)[2]

    def plot_anomaly(self, m, plot_hatches=True, **kwargs):
        # M needs to be a basemap instance
        cb = m.contourf(
            self._lons, self._lats, self.anom, latlon=True, **kwargs)
        m.colorbar(cb)
        if plot_hatches:
            mask = np.ma.masked_not_equal(self.sig_mask, 1)
            m.contourf(self._lons, self._lats, mask, 1,
                       colors='white', hatches=['////'], latlon=True)

    def save_sig_mask_as_nc(self, ofile):
        # Save outdata for netcdf!
        outfile = netcdf.netcdf_file(ofile, 'w')
        outfile.createVariable('mask', None, ('lat', 'lon'))
        outfile.variables['mask'].data[:] = self.sig_mask
        outfile.close()
