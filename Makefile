.PHONY: all
all: clean tests

.PHONY: clean
clean: clean-pyc clean-code-coverage

.PHONY: clean-code-coverage
clean-code-coverage:
	rm -rf .coverage
	rm -rf tests/coverage

.PHONY: clean-packaging
clean-packaging:
	rm -rf *.egg*

.PHONY: clean-pyc
clean-pyc:
	find . -name '*.pyc' -exec rm -f {} +
	find . -name '*.pyo' -exec rm -f {} +

.PHONY: bump-major
bump-major:
	bumpversion major --commit

.PHONY: bump-minor
bump-minor:
	bumpversion minor --commit

.PHONY: bump-patch
bump-patch:
	bumpversion patch --commit

tests: clean-code-coverage
	nosetests -v --with-ignore-docstrings --with-coverage --cover-package blaster --cover-html --cover-html-dir tests/coverage
