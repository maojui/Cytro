def get_phi(N):
    phi = N
    for f in factor(N):
        phi = phi * (1 - 1 / f[0])
    return phi

def get_roots(r,c,mod):
    rems = []
    if gcd( get_phi(mod), r) == 1:
        d = inverse_mod( r,get_phi(mod) )
        rems.append(int(pow(c, d, mod)))
    else:
        g = GF(mod).multiplicative_generator()
        u = int(g ** ((mod-1)/r))
        r1 = int(rth_root(r,c, mod))
        for i in range(r):
            rems.append( int(r1 * pow(u, i, mod) % mod) )
    return rems

def rth_root(c,p,root):
    rems = get_roots(root, c%p, p)
    for m in rems :
        if pow(m,root,p) != c :
            print('%d = m^%d mod %d, m has no integer solutions.' % (c,root,p) )
            exit()
    return rems
    
if __name__ == "__main__":
    # # Debug
    # p = random_prime(2^512-1,False,2^511)
    # x = randint(2^511,2^512) % p
    # e = random_prime(15)
    # c = pow(x,e,p)
    # print(f"{x}^{e} mod {p} = {c}")
    # rems = rth_root(c,p,e)
    # print(f'x = {rems}')
    # assert x in rems

    # Example 
    print("x^e mod p = c")
    c = int(input("c = "))
    p = int(input("p = "))
    e = int(input("e = "))
    rems = rth_root(c,p,e)
    print(f"x = {rems}")