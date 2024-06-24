.PHONY: setup
setup:
	pipenv sync --dev
	pipenv run pre-commit install
	pipenv run pre-commit run --all-files
	pipenv run pytest

.PHONY: precommit
precommit:
	pipenv run pre-commit run --all-files
