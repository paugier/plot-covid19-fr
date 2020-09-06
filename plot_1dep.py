import numpy as np

import pandas as pd

import matplotlib.pyplot as plt

from util import complete_df_1dep_1age

from load_data import load_dataframe, DEPARTMENTS

df = load_dataframe()


def plot_month(idep):

    dep = f"{idep:02d}"

    fig, ax = plt.subplots()

    def make_df_1age(age):
        tmp = df[(df.cl_age90 == age) & (df.dep == dep)].copy()

        tmp.index = pd.to_datetime(tmp.index)
        tmp = tmp[tmp.index > "2020-07-23"]

        complete_df_1dep_1age(tmp)

        return tmp[tmp.index > "2020-07-30"]

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
    ax.set_title(f"Taux de positivité sur 7 jours, {DEPARTMENTS[dep]} ({dep:2})")

    fig.tight_layout()


if __name__ == "__main__":
    plot_month(13)
    plot_month(33)
    plot_month(38)
    plot_month(44)
    plot_month(75)
    plot_month(17)

    plt.show()
