shift = 460
outbits = 512 - shift
inpbits = 111
P = int("""
688059984333666246787910938723621381598729218850718755998907
412161535424331160661632770337782800635183362958339254636297
5490427453804091142854644316412663
""".replace('\n', ''))
seed = int("""
611568351255149368142901367257843725099270917450763311096507
355114332487651131579836372226229940559778129750601398194971
3431316382568201987118489728973776
""".replace('\n', ''))

R = IntegerModRing(P)
seed = R(seed)


print('[*] Loading data')
if True:
    with open('leaks.txt') as f:
        Os = list(map(int, f.read().splitlines()))
        assert len(Os) % 4 == 0
        Os = [Os[i:i+4] for i in range(0, len(Os), 4)]
        Os = list(zip(*Os))
        assert len(Os) == 4
else:
    # Fake data
    unk = R(getrandbits(inpbits))
    O, C, c = [], [], seed
    for i in range(50):
        C.append(c)
        O.append(int(unk * c) >> shift)
        c = c ** 2
    Os = [O]

print('[*] Running')
O = Os[0]
size = len(O)
print(size)
print(O)

print('[*] Building Coeffs')
C, c = [], seed
for i in range(size):
    C.append(c)
    c = c ** 2

print('[*] Building Matrix')
M = []
for c, o in zip(C, O):
    M.append([int(c), int(o) << shift])
M = Matrix(ZZ, M)
M = M.augment(-identity_matrix(size))
M = M.augment(-identity_matrix(size) * P)

print('[*] Building Lattice')
L = M.right_kernel_matrix()

print('[*] Reducing Lattice')
B = L.LLL()

print('[*] Finding answer')
for row in B:
    if int(row[0]) != 0:
        print(abs(row[0]))
        break
