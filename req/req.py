import ast
import inspect


def symbolify(x):
    return '`%s' % x


class Symbol(object):
    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return symbolify(self.name)

    __str__ = __repr__


class List(object):
    def __init__(self, *values):
        self.values = values

    def __repr__(self):
        if len(self.values) == 1:
            return '(,:[%s])' % self.values[0]
        return '(%s)' % '; '.join(map(str, self.values))


class Function(object):
    def __init__(self, name, args, code):
        self.name = name
        self.args = args
        self.code = code

    def __repr__(self):
        return '%s: {[%s] %s}' % (self.name, '; '.join(map(str, self.args)),
                                  self.code)


class BinOp(object):
    op = None

    def __init__(self, left, right):
        self.left, self.right = left, right

    def __repr__(self):
        return '(%s) %s (%s)' % (self.left, self.op, self.right)


class Add(BinOp):
    op = '+'


class Mult(BinOp):
    op = '*'


class Sub(BinOp):
    op = '-'


ops = {
    ast.Add: Add,
    ast.Mult: Mult,
    ast.Sub: Sub
}

compops = {
    ast.Eq: '=',
}


qbuiltins = {
    'map': 'each'
}


class NodeVisitor(ast.NodeVisitor):
    def visit_BinOp(self, node):
        return ops[type(node.op)](self.visit(node.left), self.visit(node.right))

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

    def visit_FunctionDef(self, node):
        return Function(node.name,
                        [arg.arg for arg in node.args.args],
                        '; '.join(map(str, map(self.visit, node.body))))

    def visit_Module(self, node):
        return ';\n'.join(map(str, map(self.visit, node.body)))

    def visit_arg(self, node):
        return node.arg

    def visit_Assign(self, node):
        return '%s: %s' % (self.visit(node.targets[0]), self.visit(node.value))

    def visit_If(self, node):
        if not node.orelse:
            raise ValueError('else clause must not be empty')
        return '$[%s; %s; %s]' % (self.visit(node.test),
                                  '; '.join(map(str, map(self.visit, node.body))),
                                  '; '.join(map(str, map(self.visit, node.orelse))))

    def visit_Compare(self, node):
        ops = node.ops
        comps = node.comparators
        return '(%s) %s (%s)' % (self.visit(node.left), compops[type(ops[0])],
                                 self.visit(comps[0]))


def translate(f):
    source = inspect.getsource(f)
    parse = ast.parse(source)
    v = NodeVisitor()
    return v.visit(parse)


def f(a, b, c):
    return a + b * c - 1


if __name__ == '__main__':
    q = translate(f)
    print(q)

    import reqtest
    print(translate(reqtest))
