import json
import random
from datetime import datetime, timedelta

import ipyleaflet as ipyl
import ipywidgets as ipyw
from branca.colormap import linear

from load_data import load_dataframe_dep
from population import population

df = load_dataframe_dep()
df = df[(df.cl_age90 == 0)].copy()

date_max = df.index.max()
date_max_obj = datetime.strptime(date_max, "%Y-%m-%d")
date_m7 = date_max_obj - timedelta(7)
date_m7 = date_m7.strftime("%Y-%m-%d")

df7 = df[(df.index > date_m7)][["dep", "P"]]
df7 = df7.groupby("dep").sum()

df7["incidence"] = 0.0
for dep in df7.index:
    if dep in population:
        incidence = 100000 / population[dep] * df7.P.loc[dep]
    else:
        incidence = 0
    df7.loc[dep, "incidence"] = incidence

tmp = df[(df.index == date_max)].copy()
tmp.index = tmp.dep
positivity_vs_dep = 100 * tmp["P"] / tmp["T"]


def get_positivity(dep):
    return positivity_vs_dep.loc[dep]


def get_incidence(dep):
    return df7.incidence.loc[dep]


cmap = linear.YlOrRd_09.scale(0, 150)
cmap.caption = "Taux d'incidence"


def color_dep(feature):
    dep = feature["properties"]["code"]
    value = get_incidence(dep)
    color = cmap(value)
    return {
        "color": "black",
        "fillColor": color,
    }


with open("data/departements-version-simplifiee.geojson", "r") as f:
    data_geojson_dep = json.load(f)
