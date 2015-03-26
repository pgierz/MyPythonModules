#!/usr/bin/python
"""amoc.py
Lives: /Users/paulgierz/Repos/MyPythonModules/post_database/amoc.py

Makes an amoc timeseries based upon cdo routines for a run, and
registers the resulting file in a hdf5 database

Paul J. Gierz Thu Feb 12 14:15:25 2015

"""
import h5py

# Alright, I need to actually legitimately think about this. To start,
# we want to make an AMOC timeseries (as a proof of concept), that can
# be done in a function:


class post_amoc(object):
    """Documentation for post_amoc

    """
    def __init__(self, expid):
        super(post_amoc, self).__init__()
        self.expid = expid
    
    def make_amoc_timeseries(self, expid):
        """ Makes a yearmean timeseries of AMOC based upon a stnadardized index. Uses CDO routines.
        Keyword Arguments:
        expid -- the expirement name
        """
        # TODO: Some cdo based code...
        pass

    # Next, we wish to register the file we just made into a database

    def register_post_to_db(self, dataset):
        """
        Keyword Arguments:
        dataset -- the dataset to register
        """
        # I guess the best way is to just try it out...
        db = h5py.File(self.expid+"_post_db.hdf5", "a")

