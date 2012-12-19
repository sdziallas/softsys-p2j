Description:
Python to Java Translator for Olin College's Software Systems course.

Team Members:
Pierre Alsina
Sebastian Dziallas
Mandy Korpusik
Pati Martin Vicente
Lillian Tseng

Copyright 2012
License: Creative Commons Attribution-ShareAlike 3.0


The code for visiting the AST nodes to translate Python to Java 
is in astor/codegen.py.

The test code is in test/test.py. Run it using this command:

	python test.py [function name]

where the function name is the name of one of the functions in 
test_func.py. The resulting Java code will be saved in the test 
folder.