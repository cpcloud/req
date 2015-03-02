`req`use your self from using the `q` language, and use Python instead.


`req` translates your Python code to `q`, so you don't have to ever write `q`
again.


Use it as a library function:

```python
In [1]: from req import translate

In [2]: def f(a, b):
   ...:     return a + b
   ...:

In [3]: translate(f)
Out[3]: 'f: {[a; b] (a) + (b)}'
```

Or as a command line tool


```sh
$ echo "def f(a, b): return a + b" | ./req.py                                                                                
f: {[a; b] (a) + (b)}
```
