import os
from scipy.io import netcdf


def make_region_fldmean(fin, lonmin, lonmax, latmin, latmax, output=False):
    os.system("cdo -f nc -fldmean -sellonlatbox,"
              + ",".join(str(n) for n in (lonmin, lonmax, latmin, latmax))
              + " "
              + " ".join((fin, fin.replace(".nc", "_"
                                           + str(lonmin) + str(lonmax)
                                           + "-"
                                           + str(latmin) + str(latmax)
                                           + ".nc")
                          ))
              )
    if output:
        return netcdf.netcdf_file(fin.replace(".nc", "_"
                                              + str(lonmin) + str(lonmax)
                                              + "-"
                                              + str(latmin) + str(latmax)
                                              + ".nc"))
    else:
        return None
