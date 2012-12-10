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

def ClassTest():

    class BankAccount(object):
        def __init__(self, initial_balance=0):
            self.balance = initial_balance
        def deposit(self, amount):
            self.balance += amount
        def withdraw(self, amount):
            self.balance -= amount
        def overdrawn(self):
            return self.balance < 0

def IfElseTest(i, j):
    '''Input: int i, int j'''
    '''Output: boolean'''
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
    newDict[3] = 4
    x = newDict[3]
    y = newDict.keys()
    z = newDict.values()
    x = len(newDict)
    del newDict[3]

    for value in newDict.values():
        print value
    
def ListTest():
    stack = [3, 4, "Hello"]
    stack.append(6)
    stack.append(7)


    stack.pop(1)

    stack.insert(2, "world")
    var = 2
    s = "string"
   
    print stack
    stack.pop()
    stack.pop()
    stack.pop(0)
    print stack
    
    newDict = {1:2}
    newDict[3] = stack
    newDict[4] = 2
    newDict[5] = "Hello"
    x = newDict[3]
    print stack

def ForTest():
    for i in range(10):
      print('Hello')
      
    string = "Hello World"
    for letter in string:
      print(letter)
      
    items = ['red', 'orange', 'yellow', 'green']
    for item in items:
      print(item)
      
    for item in ['red', 'orange', 'yellow', 'green']:
      print(item)
    #TEST NOT WORKING YET
    x = 0       # Exercise Play Computer Loop
    y = 1                  
    for n in [5, 4, 6]:     
      x = x + y*n         
      y = y + 1                  
    print(x)
    
    for a in range(0, 3):
      print "We're on time %a" % (a)

def WhileLoop():
    i = True
    while i:
        i = False
