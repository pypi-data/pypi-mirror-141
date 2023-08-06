.PHONY: clean install data requirements

# init

SHELL=/bin/bash
PROJECT_NAME=batchutils
CONDA_BASE:=$(shell conda info --base)

# install

update-pip:
	pip install -U setuptools wheel twine

install: clean update-pip
	pip install -e .

install-setup: clean update-pip
	python setup.py install

install-reqs:
	pip install --upgrade --no-deps --force-reinstall -r requirements.txt

install-dev:
	pip install --upgrade --no-deps --force-reinstall -r requirements-dev.txt

freeze-reqs: install-requirements
	pip freeze > requirements.txt

version:
	@python -c 'import batchutils; print(batchutils.__version__)'

lib-version:
	@python -c 'import $(NAME); print($(NAME).__version__)'

hail-version:
	@python -c 'import hail; print(hail.version())'

# clean

clean: clean-py

clean-py: clean-build clean-pyc clean-test

clean-pyc:
	find . -name '*.py[co]' -exec rm -f {} +
	find . -name '*~' -exec rm -f {} +
	find . -name '__pycache__' -exec rm -fr {} +

clean-build:
	rm -fr build/
	rm -fr dist/
	rm -fr .eggs/
	find . -name '*.egg-info' -exec rm -fr {} +
	find . -name '*.egg' -exec rm -f {} +

clean-test:
	rm -fr .tox/
	rm -f .coverage
	rm -fr htmlcov/

# env

act:
	@(. $(CONDA_BASE)/etc/profile.d/conda.sh && conda activate batchutils)

create-env:
	conda create -y --name $(PROJECT_NAME) python=3.7.4 jupyter=1.0.0

remove-env: clean
	( source $(shell conda info --base)/etc/profile.d/conda.sh && \
		conda deactivate && \
		conda remove --name $(PROJECT_NAME) --all )

install-version:
	versioneer install

# build

build: clean-py
	python setup.py sdist bdist_wheel
	twine check dist/*

upload-test:
	twine upload --repository testpypi dist/*

upload:
	twine upload dist/*

# buildx
buildx:
	python src/buildx.py