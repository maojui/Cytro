# partial_m.sage

n = 0x00bef498e6eb2cffe71312da47ab89d2c47db7438ea2cfa992ddddbc2a01978001fc51e286e6ebf028396cdb8b3323c60e6b9d50cd84187cf7f48e3875a2f0890f70b02333ad89db2923863ce146562286f63fb0a1d0198e3a6862ba5ac12e85a5c6d0d27cb1c81bdf69cc5bc95b8001a2f744517f9437b4ddd5a076fc0e9a5de1a7a268c40f31aa29e8dc27c0b3a182299ca7a9335b4bd4585452f6107c238e486c98dd73a5f9862e9e80b152f53381c72f897107551c281259ac3ee32c4b4f46cc03127d1bf699acd0266f3c6729253c70da0c69b1560fa172735709866b375b6eba294e1ce8b46fba798ba380080b4bf9603998cac199d9cd46e30ae8da9e7f
e = 3

m = randrange(n)
c = pow(m, e, n)

beta = 1
epsilon = beta^2/7

nbits = n.nbits()
kbits = floor(nbits*(beta^2/e-epsilon))
mbar = m & (2^nbits-2^kbits)
print "upper %d bits (of %d bits) is given" % (nbits-kbits, nbits)

PR.<x> = PolynomialRing(Zmod(n))
f = (mbar + x)^e - c

print m
x0 = f.small_roots(X=2^kbits, beta=1)[0]  # find root < 2^kbits with factor = n
print mbar + x0