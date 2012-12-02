# -*- coding: utf-8 -*-
"""

This module converts an AST into Python source code.

Original code copyright (c) 2008 by Armin Ronacher and
is distributed under the BSD license.

It was derived from a modified version found here:

    https://gist.github.com/1250562

This version is being adopted for a Python to Java
translator for the Software Systems course at Olin College.

"""

import ast
import string
from astor.misc import ExplicitNodeVisitor
from astor.misc import get_boolop, get_binop, get_cmpop, get_unaryop

global returnsNone
returnsNone = False

def is_public(name):
    if name[0:2] == '__' or name [0:1] == '_':
	    return False
    else:
        return True

def to_source(node, fname, indent_with=' ' * 4, add_line_information=False):
    """This function can convert a node tree into java sourcecode.
    This is useful for debugging purposes, especially if you're dealing with
    custom asts not generated by python itself.

    It could be that the sourcecode is evaluable when the AST itself is not
    compilable / evaluable.  The reason for this is that the AST contains some
    more data than regular sourcecode does, which is dropped during
    conversion.

    Each level of indentation is replaced with `indent_with`.  Per default this
    parameter is equal to four spaces as suggested by PEP 8, but it might be
    adjusted to match the application's styleguide.
    If `add_line_information` is set to `True` comments for the line numbers
    of the nodes are added to the output.  This can be used to spot wrong line
    number information of statement nodes.

	fname will be put into the public class declaration at the very beginning of the translated code so that the java sourcecode compiles nicely.
    """

    generator = SourceGenerator(indent_with, add_line_information)
    generator.write("import java.util.*;")
    generator.newline()

    if is_public(fname):
        generator.write("public class "+ fname + "{")
    else:
        # Does not currently handle _names or __names differently.
        # Assumes __names - formatted variables.
		generator.write("private class " + fname[2:] + "{")

    generator.indentation += 1
    generator.visit(node)
    generator.indentation -= 1
    generator.write("\n}");
    return ''.join(str(s) for s in generator.result)


def enclose(enclosure):
    def decorator(func):
        def newfunc(self, node):
            self.write(enclosure[0])
            func(self, node)
            self.write(enclosure[-1])
        return newfunc
    return decorator


