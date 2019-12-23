.PHONY: all
all: clean tests

.PHONY: clean
clean: clean-pyc clean-tox clean-code-coverage

.PHONY: clean-code-coverage
clean-code-coverage:
	rm -rf .coverage
	rm -rf tests/coverage

.PHONY: clean-packaging
clean-packaging:
	rm -rf *.egg*

.PHONY: clean-tox
clean-tox:
	rm -rf .tox

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

tests: clean-code-coverage clean-tox
	tox -e py27

tests-py27: clean-code-coverage clean-tox
	tox -e py27

tests-py36: clean-code-coverage clean-tox
	tox -e py36
