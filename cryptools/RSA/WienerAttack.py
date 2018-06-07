

import sys
from sympy.solvers import solve
from sympy import Symbol

# This is comes from https://github.com/sourcekris/RsaCtfTool/blob/master/wiener_attack.py
# A reimplementation of pablocelayes rsa-wiener-attack 
# https://github.com/pablocelayes/rsa-wiener-attack/

class _WienerAttack(object):
    
    def rational_to_contfrac (self, x, y):
        a = x//y
        if a * y == x:
            return [a]
        else:
            pquotients = self.rational_to_contfrac(y, x - a * y)
            pquotients.insert(0, a)
            return pquotients

    def convergents_from_contfrac(self, frac):    
        convs = [];
        for i in range(len(frac)):
            convs.append(self.contfrac_to_rational(frac[0:i]))
        return convs

    def contfrac_to_rational (self, frac):
        if len(frac) == 0:
            return (0,1)
        elif len(frac) == 1:
            return (frac[0], 1)
        else:
            remainder = frac[1:len(frac)]
            (num, denom) = self.contfrac_to_rational(remainder)
            return (frac[0] * num + denom, num)

    def is_perfect_square(self, n):
        h = n & 0xF; 
        if h > 9:
            return -1 

        if ( h != 2 and h != 3 and h != 5 and h != 6 and h != 7 and h != 8 ):
            t = self.isqrt(n)
            if t*t == n:
                return t
            else:
                return -1
        
        return -1

    def isqrt(self, n):
        if n == 0:
            return 0
        a, b = divmod(n.bit_length(), 2)
        x = 2**(a+b)
        while True:
            y = (x + n//x)//2
            if y >= x:
                return x
            x = y

    def __init__(self, n, e):
        self.d = None
        self.p = None
        self.q = None
        sys.setrecursionlimit(100000)
        frac = self.rational_to_contfrac(e, n)
        convergents = self.convergents_from_contfrac(frac)
        
        for (k,d) in convergents:
            if k!=0 and (e*d-1)%k == 0:
                phi = (e*d-1)//k
                s = n - phi + 1
                discr = s*s - 4*n
                if(discr>=0):
                    t = self.is_perfect_square(discr)
                    if t!=-1 and (s+t)%2==0:
                        self.d = d
                        x = Symbol('x')
                        roots = solve(x**2 - s*x + n, x)
                        if len(roots) == 2:
                            self.p = roots[0]
                            self.q = roots[1]
                        break



# This is comes from https://github.com/sagi/code_for_blog/tree/master/2016/wieners-rsa-attack

# But too slow :((

# class WienerAttack2(object):
#     # Rational numbers have finite a continued fraction expansion.
#     def get_cf_expansion(self,n, d):
#         e = []
#         q = n // d
#         r = n % d
#         e.append(q)
#         while r != 0:
#             n, d = d, r           
#             q = n // d
#             r = n % d
#             e.append(q)
#         return e

#     def test_get_cf_expansion(self):
#         return cf_expansion(17993, 90581) == [0, 5, 29, 4, 1, 3, 2, 4, 3] 

#     def get_convergents(self,e):
#         n = [] # Nominators
#         d = [] # Denominators

#         for i in range(len(e)):
#             if i == 0:
#                 ni = e[i]
#                 di = 1
#             elif i == 1:
#                 ni = e[i]*e[i-1] + 1
#                 di = e[i]
#             else: # i > 1 
#                 ni = e[i]*n[i-1] + n[i-2]
#                 di = e[i]*d[i-1] + d[i-2]

#             n.append(ni)
#             d.append(di)
#             yield (ni, di)
    
#     def __init__(self, e, N):
#         self.p, self.q = None, None
#         cf_expansion = self.get_cf_expansion(e, N)
#         convergents = self.get_convergents(cf_expansion)
#         # print('[+] Found the continued fractions expansion convergents of e/N.')
#         # print('[+] Iterating over convergents; '
#         #         'Testing correctness through factorization.')
#         # print('[+] ...')
#         for pk, pd in convergents: # pk - possible k, pd - possible d
#             if pk == 0:
#                 continue;
#             possible_phi = (e*pd - 1)//pk
#             p = Symbol('p', integer=True)
#             roots = solve(p**2 + (possible_phi - N - 1)*p + N, p)
#             if len(roots) == 2:
#                 pp, qq = roots # pp - possible p, pq - possible q
#                 if pp*qq == N:
#                     self.p,self.q = pp,qq
#                 break    
