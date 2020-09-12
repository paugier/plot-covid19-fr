import numpy as np

import pandas as pd

import matplotlib.pyplot as plt

from util import complete_df_1loc_1age

from load_data import load_dataframe_dep, DEPARTMENTS

df = load_dataframe_dep()


def plot_1loc(
    df_loc,
    for_title=None,
    yscale="lin",
    ax=None,
    location=None,
    with_incidence=False,
    axes_incidence=None,
):

    if ax is None:
        fig, ax = plt.subplots()
    else:
        fig = ax.figure

    if with_incidence:
        if axes_incidence is None:
            fig_incidence, axes_incidence = plt.subplots(2, 1, sharex=True)
            ax_incidence, ax_number_tests = axes_incidence
        else:
            ax_incidence, ax_number_tests = axes_incidence
            fig_incidence = ax_incidence.figure

        ax_incidence.set_title(
            "Taux d'incidence"
        )
        ax_number_tests.set_title(
            "Nombre de tests 7 derniers jours / 7"
        )

    def make_df_1age(age):
        tmp = df_loc[df_loc.cl_age90 == age].copy()

        tmp.index = pd.to_datetime(tmp.index)
        tmp = tmp[tmp.index > "2020-07-23"]

        complete_df_1loc_1age(tmp, location)

        return tmp[tmp.index > "2020-07-30"]

    tmp = make_df_1age(0)
    tmp.plot(y="ratio_c", ax=ax, label=f"total", color="k", linewidth=3)

    if with_incidence:
        tmp.plot(y="incidence", ax=ax_incidence, color="k", legend=False)
        tmp["Tc1"] = tmp["Tc"] / 7
        tmp.plot(y="Tc1", ax=ax_number_tests, color="k", legend=False)

        incidence_tmp = 0.0
        number_tests_tmp = 0

        incidence_bottom = 0.0
        number_tests_bottom = 0

    for age in 9 + 10 * np.arange(7):
        label = f"{age-9}-{age}"
        tmp = make_df_1age(age)
        tmp.plot(y="ratio_c", ax=ax, label=label)

        if with_incidence:
            incidence_tmp += tmp["incidence"]
            ax_incidence.fill_between(tmp.index, incidence_tmp, incidence_bottom)
            incidence_bottom = incidence_tmp.copy()

            number_tests_tmp += tmp["Tc"] / 7
            ax_number_tests.fill_between(
                tmp.index, number_tests_tmp, number_tests_bottom
            )
            number_tests_bottom = number_tests_tmp.copy()

    tmp79 = make_df_1age(79)
    tmp89 = make_df_1age(89)
    tmp90 = make_df_1age(90)

    tmp = pd.DataFrame(
        {
            "Tc": tmp79["Tc"] + tmp89["Tc"] + tmp90["Tc"],
            "Pc": tmp79["Pc"] + tmp89["Pc"] + tmp90["Pc"],
            "incidence": tmp79["incidence"]
            + tmp89["incidence"]
            + tmp90["incidence"],
        },
        index=tmp79.index,
    )

    tmp["ratio_c"] = 100 * tmp["Pc"] / tmp["Tc"]
    tmp.plot(y="ratio_c", ax=ax, label=f">=70")

    if with_incidence:
        incidence_tmp += tmp["incidence"]
        ax_incidence.fill_between(tmp.index, incidence_tmp, incidence_bottom)

        number_tests_tmp += tmp["Tc"] / 7
        ax_number_tests.fill_between(tmp.index, number_tests_tmp, number_tests_bottom)

    ax.grid(True, axis="y")

    title = "Taux de positivité sur 7 jours"

    if for_title:
        title += ", " + for_title

    ax.set_title(title)
    ax.set_yscale(yscale)

    fig.tight_layout()

    if with_incidence:
        fig_incidence.tight_layout()

    return ax


def plot_1dep(
    dep, yscale="linear", ax=None, with_incidence=False, axes_incidence=None
):
    if isinstance(dep, int):
        dep = f"{dep:02d}"
    df_dep = df[df.dep == dep].copy()
    return plot_1loc(
        df_dep,
        for_title=f"{DEPARTMENTS[dep]} ({dep:2})",
        yscale=yscale,
        ax=ax,
        location=dep,
        with_incidence=with_incidence,
        axes_incidence=axes_incidence,
    )


if __name__ == "__main__":
    # plot_1dep(13)
    # plot_1dep(33)
    plot_1dep(38, with_incidence=True)
    # plot_1dep(44)
    # plot_1dep(75)
    # plot_1dep(17)

    plt.show()