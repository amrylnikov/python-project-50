install:
	poetry install

publish:
	poetry publish --dry-run

pakage-install:
	python3 -m pip install --user dist/*.whl

reinstall:
	pip install --user --force-reinstall dist/*.whl

gendiff:
	poetry run gendiff

test:
	poetry run pytest

test-coverage:
	poetry run pytest --cov=hexlet_python_package --cov-report xml

lint:
	poetry run flake8 hexlet_code

selfcheck:
	poetry check

build:
	poetry build

.PHONY: install test lint selfcheck check build