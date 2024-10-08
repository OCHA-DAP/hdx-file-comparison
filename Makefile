SHELL := /bin/bash
install:
	pip install -e .
lint:
	black . --check
	flake8 --config=config/.flake8 src/
	pylint --rcfile=config/.pylintrc src/ || true
unit_tests:
	pytest --cov=hdx_file_comparison --cov-config=config/.coveragerc tests/
publish:
	rm -rf build dist *.egg-info
	hatch build
	hatch publish