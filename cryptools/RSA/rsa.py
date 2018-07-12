#-*- coding:utf-8 -*-
import os
import subprocess
from cryptools.stuff import sageworks
from cryptools.modular import invmod
from cryptools.formula import gcd, get_prime
from .WienerAttack import _WienerAttack
from Crypto.PublicKey import RSA
from Crypto.Util.number import isPrime
import requests
import re

class RSAKey():
    
    def __init__(self,tup,print_out=False):
        """
        Crypto.PublicKey.RSA.construct(tup)
            @tup : (n,e) for public key
                 : (n,e,d) for private key
            @print_out : default is False, True for print out n,e,d, ... content.
        """
        self.print_out = print_out
        self.key = RSA.construct(tup)
        self.copy_val_to_object()
        self._print()
    
    def set_private(self,p,q):
        """
        input p,q calculate d, invmod(e,phi)
        """
        d = self.cal_private(self.e,p,q)
        _key = RSA.construct((self.key.n,self.key.e,d))
        if pow(2,_key.e*_key.d,_key.n) == 2 and _key.has_private():
            print("[+] Success.")
            self.key = _key
        self.copy_val_to_object()
        self._print()

    def write_private(self,filename):
        """
        Write private key to file.
        @filename : path to save
        """
        with open(filename,'wb') as f:
            f.write(self.key.exportKey())

    def _print(self):
        if self.print_out:
            print("[+] Modular(n)  : {}".format(self.key.n))
            print("[+] Public Exponent(e) : {}".format(self.key.e))
            if self.key.has_private():
                print("[+] Private exponent(d)  : {}".format(self.key.d))
                print("[+] First factor (p) : {}".format(self.key.p))
                print("[+] Second factor (q) : {}".format(self.key.q))
                print("[+] CRT coefficient (u) : {}".format(self.key.u))
    
    def encrypt(self,plaintext):
        return pow(ciphertext,self.e,self.n)
    
    def decrypt(self,ciphertext):
        """
        ???
        """
        return pow(ciphertext,self.d,self.n)

    def copy_val_to_object(self):
        try :
            self.n = self.key.n
            self.e = self.key.e
            self.d = self.key.d
        except :
            pass
    
    @classmethod
    def load_pem(cls, pem):
        "Initialize RSA key from a file"
        _key = RSA.importKey(pem.strip())
        if _key.has_private():
            return cls((_key.n,_key.e,_key.d))
        return cls((_key.n,_key.e))

    @classmethod
    def load_file(cls, filename):
        "Initialize RSA key from a file"
        _key = RSA.importKey(open(filename).read())
        if _key.has_private():
            return cls((_key.n,_key.e,_key.d))
        return cls((_key.n,_key.e))
    
    @staticmethod
    def cal_private(e, p, q):
        phi = (p-1)*(q-1)
        return invmod(e,phi)


class MultiPrimeRSA(RSAKey):
    
    def set_factors(self,paris):
        self.pairs = pairs

    def fast_decrypt(self, c):
        ns = []
        ms = []
        for p, k in self.pairs:
            pk = p ** k
            phi = pk * (p-1)/p
            d = invmod(self.e, phi)
            mk = pow(c, d, pk)
            ns.append(pk)
            ms.append(mk)
        m = solve_crt(ms,ns)
        return m

    @staticmethod
    def cal_private(e, pairs):
        phi = 1
        for p, k in pairs:
            phi *= pow(p,(k-1)) * (p-1)
        d = invert(e, phi)
        return d


