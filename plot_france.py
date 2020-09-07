import matplotlib.pyplot as plt

from load_data import load_dataframe_france

from plot_1dep import plot_1loc

df = load_dataframe_france()


def plot_france(yscale="log"):
    return plot_1loc(df, "France", yscale=yscale)


if __name__ == "__main__":

    plot_france()
    plt.show()
