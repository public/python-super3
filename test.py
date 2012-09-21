from super3 import more_super3 as super3
from super3 import callable_super3
import inspect
import time
import sys
def super_proxy(self, type):
    py_super = super(type, self)
    my_super = super3(caller=inspect.currentframe().f_back)

    assert py_super.__str__() == my_super.__str__() \
            or (py_super.__self_class__ == my_super.__self_class__ and \
           py_super.__self__ == my_super.__self__ and \
           py_super.__thisclass__ == my_super.__thisclass__)

    return my_super

def with_super_result(func):
    def decorated(self, *args, **kwargs):
        s = super3()
        r = getattr(s, func.__name__)()
        return func(self, r)
    return decorated

class A(object):
    def f(self):
        return A

class A2(object):
    def f(self):
        return A2

class A3(A):
    @with_super_result
    def f(self, super):
        return A3

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
        r = super_proxy(self, G).f()
        assert r == A
        return F.f(self)

class H(G):
    @with_super_result
    def f(self, super):
        return H

class I(H):
    @with_super_result
    def f(self, super):
        assert super == H
        return I

class J(A):
    def f(self):
        r = callable_super3()()
        return r

class K(G):
    def f(self):
        return callable_super3()()

import random

classes = [J, K, A3, I, H, A, A2, B, C, D, E, F, G]
random.shuffle(classes)
print(classes)

for cls in classes:
    print((cls, cls().f()))

def speed():
    class A(object):
        def f(self):
            return A, self

    class myImplicitB(A):
        def f(self):
            return super3().f()

    class myExplicitB(A):
        def f(self):
            return super3(myExplicitB, self).f()

    class pyB(A):
        def f(self):
            return super(pyB, self).f()

    class myDecoratedB(A):
        @with_super_result
        def f(self, result):
            return self

    def super_time(cls):
        b = cls()
        N = 10000
        U = 10
        s = time.time()
        for i in range(1, N):
            b.f()
            b.f()
            b.f()
            b.f()
            b.f()
            b.f()
            b.f()
            b.f()
            b.f()
            b.f()

        e = time.time()
        
        print((e-s), (e-s)/(N*U))
        return (e-s), N*U

    py = super_time(pyB)
    myI = super_time(myImplicitB)
    myE = super_time(myExplicitB)
    myD = super_time(myDecoratedB)

    print("implicit is", myI[0]/py[0], "times slower than normal super()")
    print("explicit is", myE[0]/py[0], "times slower than normal super()")
    print("decorated is", myD[0]/py[0], "times slower than normal super()")

speed()    
