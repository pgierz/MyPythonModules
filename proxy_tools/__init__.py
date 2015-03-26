#!/usr/bin/python
"""
    __init__.py
Lives: /Users/paulgierz/Code/MyPythonModules/proxy_tools/__init__.py

This file is part of the Paleoclimate Python Toolkits (name subject to
change in finalized versions), and comes with NO WARRARNTY. Similar
warnings are given in professional software, I'm just following
suit. Tools gathered in this file do:

downloading proxy data
plotting proxy data on a map
associating proxy data with corresponding model simiulations

Paul J. Gierz Wed Feb 18 09:14:17 2015
"""


class _proxy_plotting_settings(object):
    self.terrestrial_marker = 'square'
    self.cryosphere_marker = 'circle'
    self.sediment_marker = 'diamond'
    # TODO: add other markers as they become relevant


# Pseudofunctions that I can't look up proper tools for at the moment:
def download_from_url(url, dest=here):
    wget url dest  # Or something similar
    print "loaded " + proxyfile + " from " + URL.
    # TODO: something with bibinfo??
    return proxyfile, bibinfo_for_plotting


def plot_proxy_on_existing(proxyfile, lab, ax):
    # Depending on the dimensions of the proxy input, we either need to use 0 and 1 as x and y
    if proxyfile.ndims == 3:
        ax.scatter(proxyfile[0], proxyfile[1], c=proxyfile[2], label=lab)
    else:
        # ERROR
        print "Utter failure, sorry"
