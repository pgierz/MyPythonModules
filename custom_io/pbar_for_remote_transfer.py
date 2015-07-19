"""
This file contains a few functions that make a nice progressbar
when copying remote data to a local filesystem


Paul J. Gierz, Sat Jun 27 11:55:25 2015
"""

import progressbar

# The callback function from paramiko gives me something like:
currentvalue=0
maxvalue=100

pbar = Progressbar().start()

