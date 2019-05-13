import sys

def cube_root(c, q):
    F = FiniteField(q)
    R.<x> = PolynomialRing(F,'x')
    while 1:
        a = F.random_element()
        b = F.random_element()
        fx = x**3 - a*x**2 + b*x - c
        fc = list(factor(fx))
        if len(fc) <= 1:
            root = pow(x, (q**2+q+1)//3, fx)
            root %= x
            return int(root)

def cube_roots(c,mod):
    c = c % mod
    rems = []
    if gcd( (mod-1), 3) == 1:
        d = inverse_mod(3, mod - 1)
        rems.append( int(pow(c, d, mod)) )
    else:
        g = GF(mod).multiplicative_generator()
        u = int(g ** ((mod-1)//3))
        r1 = int(cube_root(c, mod))
        for i in xrange(3):
            rems.append( int(r1 * pow(u, i, mod) % mod) )
    for m in rems :
        if pow(m,3,p) != c :
            print('%d = m^3 mod %d, m has no integer solutions.' % (c,p) )
            exit()
    return [str(r).replace('L','') for r in rems]


if __name__ == '__main__':
    import sys

    c = int(sys.argv[1])
    p = int(sys.argv[2])
    rems = cube_roots(c%p,p)
    print(rems)
