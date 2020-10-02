
download:
	python plot_covid19_fr/download_files.py

black:
	black -l 82 *.py

install-dep:
	pip install -r requirements.txt
