TEST_JUST := tests/task_math

install:
	poetry install

codegen:
	playwright codegen http://localhost:8000

headed-test:
	pytest --headed --slowmo 2000

lint:
	poetry run flake8

test:
	pytest

just-test:
	pytest $(TEST_JUST)

check: lint test