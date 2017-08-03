.PHONY: clean-pyc clean

all: clean-pyc clean

clean-all: clean-pyc clean

clean:
	rm -rf *.egg*
	rm -rf .cache

clean-pyc:
	find . -name '*.pyc' -exec rm -f {} +
	find . -name '*.pyo' -exec rm -f {} +
	find . -name '*~' -exec rm -f {} +
