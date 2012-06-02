from super3 import super3
import inspect
import time

def super_proxy(self, type):
    py_super = super(type, self)
    my_super = super3(caller=inspect.currentframe().f_back)

    assert py_super.__str__() == my_super.__str__() \
            or (py_super.__self_class__ == my_super.__self_class__ and \
           py_super.__self__ == my_super.__self__ and \
           py_super.__thisclass__ == my_super.__thisclass__)

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

    def super_time(cls):
        b = cls()
        N = 50000
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
        
        print (e-s), (e-s)/(N*U)
        return (e-s), N*U

    py = super_time(pyB)
    myI = super_time(myImplicitB)
    myE = super_time(myExplicitB)

    print "implicit is", myI[0]/py[0], "times slower than normal super()"
    print "explicit is", myE[0]/py[0], "times slower than normal super()"

speed()    
