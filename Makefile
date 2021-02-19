.PHONY: all
all: clean test

.PHONY: clean
clean: clean-pyc

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

test:
	pytest -v --cov=blaster tests
