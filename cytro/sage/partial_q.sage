
n = 2062521684938364459387498432429946594318125528980549199356976621583932152727232193909641817297183895615845700210175832265356957753985436563959942957952186855195131118549518451899418177389429804334409624918942126922696191728934268038066970010450960060605601284346526760357177120663929662244482217738116522078301
e = 65537

p = isqrt(4*n)

beta = 0.5
epsilon = beta^2/7

pbits = p.nbits()
kbits = floor(n.nbits()*(beta^2-epsilon))
pbar = p & (2^pbits-2^kbits)
print("upper %d bits (of %d bits) is given" % (pbits-kbits, pbits))

PR.<x> = PolynomialRing(Zmod(n))
f = x + pbar
print(pbar)
# print p
x0 = f.small_roots(X=2^kbits, beta=0.3)[0]  # find root < 2^kbits with factor >= n^0.3

print (x0)
print (pbar)
print (x0 + pbar)
print is_prime(x0 + pbar)