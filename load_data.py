from pathlib import Path

import pandas as pd

from departements import DEPARTMENTS
from population import population

here = Path(__file__).absolute().parent

data = here / "data"


def load_dataframe_dep():
    return pd.read_csv(
        data / "sp-pos-quot-dep.csv",
        sep=";",
        index_col=1,
        dtype={"jour": str, "dep": str},
    )


def load_dataframe_france(no_sex=True):

    df = pd.read_csv(
        data / "sp-pos-quot-france.csv",
        sep=";",
        index_col=1,
        dtype={"jour": str, "dep": str},
    )

    return df[["P", "T", "cl_age90"]].copy()


def load_hospi():
    df = pd.read_csv(
        data / "donnees-hospitalieres-nouveaux-covid19-hospi.csv",
        sep=";",
        index_col=1,
        dtype={"jour": str, "dep": str},
    )
    df = df.rename(
        {key: key[6:] for key in df.keys() if key.startswith("incid_")},
        axis="columns",
    )

    # see https://www.leparisien.fr/societe/covid-19-pourquoi-la-hausse-soudaine-de-la-mortalite-en-24-heures-doit-etre-nuancee-19-09-2020-8387748.php
    df.loc[(df.index == "2020-09-18") & (df.dep == "91"), "hosp"] = 30
    df.loc[(df.index == "2020-09-18") & (df.dep == "91"), "dc"] = 0
    df.loc[(df.index == "2020-09-18") & (df.dep == "91"), "rad"] = 0
    return df
