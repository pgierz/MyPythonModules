# Python_Helpers
A library of some useful python wrappers to facilitate analysis and visualization work

# How to Install:
Please follow the instructions to get the functions working on your account.
1. clone the repository
`git clone https://github.com/AWI-Paleodyn/Python_Helpers.git`
2. set up your `PYTHONPATH` (in `.bashrc` or similar)
`export PYTHONPATH=${HOME}/Python_Helpers:${PYTHONPATH}`
3. Test
```shell

$ ipython
... some start up message ...
[1] from plot_tools import plot_var_from_ncdf_file 

```

# How to use
I'll probably add a detailed description to this in the next several days/weeks. In principle, two important modules are ready to use:

- `plot_tools` : contains functions for plotting netcdf variables onto maps

- `basemap_wrappers` : some shortcuts for the Basemap toolkit to make maps faster

Here's a minimal example script:
```python
from plot_tools import plot_var_from_ncdf_file
from basemap_wrappers import map_global
import matplotlib.pyplot as plt
from scipy.io import netcdf

f = netcdf.netcdf_file("/csys/nobackup1_PALEO/pgierz/cosmos-aso/Eem120-B/post/echam5/Eem120-B_echam5_tsurf_timmean.nc")
fig, axs = plt.subplots(1, 1)
m = map_global(thisax=axs, fill_color=None)
plot_var_from_ncdf_file("tsurf", f, m)
plt.show()
```

Good luck!
Paul
