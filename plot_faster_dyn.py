import random

import pandas as pd

import matplotlib.pyplot as plt

from util import complete_df_1loc_1age

from load_data import load_dataframe_dep, DEPARTMENTS

df_full = load_dataframe_dep()


def plot_faster_dyn(
    verbose=False, axes=None, min_positive_rate=6, max_positive_rate=None
):

    df = df_full[df_full.cl_age90 == 0]

    df.index = pd.to_datetime(df.index)
    df = df[df.index > "2020-07-23"]

    df["ratio"] = 100 * df.P / df["T"]

    if axes is None:
        fig, ax = plt.subplots()
        fig1, ax1 = plt.subplots()
    else:
        ax, ax1 = axes
        fig = ax.figure
        fig1 = ax1.figure

    styles = ["-", "--", ":", "-."]
    for dep in DEPARTMENTS.keys():
        if len(dep) > 2:
            continue
        tmp = df[df.dep == dep].copy()
        tmp = tmp[tmp.index > "2020-07-23"]
        complete_df_1loc_1age(tmp, dep)
        tmp = tmp[tmp.index > "2020-07-30"]

        last = tmp[tmp.index == tmp.index.max()]

        nb_tests = last["Tc"].values[0]
        last_ratio = last["ratio_c"].values[0]
        last_incidence = last["incidence"].values[0]

        if verbose:
            print(
                f"{dep:2}, {DEPARTMENTS[dep]:23} : {nb_tests = :5d}, "
                f"{last_ratio = :6.2f}\n{last_incidence = :6.2f}"
            )

        style = random.choice(styles)

        if (
            nb_tests > 1000
            and last_ratio > min_positive_rate
            and (max_positive_rate is None or last_ratio < max_positive_rate)
        ):

            label = f"{dep:2} - {DEPARTMENTS[dep]}"
            tmp.plot(y="ratio_c", ax=ax, label=label, style=style)
            tmp.plot(y="incidence", ax=ax1, label=label, style=style)

    ax.set_title("Taux de positivité sur 7 jours")
    ax1.set_title("Incidence (cas positifs sur 7 jours par 100000 hab.)")

    ax1.axhline(50, color="k")

    date_bad_data = tmp.index[-3]
    for _ in [ax, ax1]:
        _.axvline(date_bad_data, color="k", linestyle=":")
        _.legend(loc="upper left", prop={"size": 8})

    fig.tight_layout()
    fig1.tight_layout()


if __name__ == "__main__":

    plot_faster_dyn(verbose=True, min_positive_rate=7)
    plot_faster_dyn(verbose=True, min_positive_rate=5.5, max_positive_rate=7)
    plt.show()