class SourceGenerator(ExplicitNodeVisitor):
    """This visitor is able to transform a well formed syntax tree into python
    sourcecode.  For more details have a look at the docstring of the
    `node_to_source` function.
    """

    def __init__(self, indent_with, add_line_information=False):
        self.result = []
        self.indent_with = indent_with
        self.add_line_information = add_line_information
        self.indentation = 0
        self.new_lines = 0

    def write(self, *params):
        for item in params:
            if isinstance(item, ast.AST):
                self.visit(item)
            elif hasattr(item, '__call__'):
                item()
            elif item == '\n':
                self.newline()
            else:
                if self.new_lines:
                    if self.result:
                        self.result.append('\n' * self.new_lines)
                    self.result.append(self.indent_with * self.indentation)
                    self.new_lines = 0
                self.result.append(item)

    def trans_Expr(self, node, input_output):
        # Translates docstrings to fix the input variable and return variable
        # types.

        if input_output == 'input':
            for stmt in node.body:
                if 'Expr' in repr(stmt):
                    if "Input: " in ast.literal_eval(stmt.value):
                        return_string = ast.literal_eval(stmt.value)
                        return_string = return_string[7:]
                        return return_string
        else:
            for stmt in node.body:
                if 'Expr' in repr(stmt):
                    if "Output: " in ast.literal_eval(stmt.value):
                        return_string = ast.literal_eval(stmt.value)
                        return_string = return_string[8:]
                        return return_string


    def conditional_write(self, *stuff):
        if stuff[-1] is not None:
            self.write(*stuff)

    def newline(self, node=None, extra=0):
        self.new_lines = max(self.new_lines, 1 + extra)
        if node is not None and self.add_line_information:
            self.write('# line: %s' % node.lineno)
            self.new_lines = 1

    def body(self, statements):
        self.indentation += 1
        for stmt in statements:
            self.visit(stmt)
        self.indentation -= 1

    def else_body(self, elsewhat):
        if elsewhat:
            self.write('\n', 'else{')
            self.body(elsewhat)
            self.newline(elsewhat)
            self.write('}')

    def body_or_else(self, node):
        self.body(node.body)
        self.else_body(node.orelse)

    def signature(self, node):
        want_comma = []
        def write_comma():
            if want_comma:
                self.write(', ')
            else:
                want_comma.append(True)

        def loop_args(args, defaults):
            padding = [None] * (len(args) - len(defaults))
            for arg, default in zip(args, padding + defaults):
                self.write(write_comma, arg)
                self.conditional_write('=', default)


        loop_args(node.args, node.defaults)
        self.conditional_write(write_comma, '*', node.vararg)
        self.conditional_write(write_comma, '**', node.kwarg)

        kwonlyargs=getattr(node, 'kwonlyargs', None)
        if kwonlyargs:
            if node.vararg is None:
                self.write(write_comma, '*')
            loop_args(kwonlyargs, node.kw_defaults)

    def write_inputs(self, node):
        input_vars = self.trans_Expr(node, 'input')
        if input_vars != None:
            self.write(input_vars)

    def statement(self, node, *params, **kw):
        self.newline(node)
        self.write(*params)

    def decorators(self, node, extra):
        self.newline(extra=extra)
        for decorator in node.decorator_list:
            self.statement(decorator, '@', decorator)

    # Change in order to get only the first string
    def comma_list(self, items, trailing=False):
        for idx, item in enumerate(items):
            if idx:
                self.write(', ')
            self.visit(item)
        if trailing:
            self.write(',')
            
    # Change in order to get only the first string
    def comma_list_print(self, items, trailing=False):
        #print 'COMMA'
        moduleDetected = False
        firstItem = True
        for idx, item in enumerate(items):
            #print 'ITEM', type(item)
            if type(item) is ast.BinOp:
              #print item.op
              #if item.op == 'Mod':
              #print 'MODULE DETECTED'
              moduleDetected = True
            if moduleDetected:
              if firstItem:
                self.write(item)
                firstItem = False
            else:
              if firstItem:
                self.write(item)
                firstItem = False
              else:
                self.write(' + ')
                self.visit(item)

    # Statements

    def check_Type(self, node):
        # TODO: this does not work for things like 10%4
        ValueType = type(ast.literal_eval(node.value))
        print ValueType
        if ValueType == int:
            return 'int '
        elif ValueType == float:
			# In Java, 'float' requires 'f' to appear after the number,
			# but 'double' does not.
            return 'double '
        elif ValueType == str:
            return 'String '
        elif ValueType == bool:
            return 'Bool'
        elif ValueType == list:
            return 'ArrayList '

    def visit_Assign(self, node):
        # TODO: this is not working for things like 10%4
        self.newline(node)
        if type(node.value) == ast.List:
            self.write('ArrayList ');
            self.write(node.targets[0].id)
            self.write(' = ')
            self.write('new ArrayList();')
            for i in range(0,len(node.value.elts)):
              self.newline(node)
              self.write(node.targets[0].id)
              self.write('.add(')
              self.write(node.value.elts[i])
              self.write(');')
        else:
            try:
                node_type = self.check_Type(node)
                self.write(node_type)
            except:
                self.write("// FIX TYPE OF ASSIGNED VARIABLE")
                self.newline(node)
                self.write("int ")
            for target in node.targets:
                self.write(target, ' = ')
                self.visit(node.value)
            self.write(';')


    def visit_AugAssign(self, node):
        self.statement(node, node.target, get_binop(node.op, ' %s= '), node.value)

    def visit_ImportFrom(self, node):
        self.statement(node, 'from ', node.level * '.' , node.module, ' import ')
        self.comma_list(node.names)

    def visit_Import(self, node):
        self.statement(node, 'import ')
        self.comma_list(node.names)

    def visit_Expr(self, node):
        self.newline()
        self.write('/*')
        self.statement(node)
        self.generic_visit(node)  
        self.newline()      
        self.write('*/')

    def visit_FunctionDef(self, node):
        global returnsNone
        self.decorators(node, 1)

        return_type = None        

        # determine the function's return type
        for ast_object in node.body:
            print repr(ast_object)
            if 'Return' in repr(ast_object):
                try:
                    # Handles simple case of returning straight integers,
                    # strings, etc.
                    return_type = self.check_Type(ast_object)
                    
                    # Handles return_type of None
                    if return_type == None:
                        return_type = 'void '
                        returnsNone = True
                    incorrect_type = False
                except:
                    # Handles return types of expressions and variables
                    # The docstring must have "Input: " and "Output: " in 
                    # different expressions
                    return_type = self.trans_Expr(node,'output') + ' '
                    incorrect_type = True

        if return_type == None:
            # There is no return type
            print "No return type"
            incorrect_type = False
            return_type = 'void '
                
        if is_public(node.name):
	        self.statement(node, 'public ' + return_type + '%s(' % node.name)
        else:
            self.statement(node, 'private ' + return_type + '%s(' % node.name[2:])
        self.write_inputs(node)
        self.write(')')
        if getattr(node, 'returns', None) is not None:
            self.write(' ->', node.returns)
        self.write('{')
        if incorrect_type:
            self.indentation += 1
            self.newline(node)
            self.write('// Fix the return type')
            self.indentation -= 1
        self.body(node.body)
        self.newline(node)
        self.write('}')

    def visit_ClassDef(self, node):
        have_args = []
        def paren_or_comma():
            if have_args:
                self.write(', ')
            else:
                have_args.append(True)
                self.write('(')

        self.decorators(node, 2)
        self.statement(node, 'class %s' % node.name)
        for base in node.bases:
            self.write(paren_or_comma, base)
        # XXX: the if here is used to keep this module compatible
        #      with python 2.6.
        if hasattr(node, 'keywords'):
            for keyword in node.keywords:
                self.write(paren_or_comma, keyword.arg, '=', keyword.value)
            self.conditional_write(paren_or_comma, '*', node.starargs)
            self.conditional_write(paren_or_comma, '**', node.kwargs)
        self.write(have_args and '):' or ':')
        self.body(node.body)

    def visit_If(self, node):
        self.statement(node, 'if ', node.test, '{')
        self.body(node.body)
        self.newline(node)
        self.write('}')
        while True:
            else_ = node.orelse
            if len(else_) == 1 and isinstance(else_[0], ast.If):
                node = else_[0]
                self.write('\n', 'else if ', node.test, '{')
                self.body(node.body)
                self.newline(node)
                self.write('}')
            else:
                self.else_body(else_)
                break


    def visit_For(self, node):
        self.statement(node, 'for ', node.target, ' in ', node.iter, ':')
        self.body_or_else(node)

    def visit_While(self, node):
        self.statement(node, 'while ', node.test, ':')
        self.body_or_else(node)

    def visit_With(self, node):
        self.statement(node, 'with ', node.context_expr)
        self.conditional_write(' as ', node.optional_vars)
        self.write(':')
        self.body(node.body)

    def visit_Pass(self, node):
        self.statement(node, 'pass')

    def visit_Print(self, node):
        # XXX: python 2.6 only
		# Modified to write 'system.out.println' instead of 'print'
        self.statement(node, "System.out.println(")
        values = node.values
        if node.dest is not None:
            self.write(' >> ')
            values = [node.dest] + node.values
        self.comma_list_print(values, not node.nl)
        self.write(");");

    def visit_Delete(self, node):
        self.statement(node, 'del ')
        self.comma_list(node.targets)

    def visit_TryExcept(self, node):
        self.statement(node, 'try:')
        self.body(node.body)
        for handler in node.handlers:
            self.visit(handler)
        self.else_body(node.orelse)

    def visit_ExceptHandler(self, node):
        self.statement(node, 'except')
        if node.type is not None:
            self.write(' ', node.type)
            self.conditional_write(' as ', node.name)
        self.write(':')
        self.body(node.body)

    def visit_TryFinally(self, node):
        self.statement(node, 'try:')
        self.body(node.body)
        self.statement(node, 'finally:')
        self.body(node.finalbody)

    def visit_Exec(self, node):
        dicts = node.globals, node.locals
        dicts = dicts[::-1] if dicts[0] is None else dicts
        self.statement(node, 'exec ', node.body)
        self.conditional_write(' in ', dicts[0])
        self.conditional_write(', ', dicts[1])

    def visit_Assert(self, node):
        self.statement(node, 'assert ', node.test)
        self.conditional_write(', ', node.msg)

    def visit_Global(self, node):
        self.statement(node, 'global ', ', '.join(node.names))

    def visit_Nonlocal(self, node):
        self.statement(node, 'nonlocal ', ', '.join(node.names))

    def visit_Return(self, node):
        global returnsNone
        if not returnsNone:
            self.statement(node, 'return')
            self.conditional_write(' ', node.value)
            self.write(';')
        returnsNone = False

    def visit_Break(self, node):
        self.statement(node, 'break')

    def visit_Continue(self, node):
        self.statement(node, 'continue')

    def visit_Raise(self, node):
        # XXX: Python 2.6 / 3.0 compatibility
        self.statement(node, 'raise')
        if hasattr(node, 'exc') and node.exc is not None:
            self.write(' ', node.exc)
            self.conditional_write(' from ', node.cause)
        elif hasattr(node, 'type') and node.type is not None:
            self.write(' ', node.type)
            self.conditional_write(', ', node.inst)
            self.conditional_write(', ', node.tback)

    # Expressions

    def visit_Attribute(self, node):
        self.write(node.value, '.', node.attr)

    def visit_Call(self, node):
        want_comma = []
        def write_comma():
            if want_comma:
                self.write(', ')
            else:
                want_comma.append(True)

        self.visit(node.func)
        self.write('(')
        for arg in node.args:
            self.write(write_comma, arg)
        for keyword in node.keywords:
            self.write(write_comma, keyword.arg, '=', keyword.value)
        self.conditional_write(write_comma, '*', node.starargs)
        self.conditional_write(write_comma, '**', node.kwargs)
        self.write(')')
        self.write(';')
		
    def visit_Name(self, node):
        self.write(node.id);

    # Change self.write(repr(node.s)) to the code below
    # in order to get "" instead of ''
    def visit_Str(self, node):
       #self.write('"')
        #self.write(node.s)
        #self.write('"')
        found = False
        string = '"'
        for char in node.s:
          if found == True and char == ' ':
            found = False
            string += ' + "'
          elif char == '%' and found == False:
            string += '" + '
            found = True
          else:
            string += char
        if found == False:
          string += '"'
        string = string.replace(' + ""', '')
        string = string.replace('"" + ', '')
        self.write(string)

    def visit_Bytes(self, node):
        self.write(repr(node.s))

    def visit_Num(self, node):
        # Hack because ** binds more closely than '-'
        s = repr(node.n)
        if s.startswith('-'):
            s = '(%s)' % s
        self.write(s)

    @enclose('()')
    def visit_Tuple(self, node):
        self.comma_list(node.elts, len(node.elts) == 1)

    @enclose('[]')
    def visit_List(self, node):
        self.comma_list(node.elts)

    @enclose('{}')
    def visit_Set(self, node):
        self.comma_list(node.elts)

    @enclose('{}')
    def visit_Dict(self, node):
        for key, value in zip(node.keys, node.values):
            self.write(key, ': ', value, ', ')


    # Take @enclose('()') in order to have only one pair of parentheses
    def visit_BinOp(self, node): 
        # Must remember to handle % when used for mathematical expressions, not just string formatting
        # TODO: if the left & right side are type Num, we want to be doing math; otherwise this 
        if (get_binop(node.op, ' %s ') == ' % '):
            node_type_left = type(node.left)
            node_type_right = type(node.left)
            if node_type_left == ast.Num and node_type_right == ast.Num:
                self.write(node.left)
                # self.write(node.left, ', ', node.right)
            else:
                self.write(node.left, get_binop(node.op, ' %s '), node.right)
        else:
            self.write(node.left, get_binop(node.op, ' %s '), node.right)

    @enclose('()')
    def visit_BoolOp(self, node):
        op = get_boolop(node.op, ' %s ')
        for idx, value in enumerate(node.values):
            self.write(idx and op or '', value)

    @enclose('()')
    def visit_Compare(self, node):
        self.visit(node.left)
        for op, right in zip(node.ops, node.comparators):
            self.write(get_cmpop(op, ' %s '), right)

    @enclose('()')
    def visit_UnaryOp(self, node):
        self.write(get_unaryop(node.op), ' ', node.operand)

    def visit_Subscript(self, node):
        self.write(node.value, '[', node.slice, ']')

    def visit_Slice(self, node):
        self.conditional_write(node.lower)
        self.write(':')
        self.conditional_write(node.upper)
        if node.step is not None:
            self.write(':')
            if not (isinstance(node.step, ast.Name) and node.step.id == 'None'):
                self.visit(node.step)

    def visit_Index(self, node):
        self.visit(node.value)

    def visit_ExtSlice(self, node):
        self.comma_list(node.dims, len(node.dims) == 1)

    def visit_Yield(self, node):
        self.write('yield')
        self.conditional_write(' ', node.value)

    @enclose('()')
    def visit_Lambda(self, node):
        self.write('lambda ')
        self.signature(node.args)
        self.write(': ', node.body)

    def visit_Ellipsis(self, node):
        self.write('...')

    def generator_visit(left, right):
        def visit(self, node):
            self.write(left, node.elt)
            for comprehension in node.generators:
                self.visit(comprehension)
            self.write(right)
        return visit

    visit_ListComp = generator_visit('[', ']')
    visit_GeneratorExp = generator_visit('(', ')')
    visit_SetComp = generator_visit('{', '}')
    del generator_visit

    @enclose('{}')
    def visit_DictComp(self, node):
        self.write(node.key, ': ', node.value)
        for comprehension in node.generators:
            self.visit(comprehension)

    @enclose('()')
    def visit_IfExp(self, node):
        self.write(node.body, ' if ', node.test, ' else ', node.orelse)

    def visit_Starred(self, node):
        self.write('*', node.value)

    @enclose('``')
    def visit_Repr(self, node):
        # XXX: python 2.6 only
        self.visit(node.value)

    def visit_Module(self, node):
        for stmt in node.body:
            self.visit(stmt)

    # Helper Nodes

    def visit_arg(self, node):
        self.write(node.arg)
        self.conditional_write(': ', node.annotation)

    def visit_alias(self, node):
        self.write(node.name)
        self.conditional_write(' as ', node.asname)

    def visit_comprehension(self, node):
        self.write(' for ', node.target, ' in ', node.iter)
        if node.ifs:
            for if_ in node.ifs:
                self.write(' if ', if_)
