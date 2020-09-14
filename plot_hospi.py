import matplotlib.pyplot as plt
import pandas as pd

from load_data import load_hospi, DEPARTMENTS

from util import cumul7

df = load_hospi()


def plot_hospi(loc, set_title=False, axes=None):

    df.index = pd.to_datetime(df.index)

    if loc == "France":
        tmp = df.groupby(["jour"]).sum()
    else:
        tmp = df[df.dep == loc].copy()
        tmp = tmp.drop(columns=["dep"])

    tmp = tmp[tmp.index > "2020-07-23"]

    for key in tmp.keys():
        tmp[key + "_c"] = cumul7(tmp[key].values) / 7
    tmp = tmp[tmp.index > "2020-07-30"]

    if axes is None:
        fig, (ax0, ax1) = plt.subplots(2, 1, sharex=True)
        tight_layout = True
    else:
        (ax0, ax1) = axes
        fig = ax0.figure
        tight_layout = False

    tmp["solde"] = tmp.hosp_c - tmp.rad_c - tmp.dc_c
    # tmp.rad_c = -tmp.rad_c

    tmp.plot(y="hosp_c", ax=ax0, label="hospitalisations")
    tmp.plot(y="rad_c", ax=ax0, label="retours à domicile")
    tmp.plot(y="solde", ax=ax0, color="k", linewidth=2)

    ax0.axhline(0, color="k", linestyle=":")

    tmp.plot(y="rea_c", ax=ax1, label="réanimation", color="r")
    tmp.plot(y="dc_c", ax=ax1, label="décès", color="k")

    if set_title:
        if loc == "France":
            title = "France"
        else:
            title = f"{DEPARTMENTS[loc]} ({dep:2})"

        ax0.set_title(title + ", (moyenne 7j)")

    if tight_layout:
        fig.tight_layout()

    return ax0, ax1


if __name__ == "__main__":

    plot_hospi("75")
    plt.show()
