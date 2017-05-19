"""
Some helper functions for plotting transient stuff.

Paul Gierz, 2016
"""
import numpy as np


def decorate_time_axis_yearmeans(ax, suppress_ticks=False):
    """This function helps to get the time axis of a timeseries for the
    transient run looking pretty. You have the option to suppress the
    ticks with a boolean, useful if for example you are making a
    multi-variable (stacked) timeseries plot.

    Paul Gierz, 2016
    """
    # Assume we have year means with the spinup period from the
    # LIG-Tx10 run. We then have 200 years of spinup and 1500 years of
    # actual simulation.
    # Get the x and y limits:
    xlims = ax.get_xlim()
    ylims = ax.get_ylim()
    ax.fill_between(np.arange(0, 200), *ylims, color="gray", alpha=0.4, hatch="//")
    tick_locations = np.arange(0, 200 + 1500 + 100, 100)
    tick_labels = ["", "Spinup Period", "130", "129", "128", "127", "126", "125", "124", "123", "122", "121", "120", "119", "118", "117", "116", "115"]
    if not suppress_ticks:
        ax.set_xticks(tick_locations)
        ax.set_xticklabels(tick_labels)
    else:
        ax.set_xticks(tick_locations)
        ax.set_xticklabels([])
