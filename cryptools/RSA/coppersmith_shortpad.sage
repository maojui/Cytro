import sys
from sage.all import *
 
n = int(sys.argv[1])
e = int(sys.argv[2])
c1 = int(sys.argv[3])
c2 = int(sys.argv[4])

PRxy.<x,y> = PolynomialRing(Zmod(n))
PRx.<xn> = PolynomialRing(Zmod(n))
PRZZ.<xz,yz> = PolynomialRing(Zmod(n))
 
g1 = x**e - c1
g2 = (x + y)**e - c2
 
q1 = g1.change_ring(PRZZ)
q2 = g2.change_ring(PRZZ)
 
h = q2.resultant(q1)

# Need to switch to univariate polynomial ring because .small_roots is implemented only for univariate
h = h.univariate_polynomial() # x is hopefully eliminated
h = h.change_ring(PRx).subs(y=xn)
h = h.monic()
 
roots = h.small_roots(X=2**40, beta=0.3)
assert roots, "Failed."
 
diff = roots[0]
if diff > 2**32:
    diff = -diff
    c1, c2 = c2, c1

print(diff)
