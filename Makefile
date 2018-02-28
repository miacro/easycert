SHELL=/bin/bash
MAKE=make --no-print-directory

install:
	python setup.py install --user

test:
	python -m unittest discover ./easycert/test

uninstall:
	pip uninstall easycert

.PHONY:
	install uninstall
