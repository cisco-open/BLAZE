build:
	echo "Building local development environment"
	curl https://pyenv.run | bash
	pyenv install -v 3.9.16
	pyenv virtualenv 3.9.16 venv
	pyenv activate venv

install:
	echo "Installing dependencies"
	pip install -r requirements.txt

test:
	echo "Running unit tests"
	pytest
	echo "Running linter"
	flake8 --ignore=E501

run_search:
	echo "Running search model"
	python run_backend.py yaml/01_search_custom.yaml

run_summ:
	echo "Running summarization model"
	python run_backend.py yaml/05_summary_datasets.yaml
