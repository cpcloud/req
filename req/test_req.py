from req import translate


def f(a, b, c):
    return a + b * c - 1


def test_simple():
    q = translate(f)
    assert q == 'f: {[a; b; c] ((a) + ((b) * (c))) - (1)}'


def g(a, b):
    return a * b


def test_binop():
    q = translate(g)
    assert q == 'g: {[a; b] (a) * (b)}'


def h(c, d):
    x = c + 1
    return x + 2


def test_assign():
    q = translate(h)
    assert q == 'h: {[c; d] x: (c) + (1); (x) + (2)}'


def k(x):
    if x == 1:
        return x + 1
    else:
        return x * 2


def test_if():
    q = translate(k)
    assert q == 'k: {[x] $[(x) = (1); (x) + (1); (x) * (2)]}'


def mapper(x):  # -> f each x
    return map(f, x)


def test_call():
    q = translate(mapper)
    assert q == 'mapper: {[x] each[f; x]}'
