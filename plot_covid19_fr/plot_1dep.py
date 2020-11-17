from datetime import datetime, timedelta

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from .util import complete_df_1loc_1age, shift_date_str, default_first_day_in_plot
from .load_data import load_dataframe_dep, DEPARTMENTS, population

fmt = "%Y-%m-%d"
df = load_dataframe_dep()
date_max = df.index.max()
date_max_obj = datetime.strptime(date_max, fmt)
date_bad_data_obj = date_max_obj - timedelta(2)
date_bad_data = date_bad_data_obj.strftime(fmt)
date_for_R_obj = date_bad_data_obj - timedelta(7)
date_for_R = date_for_R_obj.strftime(fmt)


def plot_1loc(
    df_loc,
    for_title=None,
    yscale="linear",
    ax=None,
    location=None,
    with_incidence=False,
    axes_incidence=None,
    first_day_in_plot=default_first_day_in_plot,
):

    if yscale == "linear daily":
        yscale = "linear"
        daily = True
    else:
        daily = False

    if ax is None:
        fig, ax = plt.subplots()
        tight_layout = True
    else:
        fig = ax.figure
        tight_layout = False

    if with_incidence:
        if axes_incidence is None:
            fig_incidence, axes_incidence = plt.subplots(2, 1, sharex=True)
            ax_incidence, ax_number_tests = axes_incidence
        else:
            ax_incidence, ax_number_tests = axes_incidence
            fig_incidence = ax_incidence.figure

        ax_number_tests.set_title(
            "Nombre de tests 7 derniers jours / 100000 hab."
        )

    first_day_in_plot_minus7 = shift_date_str(first_day_in_plot, -7)

    def make_df_1age(age):
        tmp = df_loc[df_loc.cl_age90 == age].copy()

        tmp.index = pd.to_datetime(tmp.index)
        tmp = tmp[tmp.index >= first_day_in_plot_minus7]

        complete_df_1loc_1age(tmp, location)

        return tmp[tmp.index >= first_day_in_plot]

    tmp = make_df_1age(0)
    tmp.plot(y="ratio_c", ax=ax, label=f"total", color="k", linewidth=3)

    if with_incidence:
        I_for_R = tmp["incidence"]
        I_for_R = I_for_R[
            (I_for_R.index >= date_for_R) & (I_for_R.index <= date_bad_data)
        ]
        log2_I = np.log2(I_for_R.values)
        sigma12, _ = np.polyfit(np.arange(len(log2_I)), log2_I, 1)
        R_eff = 2 ** (7 * sigma12)
        ax_incidence.set_title(
            "Taux d'incidence, $R_{eff} \simeq $"
            fr" {R_eff:.2f} $\Leftrightarrow "
            fr"\tau \simeq $ {1/sigma12:.1f} jours"
        )

        if yscale == "linear":
            tmp.plot(y="incidence", ax=ax_incidence, color="k", legend=False)
            ax_incidence.plot(
                [date_for_R_obj, date_bad_data_obj], [0, 0], "k-h", markersize=4
            )
            tmp["Tc1"] = 100000 / population[location] * tmp["Tc"]
            tmp.plot(y="Tc1", ax=ax_number_tests, color="k", legend=False)

            if daily:
                tmp["incidence_daily"] = 700000 / population[location] * tmp["P"]
                tmp.plot(
                    y="incidence_daily",
                    ax=ax_incidence,
                    color="k",
                    legend=False,
                    marker=".",
                    linestyle="None",
                )
                tmp["T1"] = 700000 / population[location] * tmp["T"]
                tmp.plot(
                    y="T1",
                    ax=ax_number_tests,
                    color="k",
                    legend=False,
                    marker=".",
                    linestyle="None",
                )

        incidence_tmp = 0.0
        number_tests_tmp = 0

        incidence_bottom = 0.0
        number_tests_bottom = 0

    for age in 9 + 10 * np.arange(7):
        label = f"{age-9}-{age}"
        tmp = make_df_1age(age)
        tmp.plot(y="ratio_c", ax=ax, label=label)

        if with_incidence:
            incidence = tmp["incidence"]
            number_tests = 100000 / population[location] * tmp["Tc"]
            if daily:
                pass
            elif yscale == "linear":
                incidence_tmp += incidence
                ax_incidence.fill_between(
                    tmp.index, incidence_tmp, incidence_bottom
                )
                incidence_bottom = incidence_tmp.copy()

                number_tests_tmp += number_tests
                ax_number_tests.fill_between(
                    tmp.index, number_tests_tmp, number_tests_bottom
                )
                number_tests_bottom = number_tests_tmp.copy()
            else:
                tmp["incidence_age"] = incidence
                tmp.plot(y="incidence_age", ax=ax_incidence, legend=False)
                tmp["number_tests_age"] = number_tests
                tmp.plot(y="number_tests_age", ax=ax_number_tests, legend=False)

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
    tmp.plot(y="ratio_c", ax=ax, label=f">=70", linewidth=3)

    ax.axvline(date_bad_data_obj, color="k", linestyle=":")

    if with_incidence:
        incidence = tmp["incidence"]
        number_tests = 100000 / population[location] * tmp["Tc"]
        if daily:
            pass
        elif yscale == "linear":
            incidence_tmp += incidence
            ax_incidence.fill_between(tmp.index, incidence_tmp, incidence_bottom)

            number_tests_tmp += number_tests
            ax_number_tests.fill_between(
                tmp.index, number_tests_tmp, number_tests_bottom
            )
        else:
            ax_incidence.plot(tmp.index, incidence, linewidth=3)
            ax_number_tests.plot(tmp.index, number_tests, linewidth=3)

        for _ in [ax_incidence, ax_number_tests]:
            _.axvline(date_bad_data_obj, color="k", linestyle=":")
            _.grid(True, axis="y")
            _.set_yscale(yscale)

    ax.grid(True, axis="y")

    title = "Taux de positivité sur 7 jours"

    if for_title:
        title += ", " + for_title

    ax.set_title(title)
    ax.set_yscale(yscale)

    if tight_layout:
        fig.tight_layout()

    if with_incidence and tight_layout:
        fig_incidence.tight_layout()

    return ax


def plot_1dep(
    dep,
    yscale="linear",
    ax=None,
    with_incidence=False,
    axes_incidence=None,
    first_day_in_plot=default_first_day_in_plot,
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
        first_day_in_plot=first_day_in_plot,
    )


if __name__ == "__main__":
    # plot_1dep(13)
    # plot_1dep(33)
    plot_1dep(38, with_incidence=True)
    # plot_1dep(44)
    # plot_1dep(75)
    # plot_1dep(17)

    plt.show()
