import numpy as np
from scipy.fftpack import fft

def frequency(timeseries):
    """

    Makes a frequency analysis of the timeseries

    returns frequencies and power
    Arguments:
    - `timeseries`: An array containing a timeseries
    """
    yt = timeseries
    yf = fft(timeseries)
    n = yt.size
    timestep = 1.0 / n
    xt = np.linspace(0.0, timestep, n)
    xf = np.linspace(0,0, 1.0/(2.0 * timestep), n/2)
    return xf, yf
