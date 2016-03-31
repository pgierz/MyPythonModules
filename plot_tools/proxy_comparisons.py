import numpy as np

def decorate_ax_1to1(ax):
    xmin, xmax = ax.get_xlim()
    xmax = xmax*1.5
    ymin, ymax = ax.get_ylim()
    ymax = ymax*1.5
    ax.plot(np.arange(xmin, xmax), np.arange(ymin, ymax),
            color="black", marker=None)
    ax.fill_between(np.arange(xmin, 1), 0, ymax,
                    color="gray", alpha=0.1, hatch="//")
    ax.fill_between(np.arange(0, xmax), ymin, 0,
                    color="gray", alpha=0.1, hatch="//")
    return ax
