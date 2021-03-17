@PHONY: test check

test:
	python -m pytest -vvxs src/tests/

testwip:
	python -m pytest -vvxs -m wip src/tests/

check:
	twine check --strict dist/*
