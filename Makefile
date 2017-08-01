.PHONY: clean-pyc clean

all: clean-pyc clean

clean-all: clean-pyc clean

clean:
	rm -rf blaster/*.egg
	rm -rf blaster/*.egg-info
	rm -rf .cache

clean-pyc:
	find . -name '*.pyc' -exec rm -f {} +
	find . -name '*.pyo' -exec rm -f {} +
	find . -name '*~' -exec rm -f {} +
