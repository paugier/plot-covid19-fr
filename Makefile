
launch:
	voila plot_covid19.ipynb

install-dep:
	pip install -r requirements.txt

download:
	python plot_covid19_fr/download_files.py
	hg st

black:
	black -l 82 .
