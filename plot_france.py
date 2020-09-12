import matplotlib.pyplot as plt

from load_data import load_dataframe_france

from plot_1dep import plot_1loc

df = load_dataframe_france()


def plot_france(yscale="log", ax=None, with_incidence=False, axes_incidence=None):
    return plot_1loc(
        df,
        "France",
        yscale=yscale,
        location="France",
        ax=ax,
        with_incidence=with_incidence,
        axes_incidence=axes_incidence,
    )


if __name__ == "__main__":

    plot_france(with_incidence=True)
    plt.show()
