v=venv\Scripts\activate

black:
	$(v) && black .

isort:
	$(v) && isort .

flake8:
	$(v) && flake8 .

format:
	$(v) && black . && isort .

test:
	$(v) && pytest --disable-warnings src\tests

cover:
	$(v) && coverage run -m pytest -q --no-header --no-summary src\tests && coverage report
