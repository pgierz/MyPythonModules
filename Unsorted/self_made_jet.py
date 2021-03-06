list = [
    [255./255., 0./255., 255./255.],
    [218./255., 112./255., 214./255.],
    [186./255., 85./255., 211./255.],
    [160./255., 0./255., 200./255.],
    [110./255., 0./255., 220./255.],
    [30./255., 60./255., 255./255.],
    [0./255., 160./255., 255./255.],
    [0./255., 200./255., 200./255.],
    [175./255., 238./255., 238./255.],
    [255./255., 255./255., 255./255.],
    [20./255., 218./255., 7./255.],
    [158./255., 247./255., 0./255.],
    [236./255., 245./255., 0./255.],
    [247./255., 185./255., 0./255.],
    [241./255., 119./255., 0./255.],
    [250./255., 0./255., 0./255.],
    [204./255., 0./255., 0./255.],
    [153./255., 0./255., 0./255.],
    [102./255., 0./255., 0./255.]
    ]


import matplotlib as mpl
import matplotlib.colorbar as colorbar
import numpy as np
import matplotlib.pyplot as plt

cmap = mpl.colors.ListedColormap(list)
bounds = [-4.5, -4.0, -3.5, -3.0, -2.5, -2.0, -1.5, -1.0, -0.5, -0.25 ,0.25, 0.5, 1.0, 1.5, 2.0, 2.5, 3.0, 3.5, 4.0, 4.5] # 19
norm = mpl.colors.BoundaryNorm(bounds, cmap.N)
cb = colorbar.ColorbarBase(plt.subplot(111), cmap = cmap, norm = norm)
plt.show()
