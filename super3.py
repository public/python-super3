"""
Super3 is Python 3's super() for Python 2
"""

import inspect

class super3(super):
    def __init__(self, *args, **kwargs):
        if not args:
            # Find the caller and work out the class it was defined in (not what it was bound to!)
            caller = kwargs.get('caller') or inspect.currentframe().f_back
            caller_args = inspect.getargvalues(caller)
            caller_self = caller_args.locals[caller_args.args[0]]
            caller_code = caller.f_code
            caller_name = caller_code.co_name
            
            # type(caller_self) may not be the class that the caller is actually defined
            # in so instead we search through the MRO to find the class which owns this code object
            
            mro_funcs = ((cls, cls.__dict__.get(caller_name)) for cls in type(caller_self).__mro__)
            caller_class = next((cls for cls, func in mro_funcs
                                        if func and func.func_code == caller_code))
            
            return super.__init__(self, caller_class, caller_self) 
        else:
            return super.__init__(self, *args)

