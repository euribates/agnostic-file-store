@PHONY: test check

test:
	python -m pytest -vvxs tests/

check:
	python ./setup.py check -mrs
