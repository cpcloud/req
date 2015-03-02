from req import translate


def test_simple():
    def f(a, b, c):
        return a + b * c - 1

    q = translate(f)
    assert q == 'f: {[a; b; c]}'


def test_binop():
    def f(a, b):
        return a * b

    q = translate(f)
    assert q == 'f: {[a; b] (a) * (b)}'


def test_assign():
    def h(c, d):
        x = c + 1
        return x + 2

    q = translate(h)
    assert q == 'h: {[c; d] x: (c) + (1); (x) + (2)}'


def test_if():
    def k(x):
        if x == 1:
            return x + 1
        else:
            return x * 2

    q = translate(k)
    assert q == 'k: {[x] $[(x) = (1); (x) + (1); (x) * (2)]}'


def test_call():
    def f(x):
        return x + 1

    def mapper(x):  # -> f each x
        return map(f, x)

    q = translate(mapper)
    assert q == 'mapper: {[x] each[f; x]}'
