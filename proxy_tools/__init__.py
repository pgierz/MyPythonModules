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
converting 18O in seawater to 18O in calcite.

Paul J. Gierz Wed Feb 18 09:14:17 2015
"""
import math
import numpy as np

# class _proxy_plotting_settings(object):
#     self.terrestrial_marker = 'square'
#     self.cryosphere_marker = 'circle'
#     self.sediment_marker = 'diamond'
# TODO: add other markers as they become relevant


# Pseudofunctions that I can't look up proper tools for at the moment:
# def download_from_url(url, dest=here):
#     wget url dest  # Or something similar
#     print "loaded " + proxyfile + " from " + URL.
#     # TODO: something with bibinfo??
#     return proxyfile, bibinfo_for_plotting


def plot_proxy_on_existing(proxyfile, lab, ax):
    # Depending on the dimensions of the proxy input, we either need to use 0
    # and 1 as x and y
    if proxyfile.ndims == 3:
        ax.scatter(proxyfile[0], proxyfile[1], c=proxyfile[2], label=lab)
    else:
        # ERROR
        print "Utter failure, sorry"


def convert_18Osw_to_18Oc(d18Osw, T):
    print d18Osw
    print T
    d18Oc = (T + d18Osw - 16.9) / -4.0
    return d18Oc


def Epstein_1953_d18Oc(T, W):
    # T=16.5-4.3*((1.01025*(1000+C)-1000)-(1.0412*(1000+(0.97002*W-29.98))-1000))+0.14*((1.01025*(1000+C)-1000)-(1.0412*(1000+(0.97002*W-29.98))-1000))^2
    # T - 16.5 = 4.3
    C1 = (-312500000.0 * (56 * T + 925)**0.5 +
          883736721.0 * W + 13205471000.0) / 883968750.0
    C2 = C1 * -1.0
    return C1, C2


def Craig_1965_d18Oc(T, W):
    # T=16.9-4.2*((1.01025*(1000+C)-1000)-(1.0412*(1000+(0.97002*W-29.98))-1000))+0.13*((1.01025*(1000+C)-1000)-(1.0412*(1000+(0.97002*W-29.98))-1000))^2
    C1 = (-125000000.0 * (10.0**0.5) * (130.0 * T + 2213.0) +
          1641225339.0 * W + 25819089000.0) / 1641656250.0
    C2 = C1 * -1.0
    return C1, C2


def Anderson_Arthur_1983_d18Oc(T, W):
    # T=16-4.14*(C-W)+0.13*(C+-W)^2
    C1 = (1.0 / 13.0) * (207.0 - (1300.0 * T + 22049.0)**0.5) + W
    C2 = (1.0 / 13.0) * ((1300.0 * T + 22049.0)**0.5 + 13.0 * W + 207.0)
    return C1, C2


def Friedman_ONeil_1977_d18Oc(T, W):
    # T=((1000000*2.78)/(1000*LN((1000+C)/(1000+W))+2.89))^0.5-273.15
    C_SMOW = W * math.e**((-0.00289 * (T - 707.634) * (T + 1253.93)) / (T + 273.15)**2) + \
        1000 * math.e**((-0.00289 * (T - 707.634) *
                         (T + 1253.93)) / (T + 273.15)**2) - 1000
    # Convert to C_SMOW
    return (C_SMOW - 30.86) / 1.03086


def Kim_ONeill_Corrected_1997_d18Oc(T, W):
    # print T.shape, W.shape
    C = np.exp((2000000.0 * T * np.log(W + 1000.0) - 64340.0 * T + 546300000.0 *
                np.log(W + 1000.0) + 18485529.0) / (100000.0 * (20.0 * T + 5463.0))) - 1000.0
    return (C - 30.91) / 1.03091


def Kim_ONeill_after_MW(T, W):
    C = W + 18.03 * (1000 / T) - 32.42 + 0.27
    return C


def convert_SMOW_to_PDB(d18O_S):
    return 0.97002 * d18O_S - 29.98

# def Shackelton_after_MW(T, W):
    
