from pathlib import Path

import pandas as pd

from departements import DEPARTMENTS
from population import population

here = Path(__file__).absolute().parent
path = here / "data" / "sp-pos-quot-dep.csv"


def load_dataframe():
    return pd.read_csv(path, sep=";", index_col=1)
