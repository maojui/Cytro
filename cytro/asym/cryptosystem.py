import random
from ..formula import lcm
from ..modular import invmod
from Crypto.Util.number import getPrime, getRandomRange

class SchmidtSamoa:
    """
    Implement from Wikipedia : https://en.wikipedia.org/wiki/Schmidt-Samoa_cryptosystem
    
    SchmidtSamoa(tup) :
        @tup : (n,) for public key, n=p*p*q
             : (n,p,q) for private key, generate (d,module)
    
    """
    def __init__(self,tup):
        "Choose two large distinct primes p and q and compute N = (p**2) * q"
        if len(tup) == 1 :
            self.pubkey = tup[0]
            self.privkey = None
        elif len(tup) == 3 :
            n, p, q = tup
            assert n == pow(p,2)*q, 'Input private key raise error.'
            self.pubkey = n
            self.privkey = (invmod(self.pubkey,lcm(p-1,q-1)), p*q)
        else :
            raise ValueError('SchmidtSamoa(tup) : \n\t@tup : \n\t\t(n) for public key \n\t\t(n,p,q) for private key')

    def encrypt(self,m):
        "c = m**N % N  ( N = p**2 * q)"
        return pow(m,self.pubkey,self.pubkey)
        
    def decrypt(self,c):
        """
        m = c**d % pq
        """
        if self.privkey :
            d , module = self.privkey
            return pow(c,d,module)
        else :
            raise ValueError('Could not decrypt without privkey.')
    



class OkamotoUchiyama :
    """

    Implement from Wikipedia : https://en.wikipedia.org/wiki/Okamoto%E2%80%93Uchiyama_cryptosystem

    OkamotoUchiyama(tup) :
        @tup : (n,g,h) for public key, 

                n=p*p*q
                g**(p-1) mod p**2 != 1, 
                h = g**n mod n, 

        @tup : (n,g,h,p,q)
                
                p q are for private key, the factors of n

    """
    def __init__(self,tup):
        "Choose two large distinct primes p and q and compute N = (p**2) * q"
        n,g,h = tup[:3]
        if len(tup) >= 3 :
            self.n = n
            self.g = g
            self.h = h
            self.pubkey = (n,g,h)
        if len(tup) == 5 :
            p, q = tup[3:5]
            self.p = p
            self.q = q
            assert n == pow(p,2) * q, 'Input private key raise error.'
            self.privkey = (g,p,q)
        else :
            raise ValueError('OkamotoUchiyama(tup) : \n\t@tup : \n\t\t(n,g,h) for public key \n\t\t(n,g,h,p,q) for private key')

    def encrypt(self,m):
        """
        return (g ** m * h ** r) % n
        """
        n,g,h = self.pubkey
        r = getRandomRange(1,self.n-1)
        return pow(g,m,n) * pow(h,r,n) % n

    def decrypt(self,c):
        g,p,q = self.privkey
        return self.logarithm(pow(c,p-1,p**2)) * invmod(self.logarithm(pow(g,p-1,p**2)),p)% p
    
    def logarithm(self,x):
        'return L(X) = (X-1) // p'
        return (x-1) // self.p
    
    @classmethod
    def generate(cls,bits):
        p = getPrime(bits//3)
        q = getPrime(bits//3+ bits%3)
        n = p**2 * q
        while True:
            g = getRandomRange(1, n-1)
            g_p = pow(g, p-1, p**2)
            if pow(g_p, p, p**2) == 1:
                break
        h = pow(g,n,n)
        return cls((n,g,h,p,q))


class Rabin:
    def __init__():
        pass    
    def encrypt():
        pass
    def decrypt():
        pass

class NaccacheStern:
    def __init__():
        pass
    def encrypt():
        pass
    def decrypt():
        pass

class Paillier:
    """
    Implement from Wikipedia : https://en.wikipedia.org/wiki/Paillier_cryptosystem
    
    Paillier(tup) :
        @tup : (n,g) for public key, n=p*q, g is a random integer in field n*n
             : (n,g,p,q) for private key, generate (mu, phi)
    
    """
    def __init__(self,tup):
        "Choose two large distinct primes p and q and compute N = (p**2) * q"
        if len(tup) == 2 :
            self.pubkey = tup
        elif len(tup) == 4 :
            n, g = tup[:2]
            p, q = tup[2:]
            assert n == p*q, 'Input private key raise error.'
            self.pubkey = (n,g)
            phi = (p-1)*(q-1)
            mu = invmod(_L(pow(g,phi,n*n)),n)
            self.privkey = (n,phi,mu)
        else :
            raise ValueError('Paillier(tup) : \n\t@tup : \n\t\t(n,g) for public key \n\t\t(n,g,p,q) for private key')

    def _L(self, u) :
        return (u - 1) // self.pubkey[0]

    def encrypt(self,m):
        """
        return (g^m * r^n) % n^2
        """
        n,g = self.pubkey
        mods = n*n
        gm = pow(g,m,mods)
        r = 0
        while gcd(r,n) != 1 :
            r = random.randint(0,n-1)
        return (gm * pow(r,n,mods)) % mods
    
    def decrypt(self, c):
        n,phi,mu = self.privkey
        mes = pow(c,phi,n*n)
        mes = _L(mes)*mu % n
        return mes