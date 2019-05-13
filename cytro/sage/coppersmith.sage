def long_to_bytes(data):
    data = str(hex(long(data)))[2:-1]
    return "".join([chr(int(data[i:i + 2], 16)) for i in range(0, len(data), 2)])
    
def bytes_to_long(data):
    return int(data.encode('hex'), 16)

def coppersmith(N,e,known_m,c,epsilon=1/30):
    P.<x> = PolynomialRing(Zmod(N), implementation='NTL')
    pol = (known_m + x)^e - c
    roots = pol.small_roots(epsilon=1/30)
    return roots


# N = int(sys.argv[1])
# e = int(sys.argv[2])
# known_m = int(sys.argv[3])     # known highbits
# c = int(sys.argv[4])
# epsilon = float(sys.argv[5])
# coppersmith(N,e,known_m,c,epsilon)