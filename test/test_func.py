#!/usr/bin/env python

import sys
import os
import string
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import astor

def TestMe(x, y, width=10, foo=None):
    from foo.bar.baz.murgatroyd import sally as bob

    a.b = c.d + x.y.z.a.b
    m.n = q = (w.w, x.x.y.y) = f(x.x.y.z)

def SimpleTest(i,j):
    '''Input: int i, int j'''
    # i = 1.2
    # j = 4
    if i==1:
        print 'A match! %i %j' % i, j
    print 'A match!'

def IfElseTest(i, j):
    '''Input: int i, int j'''
    '''Output: bool'''
    if i > j:
        print "i is greater than %i" % j
        return True
    elif i < j:
        print "i is less than %i" %j
        return False     
    else:
        print "They're equal"
        return True

def PrintTest():
  var = 'world'
  print 'hello %var' % var
  i = 1
  j = 4
  if i==1:
    print '%i and %j' % i, j
  print 'A match!'
  # different ways of printing
  print "The square root of "
  print i, ' is'
  print '%i is' % i
  # testing mod
  k = 10%4
  print k
  # this is currently not working
  text = "This is 100%."
  print text

def ReturnTest(i,j):
    '''Input: int i, int j'''
    '''Output: float'''
    return i - j

def DictTest():
    newDict = {1:2}
    newDict['dude'] = 2
    
def ListTest():
    stack = [3, 4, "Hello"]
    newDict = {1:2}
    stack2 = [2,4]
    
    stack.append(6)
    stack.append(7)
    stack2.pop(1)
    stack.insert(2, "world")
    var = 2
    s = "string"
   
    newDict['dude'] = 2
    print stack
    stack.pop()
    stack.pop()
    stack.pop(0)
    print stack
    print stack2
