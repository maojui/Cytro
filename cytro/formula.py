#-*- coding:utf-8 -*-

import math
import random
from operator import mul
from functools import reduce

def grey_code(n):
    """ 
    Encode grey code :
        Enter a value @n, return the correspond value in grey code. 
    """
    return n ^ (n >> 1)

def rev_grey_code(g):
    """ 
    Decode grey code :
        Enter a number @g, return the vaule before encode to grey code. 
    """
    n = 0
    while g:
        n ^= g
        g >>= 1
    return n

def hamming_weight(x):
    """ Hamming Weight, count 1s for number in binary. """
    return bin(x).count('1')

def factorial(n):
    res = 1
    while n > 1:
        res *= n
        n -= 1
    return res

def factorial_get_prime_pow(n, p):
    """
    Return power of prime @p in @n!
    """
    count = 0
    ppow = p
    while ppow <= n:
        count += n // ppow
        ppow *= p
    return count

def extract_prime_power(a, p):
    """
    Return s, t such that  a = p**s * t,  t % p = 0
    """
    s = 0
    if p > 2:
        while a and a % p == 0:
            s += 1
            a //= p
    elif p == 2:
        while a and a & 1 == 0:
            s += 1
            a >>= 1
    else:
        raise ValueError("Number %d is not a prime (is smaller than 2)" % p)
    return s, a

def nCk(n, k):
    """
    Combinations number
    """
    if n < 0: raise ValueError("Invalid value for n: %s" % n)
    if k < 0 or k > n: return 0
    if k in (0, n): return 1
    if k in (1, n-1): return n
    low_min = 1
    low_max = min(n, k)
    high_min = max(1, n - k + 1)
    high_max = n
    return reduce(mul, range(high_min, high_max + 1), 1) // reduce(mul, range(low_min, low_max + 1), 1)

def randint_bits(size):
    low = 1 << (size - 1)
    hi = (1 << size) - 1
    return random.randint(low, hi)

def ceil(x, y):
    """
    Input @x,@y, 
    return the smallest Integer >= x/y"""
    return x // y + (x % y != 0)

def nroot(x, n):
    """
    Return truncated n'th root of x.
    """
    if n < 0:
        raise ValueError("can't extract negative root")

    if n == 0:
        raise ValueError("can't extract zero root")

    sign = 1
    if x < 0:
        sign = -1
        x = -x
        if n % 2 == 0:
            raise ValueError("can't extract even root of negative")

    high = 1
    while high ** n <= x:
        high <<= 1

    low = high >> 1
    while low < high:
        mid = (low + high) >> 1
        mr = mid ** n
        if mr == x:
            return (mid, True)
        elif low < mid and mr < x:
            low = mid
        elif high > mid and mr > x:
            high = mid
        else :
            return (sign * mid, False)
    return (sign * (mid + 1) , False)


def sqrt(n):
   return nroot(n, 2)[0]

def gcd(*lst):
    """
    Return gcd of a variable number of arguments.
    """
    return abs(reduce(lambda a, b: _gcd(a, b), lst))


def lcm(*lst):
    """
    Return lcm of a variable number of arguments.
    """
    return reduce(lambda a, b: _lcm(a, b), lst)

def _gcd(a, b):
    """
    Return greatest common divisor using Euclid's Algorithm.
    """
    if a == 0: return b
    if b == 0: return a
    while b:
        a, b = b, a % b
    return abs(a)


def _lcm(a, b):
    """
    Return lowest common multiple.
    """
    if not a or not b:
        raise ZeroDivisionError("lcm arguments may not be zeros")
    return abs(a * b) // gcd(a, b)


def xgcd(a, b):
    """
    Extented Euclid GCD algorithm.
    Return (x, y, g) : a * x + b * y = gcd(a, b) = g.
    """
    if a == 0: return 0, 1, b
    if b == 0: return 1, 0, a

    px, ppx = 0, 1
    py, ppy = 1, 0

    while b:
        q = a // b
        a, b = b, a % b
        x = ppx - q * px
        y = ppy - q * py
        ppx, px = px, x
        ppy, py = py, y

    return ppx, ppy, a


def get_primes(n):
    """ 
    High speed to generate all primes which is smaller than n.
    http://stackoverflow.com/questions/2068372/fastest-way-to-list-all-primes-below-n/3035188#3035188 
    """
    n, correction = n-n%6+6, 2-(n%6>1)
    sieve = [True] * int((n//3))
    for i in range(1,int(n**0.5/3)+1):
      if sieve[i]:
        k=3*i+1|1
        sieve[      k*k//3      ::2*k] = [False] * int((n//6-k*k//6-1)//k+1)
        sieve[k*(k-2*(i&1)+4)//3::2*k] = [False] * int((n//6-k*(k-2*(i&1)+4)//6-1)/k+1)
    return [2,3] + [3*i+1|1 for i in range(1,int(n/3-correction)) if sieve[i]]

def sieve(n, scope):
    """
    If a big num, which is multiple by small prime, this function can sieve it by giving a small prime scope.
    @n      : the big num
    @scope  : the small prime range
    """
    primes = get_primes(scope)
    factors = {}
    for p in primes :
        count = 0
        while n % p == 0:
            n //= p
            count += 1
        if count == 0 :
            continue
        else :
            factors[p] = count
    return factors
