
from pathlib import Path
from urllib.request import urlretrieve

here = Path(__file__).absolute().parent

data = here / "data"

data.mkdir(exist_ok=True)

address = "https://www.data.gouv.fr/fr/datasets/r/406c6a23-e283-4300-9484-54e78c8ae675"


def download():
    return urlretrieve(address, data / "tmp.csv")


path, log = download()
