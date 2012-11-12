#!/usr/bin/env python

import sys
import os
import string
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import astor

def TestMe1(x, y, width=10, foo=None):
    from foo.bar.baz.murgatroyd import sally as bob

    a.b = c.d + x.y.z.a.b
    m.n = q = (w.w, x.x.y.y) = f(x.x.y.z)

def __privatefunc():
	print "Hello"

def __SimpleTest():
    i = 1.2
    j = 4
    if i==1:
        print 'A match! %i %j' % i, j
    print 'A match!'

def IfElseTest():
    i = 5
    if i == 5:
        print "number 5 %i" % i
    elif i == 3:
		print "number 3"     
    else:
        print "something else" 

func_ast = astor.codetoast(__SimpleTest)

print(astor.dump(func_ast))
print(__SimpleTest.__name__ + '\n')
print(astor.to_source(func_ast, __SimpleTest.__name__))
