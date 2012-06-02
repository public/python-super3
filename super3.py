"""
Super3 is Python 3's super() for Python 2
"""

import sys

class super3(super):
    __cache__ = {}

    def __init__(self, *args, **kwargs):
        super(super3, self).__init__(*self.__args__(*args, **kwargs))

    def __new__(cls, *args, **kwargs):
        return super(super3, cls).__new__(cls, *cls.__args__(*args, **kwargs))

    @classmethod
    def __args__(cls, *args, **kwargs):
        if not args:
            # Find the caller and work out the class it was defined in (not what it was bound to!)
            caller = kwargs.get('caller') or sys._getframe().f_back.f_back
            caller_code = caller.f_code

            if caller_code not in cls.__cache__:
                caller_self = caller.f_locals[caller.f_code.co_varnames[0]]
                caller_name = caller_code.co_name
                
                # type(caller_self) may not be the class that the caller is actually defined
                # in so instead we search through the MRO to find the class which owns this code object
                
                mro_funcs = ((cls, cls.__dict__.get(caller_name)) for cls in type(caller_self).__mro__)
                caller_class = next((cls for cls, func in mro_funcs
                                            if func and func.func_code == caller_code))
            else:
                caller_class = cls.__cache__[caller_code]
            return caller_class, caller_self
        else:
            return args
