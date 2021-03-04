from random import randrange, getrandbits
from itertools import repeat


def isProbablePrime(n, t=7):
    """Miller-Rabin primality test"""

    def isComposite(a):
        """Check if n is composite"""
        if pow(a, d, n) == 1:
            return False
        for i in range(s):
            if pow(a, 2 ** i * d, n) == n - 1:
                return False
        return True

    assert n > 0
    if n < 3:
        return [False, False, True][n]
    elif not n & 1:
        return False
    else:
        s, d = 0, n - 1
        while not d & 1:
            s += 1
            d >>= 1
    for _ in repeat(None, t):
        if isComposite(randrange(2, n)):
            return False
    return True


def getPrime(n):
    """Get a n-bit prime"""
    prime = getrandbits(n)
    while not isProbablePrime(prime):
        prime = getrandbits(n)
        if int(repr(n)[-1]) % 2 == 0 or int(repr(n)[-1]) % 5 == 0:
            continue
    return prime
