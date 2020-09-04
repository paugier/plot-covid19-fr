import pandas as pd

import matplotlib.pyplot as plt

from util import complete_df_1dep_1age

from load_data import load_dataframe, DEPARTMENTS

df = load_dataframe()

df = df[df.cl_age90 == 0]

df.index = pd.to_datetime(df.index)
df = df[df.index > "2020-08-01"]

df["ratio"] = 100 * df.P / df["T"]

fig, ax = plt.subplots()
fig1, ax1 = plt.subplots()

for idep in range(1, 96):
    if idep == 20:
        continue

    dep = f"{idep:02d}"
    tmp = df[df.dep == dep].copy()
    complete_df_1dep_1age(tmp, dep)

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
