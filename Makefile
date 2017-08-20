.PHONY: clean-pyc clean clean-tests tox

all: clean-pyc clean clean-tests

clean-all: clean-pyc clean clean-tests

tests: clean-tests tox

clean:
	rm -rf *.egg*
	rm -rf .cache

clean-pyc:
	find . -name '*.pyc' -exec rm -f {} +
	find . -name '*.pyo' -exec rm -f {} +
	find . -name '*~' -exec rm -f {} +

clean-tests:
	rm -rf .coverage
	rm -rf .tox
	rm -rf tests/coverage

tox:
	tox
