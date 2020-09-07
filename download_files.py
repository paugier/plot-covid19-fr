from pathlib import Path
from urllib.request import urlretrieve
import os
from shutil import copyfile

here = Path(__file__).absolute().parent

data = here / "data"

data.mkdir(exist_ok=True)

addresses = {
    "dep": "https://www.data.gouv.fr/fr/datasets/r/406c6a23-e283-4300-9484-54e78c8ae675",
    "france": "https://www.data.gouv.fr/fr/datasets/r/dd0de5d9-b5a5-4503-930a-7b08dc0adc7c",
}


def get_date_from_log(log):

    day, month = log.as_string().split("\n")[4].split(", ")[1].split(" ")[:2]

    if month == "Sep":
        month = "09"
    else:
        raise NotImplementedError

    return f"2020-{month}-{day}"


def download_SI_DEP(kind):
    path, log = urlretrieve(addresses[kind], data / "tmp.csv")

    date = get_date_from_log(log)

    path_new = path.with_name(f"sp-pos-quot-{kind}-{date}-19h15.csv")
    os.rename(path, path_new)

    print(f"copy {path_new.name} in data/sp-pos-quot-{kind}.csv")
    copyfile(path_new, data / f"sp-pos-quot-{kind}.csv")

    return path, log


def download_dep():
    return download_SI_DEP("dep")


def download_france():
    return download_SI_DEP("france")


if __name__ == "__main__":
    path, log = download_dep()
    download_france()
