from pathlib import Path

import pandas as pd

from departements import DEPARTMENTS
from population import population

here = Path(__file__).absolute().parent

data = here / "data"


def load_dataframe_dep():
    return pd.read_csv(data / "sp-pos-quot-dep.csv", sep=";", index_col=1)



def load_dataframe_france(no_sex=True):

    df = pd.read_csv(data / "sp-pos-quot-france.csv", sep=";", index_col=1)

    return df[["P", "T", "cl_age90"]].copy()
