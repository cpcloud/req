def f(a, b, c):
    return a + b * c - 1


def g(a, b):
    return a * b


def h(c, d):
    x = c + 1
    return x + 2


def k(x):
    if x == 1:
        return x + 1
    else:
        return x * 2


def mapper(x):  # -> f each x
    return map(f, x)