def gcd_multiple_keys(keys):
    """
        GCD at each module, find if they are product of same prime or not
        @keys : (n,e)s in a list or something iterable.
        return RSAKeys if Ns have same prime between each.  
    """
    keys = []
    for i,n in enumerate(keys) :
        for j,n2 in enumerate(keys):
            if not gcd(n,n2) == 1 and n != n2:
                p = gcd(n,n2)
                priv = RSAKey((n, pub.e, invmod(pub.e,(n//p-1)*(p-1))))
                keys.append(priv)
    return keys


#-*- coding:utf-8 -*-
from cryptools.formula import *
from cryptools.modular import *

def common_modular(set1,set2):
    """
    Common Modular Attack, if you get c1 = m^e1 % N , c2 = m^e2 % N
        Given two set of ( N, e, c )
        return plaintext
    """
    n1,e1,c1 = set1 
    n2,e2,c2 = set2 
    if n1 != n2 : 
        print("[-] Common Modular Attack Fail, N1 != N2")
        return
    if gcd(e1,e2) != 1 : 
        print("[-] Common Modular Attack Fail, gcd(e1,e2) != 1")
        return
    a,b = xgcd(e1,e2)
    t1 = pow(c1,abs(a),n1)
    t2 = pow(c2,abs(b),n2)
    if a < 0 : t1 = invmod(t1,n1)
    if b < 0 : t2 = invmod(t2,n2)
    return t1*t2 % n1
    

def pollard_rho(N):
    """    
    For one of N's prime p, 
        1. If (p-1) is a K-smooth number. (k is small)
        2. When all factor are appear in b
    Then it can be solved by Pollard_P-1.
    """
    factor, cycle = 1,1    
    x, fixed = 2,2
    while factor == 1:
        print(f'Pollard rho cycle : {cycle}')
        count = 1
        cycle *= 2
        while count <= cycle and factor <= 1:
            x = (x*x + 1) % N
            factor = gcd(x - fixed, N)
            count += 1
        fixed = x
    return factor


def pollard_pm1(N,prange=10000000):
    """    
    For one of N's prime p, 
        1. If (p-1) is a K-smooth number. (k is small)
        2. When all factor are appear in b
    Then it can be solved by Pollard_P-1.
    """
    if isPrime(N):
        return N
    test_p = iter(get_prime(prange))
    a = 2
    while True:
        try :
            b = next(test_p)
            a = pow(a, b, N)
            p = gcd(a - 1, N)
            if 1 < p < N:
                return p
        except :
            print("Pollard P-1 Failed.")
            return 0


def pollard_brute(N):
    """    
    For one of N's prime p, 
        1. If (p-1) is a K-smooth number. (k is small)
        2. When all factor are appear in b
    Then it can be solved by Pollard_P-1.
    """
    a = 2
    b = 1
    while True:
        if b % 10000 == 0:
            print('pollard brute : ',b)
        a = pow(a, b, N)
        p = gcd(a - 1, N)
        if 1 < p < N:
            return p
        b += 1


def hastad_broadcast(cipher,module):
    """    
    Chinese Remainder
    If the same message, encrypt by same exponent but different module
    hastad broadcast attack may solved it.
    
        usage  : hastad_broadcast([C1,C2,C3],[N1,N2,N3])
        return : C = M^e mod (N1*N2*N3)
    
    if M^e < N1*N2*N3 : solved.
    """
    return solve_crt(cipher,module)

def wiener(N,e):
    """
    If the encryption exponent is too small or too large.

    Let N=pq, q<p<2q, d < (1/3) * N**(1/4) 
        
        usage  : wiener(N,exponent)
        return : p, q
    
    link : https://en.wikipedia.org/wiki/Wiener's_attack
    """
    wa = _WienerAttack(N,e)
    if wa.p == None :
        print("Wiener Attack Fail.")
        return None
    return int(wa.p), int(wa.q)

def fermat_factorization(N) :
    """
    Fermat's factorization for close p and q
    link : https://en.wikipedia.org/wiki/Fermat%27s_factorization_method
    """
    a = nroot(N,2)
    b2 = a*a - N
    b = nroot(N,2)
    count = 0
    while b*b != b2:
        a = a + 1
        b2 = a*a - N
        b = nroot(b2,2)
        count += 1
    p=a+b
    q=a-b
    return p, q

def williams_pp1(n):
    """    
    If (p+1) is a K-smooth number. (k is small)
    Then it can be solved by Pollard_P-1.
    """
    
    def mlucas(v, a, n):
        """ Helper function for williams_pp1().  Multiplies along a Lucas sequence modulo n. """
        v1, v2 = v, (v**2 - 2) % n
        for bit in bin(a)[3:]: v1, v2 = ((v1**2 - 2) % n, (v1*v2 - v) % n) if bit == "0" else ((v1*v2 - v) % n, (v2**2 - 2) % n)
        return v1
    
    if isprime(n): return n
    m = ispower(n)
    if m: return m
    for v in count(1):
        for p in primegen():
            e = ilog(isqrt(n), p)
            if e == 0: break
            for _ in range(e): v = mlucas(v, p, n)
            g = gcd(v - 2, n)
            if 1 < g < n: return g
            if g == n: break

#  ------------------------  Start  ------------------------
#  Integrate those function from https://github.com/sourcekris/RsaCtfTool/blob/master/RsaCtfTool.py

def boneh_durfee(N,e,d=0.26):
    """
    If d < N^0.292, Boneh Durfee method should return a "d", else returns 0
    many of these problems will be solved by the wiener attack module 
    
    Only works if the sageworks() function returned True
    """
    import cryptools.RSA 
    filename = os.path.join(os.path.dirname(cryptools.RSA.__file__),'boneh_durfee.sage.py')
    if sageworks():
        sageresult = int(subprocess.check_output(['sage', filename, str(N), str(e), str(d)]))
        return sageresult

def noveltyprimes(n):
    """ 
    "primes" of the form 31337 - 313333337 - see ekoparty 2015 "rsa 2070"
    *** not all numbers in this form are prime but some are (25 digit is prime) ***
    """
    maxlen = 25  # max number of digits in the final integer
    for i in range(maxlen-4):
        prime = int("3133" + ("3" * i) + "7")
        if n % prime == 0:
            q = n//prime
            return prime,q

def smallq(n):
    """Try an attack where q < 100,000, from BKPCTF2016 - sourcekris"""
    for prime in primes(100000):
        if self.pub_key.n % prime == 0:
            q = n // prime
            return prime,q

def smallfraction(n):
    """
    Code/idea from Renaud Lifchitz's talk 15 ways to break RSA security @ OPCDE17
    Only works if the sageworks() function returned True
    """
    import cryptools.RSA 
    filename = os.path.join(os.path.dirname(cryptools.RSA.__file__),'smallfraction.sage.py')
    sageresult = int(subprocess.check_output(['sage', filename, str(self.pub_key.n)]))
    if sageresult > 0:
        p = sageresult
        q = n // sageresult
        return p,q

def mersenne_primes(n):
    p = q = None
    mersenne_tab = [2, 3, 5, 7, 13, 17, 19, 31, 61, 89, 107, 127, 521,
                    607, 1279, 2203, 2281, 3217, 4253, 4423, 9689, 9941,
                    11213, 19937, 21701, 23209, 44497, 86243, 110503,
                    132049, 216091, 756839, 859433, 1257787, 1398269,
                    2976221, 3021377, 6972593, 13466917, 20336011,
                    24036583, 25964951, 30402457, 32582657, 37156667,
                    42643801, 43112609, 57885161, 74207281, 77232917]
    for mersenne_prime in mersenne_tab:
        if n % ((2**mersenne_prime)-1) == 0:
            p = (2**mersenne_prime)-1
            q = n // ((2**mersenne_prime)-1)
            break
    if p is not None and q is not None:
        return p,q

#  ------------------------  END  ------------------------
def franklin_reiter(n,e,c1,c2,r,a=1):
    """
    If message(m1,m2) is in linear transformation, and m2 can be write into (a*m1+r)

        f1 = m^e - c1
        f2 = (a*m + r)^e - c2

    Given n,e,c1,c2,r,a
    return m
    """
    import cryptools.RSA 
    filename = os.path.join(os.path.dirname(cryptools.RSA.__file__),'franklin_reiter_related_message.sage.py')
    sageresult = int(subprocess.check_output(['sage', filename, str(n), str(e), str(c1), str(c2), str(r), str(a)]).strip())
    # print(sageresult)
    if int(sageresult) > 0:
        m = sageresult
        return m


def factordb(n):
    import requests
    from bs4 import BeautifulSoup
    from functools import reduce
        
    
    url = f'http://factordb.com/index.php?query={n}'
    td = BeautifulSoup(requests.get(url).text,'html.parser').select('td')
    states = list(td[11].strings)[0].strip(" ")
    print({
        'C'    : "[ ] Composite, Still no factors known.",
        "CF"   : "[ ] Composite, factors known, If number is small, You can try it again.",
        'FF'   : "[+] Composite, fully factored",
        "P"    : "[+] Definitely prime",
        "PRP"  : "[ ] Probably prime",
        "U"    : "[-] Factordb Search Failed",
        "Unit" : "[-] 1 is nothing.",
        "N"    : "This number is not in database (and was not added due to your settings)"
    }[states])
    
    if not states in  ['FF','P','PRP','CF'] :
        return None

    factor = ''
    ss = list(td[13].strings)
    for i,s in enumerate(ss):
        if ('.' in s) :
            for a in td[13].select('a') :
                if s == a.string:
                    
                    temp1 = requests.get('http://factordb.com/'+ a['href'])
                    tsoup = BeautifulSoup(temp1.text,'html.parser')
                    temp2 = requests.get('http://factordb.com/'+ tsoup.select('td')[12].a['href'])
                    tsoup2 = BeautifulSoup(temp2.text,'html.parser')
                    
                    for dnum in tsoup2.select('td')[-1].strings:
                        factor += dnum.strip('\n')
                    break

        elif s[0] != '<' :
            factor += s
        else :
            pass
    
    
    pair = {}

    _, factors = factor.split(' = ')
    if ')^' in factors :
        factors, exp = factors.split('^')
        factors = factors.strip('\(').strip('\)')
        pair = { x:int(exp) for x in list(map(int,factors.split(' · ')))}
    elif '^' in factors :
        for f in factors.split(' · '):
            if '^' in f :
                num,exp = f.split('^')
                pair[int(num)] = int(exp)
            else :
                pair[int(f)] = int(1)
    else :
        pair = { x:1 for x in list(map(int,factors.split(' · ')))}
    
    assert n == reduce( lambda x, y: x*y, [pow(k,v) for k,v in pair.items()],1), 'factordb function failed.... try connect yourself.'
    return pair


# def coppersmith(n):
# """
# Coppersmith's method : uses the Lenstra–Lenstra–Lovász lattice basis reduction algorithm (LLL)
# It finds the zeroes for the polynomial where x < N^{(1/degree(f(x))-epsilon} (epsilon essentially determines the running time) -> small_roots function
# """



