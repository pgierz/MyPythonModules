# Python_Helpers
A library of some useful python wrappers to facilitate analysis and
visualization work. Important to note here that *none* of these tools are
directly written by myself, I've just glued the functionality into easier to
digest chunks. All of the actual work is done by the wonderful people
writing [matplotlib](https://github.com/matplotlib/matplotlib)
and [basemap](https://github.com/matplotlib/basemap)

# How to Install:
Please follow the instructions to get the functions working on your account.
1. clone the repository (alternatively, make a github account, fork, and clone your own version)

`git clone https://github.com/AWI-Paleodyn/Python_Helpers.git`

2. set up your `PYTHONPATH` (in `.bashrc` or similar)

`export PYTHONPATH=${HOME}/Python_Helpers:${PYTHONPATH}`

3. Test
```shell

$ ipython
... some start up message ...
[1] from plot_tools import plot_var_from_ncdf_file 

```
if this import successfully goes through, everything is configured correctly. Go celebrate with a coffee! :coffee: 


# How to use
I'll probably add a detailed description to this in the next several days/weeks. In principle, two important modules are ready to use:

- `plot_tools` : contains functions for plotting netcdf variables onto maps

- `basemap_wrappers` : some shortcuts for the Basemap toolkit to make maps faster

Here's a minimal example script, also included in the directory `examples`:

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
