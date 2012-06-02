from super3 import super3
import inspect

def super_proxy(self, type):
    py_super = super(type, self)
    my_super = super3(caller=inspect.currentframe().f_back)

    assert py_super.__self_class__ == my_super.__self_class__ and \
           py_super.__thisclass__ == my_super.__thisclass__ and \
           py_super.__self__ == my_super.__self__

    return my_super

class A(object):
    def f(self):
        return A

class A2(object):
    def f(self):
        return A2

class B(A):
    pass

class C(B):
    def f(self):
        return super_proxy(self, C).f()

class D(C, A2):
    def f(self):
        return C.f(self)

class E(C, A, A2):
    pass

class F(E):
    def f(self):
        return super_proxy(self, F).f()

class G(F, E, A):
    def f(self):
        super_proxy(self, G).f()
        return F.f(self)

for cls in (A, A2, B, C, D, E, F, G):
    print cls, cls().f()

