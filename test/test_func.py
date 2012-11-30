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
    '''Output: '''
    # i = 1.2
    # j = 4
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
    return 1

def PrintTest():
  i = 1.2
  var = 'world'
  j = 4
  if i==1:
    print '%i and %j' % i, j
  print 'A match!'
  print 'and %var %j_p is'
  print 'hello %var' % var
  print "The square root of "
  print i
  print i, ' is'
  print '%i is' % i
  print " is "
  print "."
  print "The square root of %i is %r" % i, r 

  print "the square is ", i

def ModTest():
    i = 10%4
    print i
    text = "This is 100% tested."
    print text

def ReturnTest(i,j):
    '''Input: int i, int j'''
    '''Output: float'''
    x = "hello" + " goodbye"
    return i - j

def DictTest():
    print 'Hello'
    newDict = {}
    
def listTest():
    stack = [3, 4, "Hello"]
   # stack.append(6)
   # stack.append(7)
   # stack
   # stack.pop()
   #stack.pop()
   # stack
