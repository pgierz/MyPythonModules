"""
Some useful plot tools that are needed frequently

Paul J. Gierz, Wed Jul 15 15:46:00 2015
"""
import numpy as np


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
        # TODO: else: raise error
    elif type(tolerance) in [float, int, np.float64]:
        dat = np.ma.masked_inside(dat, tolerance * -1, tolerance)
    if type(tolerance) is str:
        if tolerance is "auto":
            percent = 0.01
        else:
            percent = float(tolerance)
        dat = np.ma.masked_inside(
            dat, percent * (dat.max() - dat.min()), -1 * percent * (dat.max() - dat.min()))
    else:
        print "Something went wrong, nothing masked!"
        print type(tolerance)
    if verbose:
        print "PG: Masked out ", sum(sum(dat.mask)), "values that are inside of ", tolerance
        # PG: I don't know why this needs to be a double sum, for
        # some reason sum(dat.mask) produces a list
    return dat, dat.mask
