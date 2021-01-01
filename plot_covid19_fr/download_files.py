from pathlib import Path
from urllib.request import urlretrieve
import os
from shutil import copyfile
from warnings import warn

here = Path(__file__).absolute().parent

data = here.parent / "data"

data.mkdir(exist_ok=True)

addresses = {
    "dep": "https://www.data.gouv.fr/fr/datasets/r/406c6a23-e283-4300-9484-54e78c8ae675",
    "france": "https://www.data.gouv.fr/fr/datasets/r/dd0de5d9-b5a5-4503-930a-7b08dc0adc7c",
    "hospi": "https://www.data.gouv.fr/fr/datasets/r/6fadff46-9efd-4c53-942a-54aca783c30c",
}


def get_date_from_log(log):

    day, month = log.as_string().split("\n")[4].split(", ")[1].split(" ")[:2]

    if month == "Sep":
        month = "09"
    elif month == "Oct":
        month = "10"
    elif month == "Nov":
        month = "11"
    elif month == "Dec":
        month = "12"
    elif month == "Jan":
        month = "01"
    elif month == "Jul":
        month = "07"
        warn(
            "Ooops, strange! month is Jul! Maybe https://www.data.gouv.fr is down?"
        )
    else:
        print(month, day)
        print(log.as_string())
        raise NotImplementedError

    return f"2020-{month}-{day}"


def download_SI_DEP(kind):
    path, log = urlretrieve(addresses[kind], data / "tmp.csv")

    date = get_date_from_log(log)

    if kind in ["dep", "france"]:
        prefix = "sp-pos-quot"
        hour = "19h15"
    elif kind == "hospi":
        prefix = "donnees-hospitalieres-nouveaux-covid19"
        hour = "19h00"
    else:
        raise ValueError

    path_new = path.with_name(f"{prefix}-{kind}-{date}-{hour}.csv")
    os.rename(path, path_new)

    print(f"copy {path_new.name} in data/{prefix}-{kind}.csv")
    copyfile(path_new, data / f"{prefix}-{kind}.csv")

    return path, log


def download_dep():
    return download_SI_DEP("dep")


def download_france():
    return download_SI_DEP("france")


def download_hospital():
    return download_SI_DEP("hospi")


if __name__ == "__main__":
    path, log = download_dep()
    download_france()
    download_hospital()
