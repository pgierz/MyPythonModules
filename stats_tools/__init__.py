import numpy as np
import scipy.stats
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


def compute_significance(file1, file2, var1, var2):
    x = file1.variables[var1].data.squeeze()
    y = file2.variables[var2].data.squeeze()
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
            cutoff = scipy.stats.t.ppf(0.975, eff_dof_comb)
            t_test = abs(xx.mean() - yy.mean()) / \
                ((xx.var() / dims['time'] + yy.var() / dims['time']) ** 0.5)
            if t_test < cutoff:
                sig_mask[j, i] = 1
            else:
                sig_mask[j, i] = 0  # float("NaN")
    return sig_mask
