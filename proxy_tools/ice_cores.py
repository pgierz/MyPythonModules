#!/usr/bin/env python
# coding: utf-8
import pandas


def interglacial_ice_cores(t, m, colmap, s=60, alpha=0.7, **opts):
    icecore_data = pandas.read_excel("/Users/pgierz/Research/data/LIG_IceCore_Compilation_PG_July16.xlsx")
    for i, r in icecore_data.iterrows():
        if not pandas.isnull(r[t]):
            ice_points = m.scatter(r["Lon"], r["Lat"], s=s, alpha=alpha, c=r[t], marker="o",
                                   cmap=colmap, latlon=True, **opts)
    return ice_points
