def frequency(timeseries):
    """

    Makes a frequency analysis of the timeseries

    returns frequencies and power
    Arguments:
    - `timeseries`: An array containing a timeseries
    """
    data = timeseries
    data_fft = np.fft.fft(data)
    n = data.size
    timestep = 1
    data_freqs = np.fft.fftfreq(n, d=timestep)
    P_data = data_fft * conj(data_fft) / n
    indexes = np.argsort(P_data)[::-1]
    sorted_values = np.sort_complex(P_data)[::-1]
    return data_freqs, P_data

def plot_frequencies(timeseries):
    data_freqs, P_data = frequency(timeseries)
    plt.subplot(211)
    plt.plot(data)
    ax = plt.subplot(212)
    ax.plot(data_freqs, P_data)
    ax.set_xscale('log')
    ax.set_yscale('log')
    
