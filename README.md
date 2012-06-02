python-super3
=============

super3 is Python3's [PEP3135](http://www.python.org/dev/peps/pep-3135/) magic super() for Python2.

Unlike previous implementations (e.g. http://code.activestate.com/recipes/286195-selfsuper/)
of the implicit super() pattern this one is syntax compatible with Python 3 if
you from ```super3 import super3 as super```.

Tested in CPython 2.7.3 (~20x slower than normal) and PyPy 1.8-2.7.2 (~100x
slower than normal.) There are some bytecode hacks that could speed CPython up
a bit...


