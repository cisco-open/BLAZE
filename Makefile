#!/bin/bash
build:
	echo "Building local development environment"
	curl https://pyenv.run | bash
	pyenv install -v 3.9.16
	pyenv virtualenv 3.9.16 venv
	pyenv activate venv

install:
	echo "Installing dependencies"
	pip install -r requirements.txt
	cd /client && npm install

test:
	echo "Running unit tests"
	pytest
	echo "Running linter"
	flake8 --ignore=E501

frontend-a:
	BUILD_TYPE = debug    
	echo "Running frontend $(framework)"
	ifeq ($(BUILD_TYPE), debug) 
		CFLAGS := -g
	else
		CFLAGS := -O2
	endif
server:
	echo "Running summarization model $(yaml)"
	python run_backend.py $(yaml)


