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
    assert translate(h) == 'h: {[c; d] x: (c) + (1); (x) + (2)}'


def k(x):
    if x == 1:
        return x + 1
    else:
        return x * 2


def test_if():
    assert translate(k) == 'k: {[x] $[(x) = (1); (x) + (1); (x) * (2)]}'


def mapper(x):  # -> f each x
    return map(f, x)


def test_call():
    assert translate(mapper) == 'mapper: {[x] each[f; x]}'


def powfunc(x):
    return x ** 2 + 1


def test_pow():
    assert translate(powfunc) == 'powfunc: {[x] ((x) xpow (2)) + (1)}'


def mylooper(n):
    s = 0.0
    for i in range(n):
        s = s + 1
    return s


def test_for():
    r = translate(mylooper)
    assert r == 'mylooper: {[n] s: 0.0; {[i] s: (s) + (1)} each til[n]; s}'


def mywhile(n):
    s = 0.0
    i = 0
    while i < n:
        s = s + i
        i = i + 1
    return s


def test_while():
    r = translate(mywhile)
    assert r == 'mywhile: {[n] s: 0.0; i: 0; while[(i) < (n); s: (s) + (i); i: (i) + (1)]; s}'


def test_dict():
    x = {'a': 1, 'b': 2}
    assert translate(x) == '("a"; "b")!(1; 2)'


def test_list():
    x = [1, 'a', 2, []]
    assert translate(x) == '(1; "a"; 2; ())'
