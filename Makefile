@PHONY: test check

test:
	python -m pytest -vvxs tests/

testwip:
	python -m pytest -vvxs -m wip tests/

check:
	python ./setup.py check -mrs
