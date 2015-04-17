import pytest

from req import translate
import math


def tr(*args, **kwargs):
    return translate(*args, **kwargs).strip()


def test_simple():
    def f(a, b, c):
        return a + b * c - 1

    assert tr(f) == 'f: {[a; b; c] ((a) + ((b) * (c))) - (1)}'


def test_binop():
    def g(a, b):
        return a * b

    assert tr(g) == 'g: {[a; b] (a) * (b)}'


def test_assign():
    def h(c, d):
        x = c + 1
        return x + 2

    assert tr(h) == 'h: {[c; d] x: (c) + (1); (x) + (2)}'


def test_if():
    def k(x):
        if x == 1:
            return x + 1
        else:
            return x * 2

    assert tr(k) == 'k: {[x] $[(x) = (1); (x) + (1); (x) * (2)]}'


def test_call():
    def mapper(x):  # -> f each x
        return map(lambda x: x + 1, x)

    assert tr(mapper) == 'mapper: {[x] each[{[x] (x) + (1)}; x]}'


def test_pow():
    def powfunc(x):
        return x ** 2 + 1

    assert tr(powfunc) == 'powfunc: {[x] ((x) xexp (2)) + (1)}'


def test_for():
    def mylooper(n):
        s = 0.0
        for i in range(n):
            s = s + 1
        return s

    r = tr(mylooper)
    assert r == 'mylooper: {[n] s: 0.0; {[i] s: (s) + (1)} each til[n]; s}'


def test_for_with_aug():
    def mylooper(n):
        s = 0.0
        for i in range(n):
            s += 1
            s *= 1
            s /= 1
            s -= 1
        return s

    r = tr(mylooper)
    assert r == 'mylooper: {[n] s: 0.0; {[i] s +: (1); s *: (1); s %: (1); s -: (1)} each til[n]; s}'


def test_while():
    def mywhile(n):
        s = 0.0
        i = 0
        while i < n:
            s = s + i
            i = i + 1
        return s

    r = tr(mywhile)
    assert r == 'mywhile: {[n] s: 0.0; i: 0; while[(i) < (n); s: (s) + (i); i: (i) + (1)]; s}'


def test_dict():
    x = {'a': 1, 'b': 2}
    assert tr(x) == '("a"; "b")!(1; 2)'


def test_list():
    x = [1, 'a', 2, []]
    assert tr(x) == '(1; "a"; 2; ())'


def test_nested():
    def nested(x):
        def g(y):
            return x + y
        return g
    assert tr(nested) == 'nested: {[x] g: {[y] (x) + (y)}; g}'


def test_lambda():
    lam = lambda x, y: x + y
    assert tr(lam) == '{[x; y] (x) + (y)}'


@pytest.mark.xfail(raises=AssertionError)
def test_complex_lambda():
    lam = lambda x, y: x + y ** 2 + math.sin(x)
    assert tr(lam) == ''
