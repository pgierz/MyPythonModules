"""
A class to plot cross sections nicely

Paul J. Gierz, Tue Aug 11 17:59:09 2015
"""

from scipy.io import netcdf

class cross_section(object):
    """Documentation for cross_section

    """
    def __init__(self, ncdf_file):
        super(cross_section, self).__init__()
        self.ncdf_file = netcdf.netcdf_file(ncdf_file)
        
        
    
