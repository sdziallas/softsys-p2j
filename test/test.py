#!/usr/bin/env python

import sys
import test_func

import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import astor

def CheckArgs():

    func = dir(test_func)
    check = 0

    print "List of available functions: " + str(func)

    if len(sys.argv) != 2:
        print "Please specify exactly one function as argument."
        sys.exit()

    for i in func:
        if i == sys.argv[1]:
            check += 1

    if check == 0:
        print "Pick a function from the list above."
        sys.exit()

    func_name = sys.argv[1]

    return func_name

def CallAstor(func_name):

    function = getattr(test_func,func_name) 

    func_ast = astor.codetoast(function)

    print(astor.dump(func_ast))
    print(function.__name__ + '\n')
    print(astor.to_source(func_ast, function.__name__))

test = CheckArgs()
CallAstor(test)
