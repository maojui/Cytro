def rth_root(r,c,q):
	F = GF(q)
	R.<x> = PolynomialRing(F,'x')
	while 1:
		coeff = []
		fx = x**r
		for i in range(1,r) :
			fx -= F.random_element()*(x^(r-i))
		fx += ((-1)^r)*c
		fc = list(factor(fx))
		if len(fc) <= 1:
			power = 0
			for i in range(r) :
				power += q^i
			root = pow(x, power/r , fx)
			root %= x
			return int(root)

def get_phi(N):
	phi = N
	for f in factor(N):
		phi = phi * (1 - 1 / f[0])
	return phi

def get_roots(r,c,mod):
	rems = []
	if gcd( get_phi(mod), r) == 1:
		d = inverse_mod( r,get_phi(mod) )
		rems.append( int(pow(c, d, mod)))
	else:
		g = GF(mod).multiplicative_generator()
		u = int(g ** ((mod-1)/r))
		r1 = int(rth_root(r,c, mod))
		for i in xrange(r):
			rems.append( int(r1 * pow(u, i, mod) % mod) )
	print(rems)


if __name__ == '__main__':

    import sys

    c = int(sys.argv[1])
    p = int(sys.argv[2])
    root = int(sys.argv[3])

    print(get_roots(root,c%p,p))
