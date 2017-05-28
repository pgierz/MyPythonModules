#!/usr/bin/env python
from plot_tools import plot_var_from_ncdf_file
from basemap_wrappers import map_global
import matplotlib.pyplot as plt
from scipy.io import netcdf


def main():
    f = netcdf.netcdf_file("/csys/nobackup1_PALEO/pgierz/cosmos-aso/Eem120-B/post/echam5/Eem120-B_echam5_tsurf_timmean.nc")
    fig, axs = plt.subplots(1, 1)
    m = map_global(thisax=axs, fill_color=None)
    plot_var_from_ncdf_file("tsurf", f, m)
    plt.show()


if __name__ == '__main__':
    main()
