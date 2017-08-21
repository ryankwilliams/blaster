.PHONY: clean tests tests-py27 tests-py36

all: clean tests

clean:
	rm -rf *.egg*
	rm -rf .cache
	find . -name '*.pyc' -exec rm -f {} +
	find . -name '*.pyo' -exec rm -f {} +
	find . -name '*~' -exec rm -f {} +
	rm -rf .coverage
	rm -rf .tox
	rm -rf tests/coverage

tests:
	rm -rf .coverage
	rm -rf .tox
	rm -rf tests/coverage
	tox

tests-py27:
	rm -rf .coverage
	rm -rf .tox
	rm -rf tests/coverage
	tox -e py27

tests-py36:
	rm -rf .coverage
	rm -rf .tox
	rm -rf tests/coverage
	tox -e py36
