#!/usr/bin/python
"""
    density_thermal_haline.py
Lives: /Users/pgierz/Code/MyPythonModules/analysis/density_thermal_haline.py

seperates thermal and haline components of density

Paul J. Gierz Fri May 29 14:46:19 2015
"""

from seawater_state import state

def RHO_thermal_component(TEMP, SALT, SHF, SFWF):
    alpha, beta, rho = state(TEMP, SALT, 0)
    print "alpha: %s, beta: %s, rho: %s" % (alpha, beta, rho)
    alpha0, beta0, rho0 = state(TEMP, 0, 0)
    print "alpha0: %s, beta0: %s, rho0: %s" % (alpha0, beta0, rho0)
    cp_sw = 3.996e3    # specific heat of salt water
    RHO_THERMAL = -1 * alpha * SHF / cp_sw
    return RHO_THERMAL

def RHO_haline_component(TEMP, SALT, SHF, SFWF):
    alpha, beta, rho = state(TEMP, SALT, 0)
    print "alpha: %s, beta: %s, rho: %s" % (alpha, beta, rho)
    alpha0, beta0, rho0 = state(TEMP, 0, 0)
    print "alpha0: %s, beta0: %s, rho0: %s" % (alpha0, beta0, rho0)
    # cp_sw = 3.996e3    # specific heat of salt water
    RHO_HALINE = beta * (rho0 * 1e3) * (-SFWF * 1e3) * (SALT / 1e3) / (1 - SALT/1e3)
    return RHO_HALINE

