python-super3
=============

super3 is Python3's [PEP3135](http://www.python.org/dev/peps/pep-3135/) magic super() for Python2 and also Python3.

Unlike previous implementations (e.g. http://code.activestate.com/recipes/286195-selfsuper/)
of the implicit super() pattern this one is syntax compatible with Python 3 if
you ```from super3 import super3 as super```.

More than super()
-----------------

Infact, we go one further than Python3's super(). It even works inside a decorator like this

```
def with_super_result(func):
    def decorated(self, *args, **kwargs):
        return func(self, getattr(super(), func.__name__)())
    return decorated
```

Tested in CPython 2.7.3 (~20x slower than normal) and PyPy 1.8-2.7.2 (~100x
slower than normal.)

Python3 Support
---------------

Python3 is also supported but it uses entirely the same code as Python2.

Really it should be taking the shortcut of grabbing the `__cell__` freevar out of `func.__closure__`.


Copying
-------

This library is licensed under the LGPLv3 or later as defined in the COPYING file.
