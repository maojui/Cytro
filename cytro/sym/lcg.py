import math
from functools import reduce
from cytro import invmod, gcd

class LCG:
    '''
    Linear Congruential Generator
    '''
    def __init__(self, seed, multiplier, increment, modulus):
        self.state = seed  # the "seed"
        self.m = multiplier
        self.c = increment
        self.n = modulus

    def next(self,i=1):
        self.state = (self.state * self.m + self.c) % self.n
        return self.state

    def prev(self):
        self.state = ((self.state - self.c) * invmod(self.m, self.n)) % self.n
        return int(self.state)

def find_increment(states, modulus, multiplier):
    """
    give states, modulus & multiplier, recover the increment
    s1 = s0*m + c
    c = s1 - s0*m
    """
    increment = (states[1] - states[0]*multiplier) % modulus
    return multiplier, increment, modulus

def find_multiplier(states, modulus):
    """
    give states & modulus, recover the multiplier
    t0 = s2 - s1 = (s1*m + c) - (s0*m + c) = m*(s1 - s0) (mod n)
    => m = t0 * (s1 - s0) ^ (-1) (mod n)
    """
    multiplier = (states[2] - states[1]) * invmod(states[1] - states[0], modulus) % modulus
    return find_increment(states, modulus, multiplier)

def find_modulus(states):
    """
    give states, recover the modulus
    t0 = s1 - s0
    t1 = s2 - s1 = (s1*m + c) - (s0*m + c) = m*(s1 - s0) = m*t0 (mod n)
    t2 = s3 - s2 = (s2*m + c) - (s1*m + c) = m*(s2 - s1) = m*t1 (mod n)
    t3 = s4 - s3 = (s3*m + c) - (s2*m + c) = m*(s3 - s2) = m*t2 (mod n)
    => t2*t0 - t1*t1 = (m*m*t0 * t0) - (m*t0 * m*t0) = 0 (mod n)
    """
    diffs = [s1 - s0 for s0, s1 in zip(states, states[1:])]
    zeroes = [t2*t0 - t1*t1 for t0, t1, t2 in zip(diffs, diffs[1:], diffs[2:])]
    modulus = abs(reduce(gcd, zeroes))
    return find_multiplier(states, modulus)
