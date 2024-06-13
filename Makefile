.PHONY: setup
setup:
	pipenv sync --dev
.PHONY: precommit
precommit:
	pipenv run pre-commit run --all-files
