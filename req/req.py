#!/usr/bin/env python

import ast
import inspect
import types

try:
    basestring
except NameError:
    basestring = str


class BinOp(object):
    op = None

    def __init__(self, left, right):
        self.left = left
        self.right = right

    def __repr__(self):
        return '(%s) %s (%s)' % (self.left, self.op, self.right)


class Add(BinOp):
    op = '+'


class Mult(BinOp):
    op = '*'


class Sub(BinOp):
    op = '-'


class Div(BinOp):
    op = '/'


class FloorDiv(BinOp):
    op = 'div'


class Pow(BinOp):
    op = 'xpow'


ops = {
    ast.Add: Add,
    ast.Mult: Mult,
    ast.Sub: Sub,
    ast.Div: Div,
    ast.FloorDiv: FloorDiv,
    ast.Pow: Pow
}

compops = {
    ast.Eq: '=',
    ast.NotEq: '<>',
    ast.Lt: '<',
    ast.Gt: '>',
    ast.LtE: '<=',
    ast.GtE: '>='
}


qbuiltins = {
    'map': 'each',
    'range': 'til',
    'xrange': 'til'
}


class NodeVisitor(ast.NodeVisitor):
    def generic_visit(self, node):
        node_kind = type(node).__name__
        method = getattr(self, 'visit_%s' % node_kind, None)
        if method is None:
            raise NotImplementedError("%r nodes not implemented" % node_kind)
        return method(node)

    def visit_BinOp(self, node):
        return ops[type(node.op)](self.visit(node.left),
                                  self.visit(node.right))

    def visit_Call(self, node):
        name = self.visit(node.func)
        return '%s[%s]' % (qbuiltins.get(name, name),
                           '; '.join(map(str, map(self.visit, node.args))))

    def visit_Name(self, node):
        return node.id

    def visit_Return(self, node):
        return self.visit(node.value)

    def visit_Num(self, node):
        return node.n

    def visit_Str(self, node):
        return '"%s"' % node.s

    def visit_FunctionDef(self, node):
        return '%s: {[%s] %s}' % (node.name,
                                  '; '.join(map(self.visit, node.args.args)),
                                  qify(self.visit, node.body))

    def visit_arg(self, node):
        return node.arg

    def visit_Module(self, node):
        return qify(self.visit, node.body, char='\n')

    def visit_Assign(self, node):
        assert len(node.targets) == 1, 'only a single assignment target allowed'
        return '%s: %s' % (self.visit(node.targets[0]), self.visit(node.value))

    def visit_If(self, node):
        assert node.orelse, 'else clause must not be empty'
        return '$[%s; %s; %s]' % (self.visit(node.test),
                                  qify(self.visit, node.body),
                                  qify(self.visit, node.orelse))

    def visit_Compare(self, node):
        ops = node.ops
        comps = node.comparators
        return '(%s) %s (%s)' % (self.visit(node.left), compops[type(ops[0])],
                                 self.visit(comps[0]))

    def visit_For(self, node):
        target = node.target
        assert isinstance(target, ast.Name), 'target must be a name'

        it = node.iter
        body = node.body
        return '{[%s] %s} each %s' % (self.visit(target),
                                      qify(self.visit, body),
                                      self.visit(it))

    def visit_While(self, node):
        return 'while[%s; %s]' % (self.visit(node.test),
                                  qify(self.visit, node.body))

    def visit_alias(self, node):
        if node.asname is None:
            return node.name
        raise ValueError('Cannot rewrite aliased imports')

    def visit_ImportFrom(self, node):
        return r'\l .%s' % '.'.join([node.module] + list(map(self.visit, node.names)))

    def visit_Assert(self, node):
        return 'if[not[%s]; \'`%s]' % (self.visit(node.test), node.msg or '')

    def visit_Dict(self, node):
        return '(%s)!(%s)' % (qify(self.visit, node.keys),
                              qify(self.visit, node.values))

    def visit_List(self, node):
        return '(%s)' % qify(self.visit, node.elts)

    def visit_Expr(self, node):
        return self.visit(node.value)


def qify(f, nodes, char='; '):
    return char.join(map(str, map(f, nodes)))


def translate(source):
    if isinstance(source, basestring):
        return NodeVisitor().visit(ast.parse(source))
    elif isinstance(source, (dict, list)):
        return NodeVisitor().visit(ast.parse(repr(source)))
    elif isinstance(source, types.FunctionType):
        return translate(inspect.getsource(source))
    else:
        raise TypeError('Cannot parse object of type %r' %
                        type(source).__name__)


if __name__ == '__main__':
    import sys
    import argparse
    p = argparse.ArgumentParser()
    p.add_argument('infile', nargs='?', type=argparse.FileType('r'),
                   default=sys.stdin)
    p.add_argument('outfile', nargs='?', type=argparse.FileType('w'),
                   default=sys.stdout)
    args = p.parse_args()
    args.outfile.write(translate(args.infile.read()))
