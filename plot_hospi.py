import matplotlib.pyplot as plt
import pandas as pd

from load_data import load_hospi, DEPARTMENTS

from util import cumul7

df = load_hospi()

dep = "75"

df.index = pd.to_datetime(df.index)

tmp = df[df.dep == dep].copy()
tmp = tmp.drop(columns=["dep"])

assert "dep" not in tmp.keys()

tmp = tmp[tmp.index > "2020-07-23"]

for key in tmp.keys():
    tmp[key + "_c"] = cumul7(tmp[key].values) / 7
tmp = tmp[tmp.index > "2020-07-30"]

fig, (ax0, ax1) = plt.subplots(2, 1, sharex=True)

tmp["solde"] = tmp.hosp_c - tmp.rad_c - tmp.dc_c
tmp.rad_c = -tmp.rad_c

tmp.plot(y="hosp_c", ax=ax0, label="hospitalisations")
tmp.plot(y="rad_c", ax=ax0, label="retours à domicile")
tmp.plot(y="solde", ax=ax0)

ax0.axhline(0, color="k", linestyle=":")

tmp.plot(y="rea_c", ax=ax1, label="réanimation")
tmp.plot(y="dc_c", ax=ax1, label="décès")

ax0.set_title(f"{DEPARTMENTS[dep]} ({dep:2}), (moyenne 7j)")

fig.tight_layout()
plt.show()
