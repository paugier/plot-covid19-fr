from pathlib import Path

import pandas as pd

from departements import DEPARTMENTS
from population import population

here = Path(__file__).absolute().parent

paths = sorted((here / "data").glob("sp-pos-quot-dep-*.csv"))
path = paths[-1]
print(path)


def load_dataframe():
    return pd.read_csv(path, sep=";", index_col=1)
