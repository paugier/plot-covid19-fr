from pathlib import Path

import numpy as np

import matplotlib.pyplot as plt

import pandas as pd

from transonic import jit

from departements import DEPARTMENTS
from population import population

here = Path(__file__).absolute().parent

paths = sorted(here.glob("sp-pos-quot-dep-*.csv"))

path = paths[-1]

print(path)


@jit
def cumul7(data: "int[]"):
    n = 7
    ret = np.empty_like(data)

    tmp = 0
    for i in range(n):
        ret[i] = tmp = tmp + data[i]

    for i in range(n, len(data)):
        ret[i] = tmp = tmp + data[i] - data[i - n]

    return ret


df = pd.read_csv(path, sep=";", index_col=1)

df = df[df.cl_age90 == 0]


df["ratio"] = 100 * df.P / df["T"]

df.index = pd.to_datetime(df.index)
df = df[df.index > "2020-07-15"]

# df_38 = df[df.dep < "100"]

# df_38 = df_38[df_38.cl_age90 == 0]

# df_38.plot(y="ratio")

fig, ax = plt.subplots()
fig1, ax1 = plt.subplots()

for idep in range(1, 96):
    if idep == 20:
        continue

    dep = f"{idep:02d}"
    tmp = df[df.dep == dep].copy()

    tmp["Tc"] = cumul7(tmp["T"].values)
    tmp["Pc"] = cumul7(tmp["P"].values)

    tmp["incidence"] = 100000 * tmp["Pc"] / population[dep]

    tmp["ratio_c"] = 100 * tmp["Pc"] / tmp["Tc"]

    last = tmp[tmp.index == tmp.index.max()]

    nb_tests = last["Tc"].values[0]
    last_ratio = last["ratio_c"].values[0]
    last_incidence = last["incidence"].values[0]

    print(
        f"{dep:2}, {DEPARTMENTS[dep]:23} : {nb_tests = :5d}, "
        f"{last_ratio = :6.2f}\n{last_incidence = :6.2f}"
    )

    style = None
    if idep == 38:
        style = "--"

    if (nb_tests > 1000 and last_ratio > 6) or idep == 38:
        tmp.plot(y="ratio_c", ax=ax, label=DEPARTMENTS[dep], style=style)

    # if (nb_tests > 1000 and last_incidence > 70) or idep == 38:

        tmp.plot(y="incidence", ax=ax1, label=DEPARTMENTS[dep], style=style)


ax.set_title("Taux de positivité sur 7 jours")
ax1.set_title("Incidence (cas positifs sur 7 jours par 100000 hab.)")

fig.tight_layout()
fig1.tight_layout()

plt.show()
