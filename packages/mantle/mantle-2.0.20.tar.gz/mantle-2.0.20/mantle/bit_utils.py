from magma.bitutils import int2seq, seq2int
import inspect
from types import FunctionType
from collections.abc import Sequence


def clz(x):
    if x == 0:
        return 32

    n = 0
    if x <= 0x0000FFFF:
        n = n + 16
        x = x << 16
    if x <= 0x00FFFFFF:
        n = n + 8
        x = x << 8
    if x <= 0x0FFFFFFF:
        n = n + 4
        x = x << 4
    if x <= 0x3FFFFFFF:
        n = n + 2
        x = x << 2
    if x <= 0x7FFFFFFF:
        n = n + 1
    return n


def log2(x):
    return 31 - clz(x)


def fun2seq(f, n=None):
    if not n:
        logn = len(inspect.getargspec(f).args)
        n = 1 << logn
    else:
        logn = log2(n)

    l = []
    for i in range(n):
         arg = int2seq(i, logn)
         l.append(1 if f(*arg) else 0)
    return l


def lutinit(init, n=None):
    if isinstance(init, FunctionType):
        init = fun2seq(init, n)

    if isinstance(init, Sequence):
        nlut = len(init)
        if n != nlut:
            assert n % nlut == 0
            init = (n//nlut) * init
        init = seq2int(init)

    assert n is not None

    return init, n
