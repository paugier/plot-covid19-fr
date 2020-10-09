
download:
	python plot_covid19_fr/download_files.py

black:
	black -l 82 .

install-dep:
	pip install -r requirements.txt

launch:
	voila plot_covid19.ipynb
