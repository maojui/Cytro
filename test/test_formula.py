import unittest
import os
import random
from cytro import *
from Crypto.Util.number import getPrime

class FormulaTest(unittest.TestCase):

    def test_factorize(self):
        n = 1
        for i in range(10):
            ra = random.randint(1,25)
            n *= getPrime(ra)
        fs = factorize(n)
        res = 1
        for f,p in fs.items():
            res *= pow(f,p)
        self.assertEqual(res,n)
    
    def test_nroot_true(self):
        x = 1
        n = random.randint(1,10)
        f = getPrime(random.randint(1,25))
        for i in range(n):
            x *= f
        val, root = nroot(x,n)
        self.assertEqual(val,f)
        self.assertEqual(root,True)
    
    def test_nroot_false(self):
        p = getPrime(30)
        q = getPrime(20)
        x = p*q
        val, root = nroot(x,2)
        self.assertEqual(root,False)
    
    def test_randbit(self):
        n = random.randint(0,1000)
        rb = randint_bits(n)
        self.assertEqual(len(bin(rb)[2:]),n)
    
    def test_gcd(self):
        primes = [getPrime(i) for i in range(10,30)]
        self.assertEqual(gcd(*primes),1)
    
    def test_lcm(self):
        n = 1
        primes = []
        for i in range(1,30):
            prime = getPrime(i)
            n *= prime
            primes.append(n)
        random.shuffle(primes)
        self.assertEqual(lcm(*primes),n)
    
    def test_get_primes(self):
        primes = get_primes(1452)
        self.assertEqual(primes,[2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113, 127, 131, 137, 139, 149, 151, 157, 163, 167, 173, 179, 181, 191, 193, 197, 199, 211, 223, 227, 229, 233, 239, 241, 251, 257, 263, 269, 271, 277, 281, 283, 293, 307, 311, 313, 317, 331, 337, 347, 349, 353, 359, 367, 373, 379, 383, 389, 397, 401, 409, 419, 421, 431, 433, 439, 443, 449, 457, 461, 463, 467, 479, 487, 491, 499, 503, 509, 521, 523, 541, 547, 557, 563, 569, 571, 577, 587, 593, 599, 601, 607, 613, 617, 619, 631, 641, 643, 647, 653, 659, 661, 673, 677, 683, 691, 701, 709, 719, 727, 733, 739, 743, 751, 757, 761, 769, 773, 787, 797, 809, 811, 821, 823, 827, 829, 839, 853, 857, 859, 863, 877, 881, 883, 887, 907, 911, 919, 929, 937, 941, 947, 953, 967, 971, 977, 983, 991, 997, 1009, 1013, 1019, 1021, 1031, 1033, 1039, 1049, 1051, 1061, 1063, 1069, 1087, 1091, 1093, 1097, 1103, 1109, 1117, 1123, 1129, 1151, 1153, 1163, 1171, 1181, 1187, 1193, 1201, 1213, 1217, 1223, 1229, 1231, 1237, 1249, 1259, 1277, 1279, 1283, 1289, 1291, 1297, 1301, 1303, 1307, 1319, 1321, 1327, 1361, 1367, 1373, 1381, 1399, 1409, 1423, 1427, 1429, 1433, 1439, 1447, 1451])
    
    def test_sieve(self):
        factors = {}
        max_fac = random.randint(1000,10000)
        primes = get_primes(max_fac)
        n = 1
        for i in range(1000) :
            p = random.choice(primes)
            factors[p] = factors.get(p,0) + 1
            n *= p
        res = sieve(n,max_fac)
        for k,v in factors.items() :
            self.assertEqual(res[k],v)

if __name__ == "__main__":
    unittest.main()
