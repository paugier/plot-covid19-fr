from pathlib import Path
from urllib.request import urlretrieve
import os
from shutil import copyfile

here = Path(__file__).absolute().parent

data = here / "data"

data.mkdir(exist_ok=True)

address = (
    "https://www.data.gouv.fr/fr/datasets/r/406c6a23-e283-4300-9484-54e78c8ae675"
)


def download():
    path, log = urlretrieve(address, data / "tmp.csv")

    day, month = log.as_string().split("\n")[4].split(", ")[1].split(" ")[:2]

    if month == "Sep":
        month = "09"
    else:
        raise NotImplementedError

    path_new = path.with_name(f"sp-pos-quot-dep-2020-{month}-{day}-19h15.csv")
    os.rename(path, path_new)

    print(f"copy {path_new.name} in data/sp-pos-quot-dep.csv")
    copyfile(path_new, data / "sp-pos-quot-dep.csv")

    return path, log


if __name__ == "__main__":
    path, log = download()
