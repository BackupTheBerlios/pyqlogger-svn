__revision__ = "$Id$"

install:
	python setup.py install
	
dist:
	python setup.py sdist

clean:
	python setup.py clean
	find . -type f -name '*~' -exec rm {} \;
	find . -type f -name '*.pyc' -exec rm {} \;

mrproper: clean
	rm -rf build
	rm -rf dist

rpm:
	python setup.py bdist_rpm
