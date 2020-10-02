from datetime import datetime, timedelta
from math import pi

import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle

from .util import complete_df_1loc_1age, population
from .load_data import load_dataframe_dep, DEPARTMENTS

df_full = load_dataframe_dep()

df = df_full[df_full.cl_age90 == 0]


fmt_date = "%Y-%m-%d"
date_max = df.index.max()
date_max_obj = datetime.strptime(date_max, fmt_date)


def format_date_for_human(date):
    date_obj = datetime.strptime(date, fmt_date)
    return date_obj.strftime("%d/%m/%Y")


def give_date(delta):
    return (date_max_obj - timedelta(delta)).strftime(fmt_date)


date_file = give_date(-3)
date_last_point = give_date(3)
delta_first_point = 7
date_first_point = give_date(delta_first_point)
date_min = give_date(delta_first_point + 7)

df.index = pd.to_datetime(df.index)
df = df[df.index >= date_min]


def plot_incidence_vs_tests(ax=None, min_incidence=100, max_incidence=None):

    if ax is None:
        fig, ax = plt.subplots()
    else:
        fig = ax.figure

    markers = "ods8p*v<>^PXhH"

    for idep, dep in enumerate(DEPARTMENTS.keys()):

        if len(dep) > 2:
            # skip DOM-TOM (only "métropole")
            continue

        tmp = df[df.dep == dep].copy()
        complete_df_1loc_1age(tmp, dep)
        tmp = tmp[
            (tmp.index >= date_first_point) & (tmp.index <= date_last_point)
        ]

        tmp["Tc_scaled"] = 100000 / population[dep] * tmp["Tc"]

        last = tmp[tmp.index == tmp.index.max()]
        nb_tests = last["Tc"].values[0]
        last_Tc_scaled = last["Tc_scaled"].values[0]
        last_incidence = last["incidence"].values[0]

        if (
            nb_tests > 1000
            and last_incidence > min_incidence
            and (max_incidence is None or last_incidence < max_incidence)
        ):
            ax.plot(tmp.Tc_scaled, tmp.incidence, color="lightgray", zorder=1)
            ax.scatter(
                tmp.Tc_scaled,
                tmp.incidence,
                c=tmp.index,
                marker=markers[idep % len(markers)],
                zorder=2,
            )

            ax.text(last_Tc_scaled - 10, last_incidence + 2, dep)

    ax.set_xlabel("Nombre de tests 7 derniers jours / 100000 hab.")
    ax.set_ylabel("Incidence (cas positifs sur 7 jours par 100000 hab.)")

    ylim = incidence_min, incidence_max = ax.get_ylim()
    xlim = nb_tests_min, nb_tests_max = ax.get_xlim()

    delta_incidence = incidence_max - incidence_min
    delta_nb_tests = nb_tests_max - nb_tests_min

    def plot_positivity_line(nb_tests, incidence, coef_position_text=0.93):
        positivity = 100 * incidence / nb_tests
        ax.plot([0, nb_tests], [0, incidence], color="r", zorder=0, linewidth=0.5)
        ax.text(
            coef_position_text * nb_tests,
            coef_position_text * incidence,
            f"{positivity:.1f} %",
            color="r",
            rotation=6 * 180 / pi * incidence / nb_tests,
        )

    plot_positivity_line(nb_tests_max, incidence_max)
    plot_positivity_line(nb_tests_max - delta_nb_tests / 3, incidence_max)
    plot_positivity_line(nb_tests_max, incidence_max - delta_incidence / 3)
    plot_positivity_line(nb_tests_max, incidence_max - 2 * delta_incidence / 3)

    ax.set_xlim(xlim)
    ax.set_ylim(ylim)

    coll = ax.collections[0]
    cmap = coll.get_cmap()

    incidence = incidence_max - 0.1 * delta_incidence
    x_points = nb_tests_min + 0.08 * delta_nb_tests
    x_text = nb_tests_min + 0.11 * delta_nb_tests

    ax.scatter(
        x_points,
        incidence,
        color=cmap.colors[0],
        marker="o",
        zorder=2,
    )
    ax.text(x_text, incidence - 2, format_date_for_human(date_first_point))

    incidence -= 0.06 * delta_incidence
    ax.scatter(
        x_points,
        incidence,
        color=cmap.colors[-1],
        marker="o",
        zorder=2,
    )
    ax.text(x_text, incidence - 2, format_date_for_human(date_last_point))

    incidence -= 0.06 * delta_incidence
    ax.text(x_points - 10, incidence - 2, "% taux de positivité", color="r")

    rect = Rectangle(
        (x_points - 0.02 * delta_nb_tests, incidence - 0.03 * delta_incidence),
        0.28 * delta_nb_tests,
        0.19 * delta_incidence,
        linewidth=1,
        edgecolor="k",
        facecolor="white",
    )
    ax.add_patch(rect)

    fig.suptitle(
        f"Données SI-DEP {format_date_for_human(date_file)},"
        f" incidence > {min_incidence}"
    )
    return ax


if __name__ == "__main__":

    ax = plot_incidence_vs_tests()
    ax.figure.tight_layout()
    window_title = f"incidence_vs_tests{date_file}"
    ax.figure.canvas.set_window_title(window_title)
    plt.show()
