"""
Super3 is Python 3's super() for Python 2
"""

import inspect

class super3(super):
    def __init__(self, *args, **kwargs):
        if not args and not kwargs:
            # Find the caller and work out the class it was defined in (not what it was bound to!)
            caller = inspect.currentframe().f_back
            caller_args = inspect.getargvalues(caller)
            caller_self = caller_args.locals[caller_args.args[0]]
            caller_func = getattr(caller_self, caller.f_code.co_name)

            return super.__init__(self, caller_func.im_class, caller_self) 
        else:
            return super.__init__(self, *args, **kwargs)

