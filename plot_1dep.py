import numpy as np

import pandas as pd

import matplotlib.pyplot as plt

from util import complete_df_1dep_1age

from load_data import load_dataframe_dep, DEPARTMENTS

df = load_dataframe_dep()


def plot_1loc(df_loc, for_title=None, yscale="lin"):

    fig, ax = plt.subplots()

    def make_df_1age(age):
        tmp = df_loc[df_loc.cl_age90 == age].copy()

        tmp.index = pd.to_datetime(tmp.index)
        tmp = tmp[tmp.index > "2020-07-23"]

        complete_df_1dep_1age(tmp)

        return tmp[tmp.index > "2020-07-30"]

    tmp = make_df_1age(0)
    tmp.plot(y="ratio_c", ax=ax, label=f"total", color="k", linewidth=2)

    for age in 9 + 10 * np.arange(8):
        tmp = make_df_1age(age)
        tmp.plot(y="ratio_c", ax=ax, label=f"{age-9}-{age}")

    tmp89 = make_df_1age(89)
    tmp90 = make_df_1age(90)

    tmp = pd.DataFrame(
        {"Tc": tmp89["Tc"] + tmp90["Tc"], "Pc": tmp89["Pc"] + tmp90["Pc"]},
        index=tmp89.index,
    )

    tmp["ratio_c"] = 100 * tmp["Pc"] / tmp["Tc"]

    tmp.plot(y="ratio_c", ax=ax, label=f">80")

    ax.grid(True, axis="y")

    title = "Taux de positivité sur 7 jours"

    if for_title:
        title += ", " + for_title

    ax.set_title(title)

    ax.set_yscale(yscale)

    fig.tight_layout()

    return ax


def plot_1dep(idep, yscale="lin"):
    dep = f"{idep:02d}"
    df_dep = df[df.dep == dep].copy()
    return plot_1loc(df_dep, for_title=f"{DEPARTMENTS[dep]} ({dep:2})", yscale=yscale)


if __name__ == "__main__":
    plot_1dep(13)
    plot_1dep(33)
    plot_1dep(38)
    plot_1dep(44)
    plot_1dep(75)
    plot_1dep(17)

    plt.show()
