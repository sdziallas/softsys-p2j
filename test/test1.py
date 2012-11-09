#!/usr/bin/env python

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import astor

def TestMe1(x, y, width=10, foo=None):
    from foo.bar.baz.murgatroyd import sally as bob

    a.b = c.d + x.y.z.a.b
    m.n = q = (w.w, x.x.y.y) = f(x.x.y.z)

def SimpleTest():
    i = 1.2
    if i==1:
        print 'A match!'

def IfElseTest():
    i = 5
    if i == 5:
        print("number 5")
    else:
        print("something else")        
    
func_ast = astor.codetoast(IfElseTest)
print(astor.dump(func_ast))
print('\n')
print(astor.to_source(func_ast))
