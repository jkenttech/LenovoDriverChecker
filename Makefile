run:
	.venv/bin/python main.py $(serial)

install:
	python -m venv .venv
	.venv/bin/python -m pip install beautifulsoup4
	.venv/bin/python -m pip install selenium

clean:
	rm -r driver_csv

