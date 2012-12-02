#!/usr/bin/env python

import sys
import test_func

import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import astor

import subprocess

def CheckArgs():

    func = dir(test_func)
    check = 0

    if len(sys.argv) != 2:
        print "Please specify exactly one function as argument."
        print "List of available functions: " + str(func)
        sys.exit()

    for i in func:
        if i == sys.argv[1]:
            check += 1

    if check == 0:
        print "Pick a function from the list below."
        print "List of available functions: " + str(func)
        sys.exit()

    func_name = sys.argv[1]

    return func_name

def CallAstor(func_name):

    function = getattr(test_func,func_name) 

    func_ast = astor.codetoast(function)

    # make sure to call this from the test directory
    # otherweise need to fix the path here
    filename = str(function.__name__ +'.java')
    f = open(filename, 'w')

    # activate to print AST again
    print(astor.dump(func_ast))
    print>>f, astor.to_source(func_ast, function.__name__)

    return filename

test = CheckArgs()
name = CallAstor(test)

# always remove existing files before committing
# subprocess.call(['javac', name])
print "Successfully compiled code."
