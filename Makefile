TEST_JUST := tests/task_math

install:
	poetry install

codegen:
	playwright codegen http://localhost:8000

state:
	poetry run python -m tests.auth.save_auth_state

headed-test:
	pytest --headed --slowmo 2000

lint:
	poetry run flake8

test:
	poetry run pytest

just-test:
	pytest $(TEST_JUST)

check: lint test