import matplotlib.pyplot as plt
import pandas as pd

from .load_data import load_hospi, DEPARTMENTS
from .util import cumul7, shift_date_str, default_first_day_in_plot

df = load_hospi()


def plot_hospi(
    loc,
    axes=None,
    title=None,
    yscale="linear",
    first_day_in_plot=default_first_day_in_plot,
):

    df.index = pd.to_datetime(df.index)

    if loc == "France":
        tmp = df.groupby(["jour"]).sum()
    else:
        tmp = df[df.dep == loc].copy()
        tmp = tmp.drop(columns=["dep"])

    first_day_in_plot_minus7 = shift_date_str(first_day_in_plot, -7)
    tmp = tmp[tmp.index >= first_day_in_plot_minus7]

    for key in tmp.keys():
        tmp[key + "_c"] = cumul7(tmp[key].values) / 7
    tmp = tmp[tmp.index >= first_day_in_plot]

    if axes is None:
        fig, (ax0, ax1) = plt.subplots(2, 1, sharex=True)
        tight_layout = True
    else:
        (ax0, ax1) = axes
        fig = ax0.figure
        tight_layout = False

    if yscale == "linear":
        tmp["solde"] = tmp.hosp_c - tmp.rad_c - tmp.dc_c
        step_legend = 2
    else:
        step_legend = 1

    def plot_points(y, ax):
        tmp.plot(
            y=y,
            ax=ax,
            marker=".",
            color=ax.lines[-1].get_color(),
            linestyle="None",
        )

    tmp.plot(y="hosp_c", ax=ax0, label="hospitalisations")

    if yscale == "linear":
        plot_points("hosp", ax0)

    tmp.plot(y="rad_c", ax=ax0, label="retours à domicile")

    if yscale == "linear":
        plot_points("rad", ax0)
        tmp.plot(y="solde", ax=ax0, color="k", linewidth=2)

    ax0.axhline(0, color="k", linestyle=":")

    handles, labels = ax0.get_legend_handles_labels()
    ax0.legend(handles[::step_legend], labels[::step_legend])

    tmp.plot(y="rea_c", ax=ax1, label="réanimation", color="r")
    if yscale == "linear":
        plot_points("rea", ax1)
    tmp.plot(y="dc_c", ax=ax1, label="décès", color="k")
    if yscale == "linear":
        plot_points("dc", ax1)

    handles, labels = ax1.get_legend_handles_labels()
    ax1.legend(handles[::step_legend], labels[::step_legend])

    if title is None:
        if loc == "France":
            title = "France"
        else:
            title = f"{DEPARTMENTS[loc]} ({loc})"

    ax0.set_title(title + " (moyenne 7j)")

    for _ in (ax0, ax1):
        _.grid(True, axis="y")
        _.set_yscale(yscale)

    if tight_layout:
        fig.tight_layout()

    return ax0, ax1


if __name__ == "__main__":

    plot_hospi("75", yscale="log")
    plt.show()
