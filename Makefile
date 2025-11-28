
.PHONY: install data lint retention notebook test clean

PYTHON ?= python

ifeq ($(OS),Windows_NT)
	VENV_PY := .venv/Scripts/python.exe
else
	VENV_PY := .venv/bin/python
endif

install:
	$(PYTHON) -m venv .venv
	$(VENV_PY) -m pip install --upgrade pip
	$(VENV_PY) -m pip install -r requirements.txt

data:
	$(VENV_PY) src/generate_data.py

lint:
	$(VENV_PY) -m flake8 src tests

retention:
	$(VENV_PY) src/retention.py --input data/orders.csv --output outputs/retention.csv

notebook:
	$(VENV_PY) -m jupyter lab

test:
	$(VENV_PY) -m pytest -q

clean:
	$(PYTHON) - <<-'PY'
	import shutil
	from pathlib import Path
	for target in [".venv", "outputs", "__pycache__", ".ipynb_checkpoints"]:
	    path = Path(target)
	    if path.exists():
	        shutil.rmtree(path, ignore_errors=True)
	PY
