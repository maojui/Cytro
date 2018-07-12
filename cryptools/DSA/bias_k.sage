import hashlib
import sys

# p = sys.argv[1]
# q = sys.argv[2]


p = 145774370140705743619288815016506936272601276321515267981294709325646228235350799641396853482542510455702593145365689674776551326526283561120782331775753481248764911686023024656237178221049671999816376444280423000085773391715885524862881877222848088840644737895543531766907185051846802894682811137086905085419
q = 739904609682520586736011252451716180456601329519

# The DSA algorithm involves two rings: the integers modulo p and the integers modulo q
Rp = Integers(p)
Rq = Integers(q)

y = Rp(128135682856750887590860168748824430714190353609169438003724812869569788088376999153566856518649548751808974042861313871720093923966663967385639616771013994922707548355367088446112595542221209828926608117506259743026809879227606814076195362151108590706375917914576011875357384956337974597411261584032533163073)
g = Rp(52865703933600072480340150084328845769706702669400766904467248075164948743170867377627486621900744105555465052783047541675343643777082719270261354312243195450389581166294097053506337884439282134405767273312076933070573084676163659758350542617531330447790290695414443063102502247168199735083467132847036144443)

# y = Rp( int(sys.argv[3]) )
# g = Rp( int(sys.argv[4]) )



datafile = 'rs_pairs.txt'

msb = False # modify exploit to work for variant problem where most sig. byte is 0
if msb:
  datafile = 'rs_pairs_msb.txt'

rs_pairs = []
with open(datafile, 'r') as f:
  for line in f:
    r, s = line.strip().split(', ')
    r, s = Rq(int(r)), Rq(int(s))
    rs_pairs.append((r,s))

def get_hash(cmd):
  return int(hashlib.sha1(cmd).hexdigest(), 16)

# Verify
r, s = rs_pairs[0]
h = Rq(get_hash('ls' + 'A' * (256 - 2)))
w = 1/s
u1 = w * h
u2 = w * r
v = Rq(pow(g, u1) * pow(y, u2))
assert v == r

# Construct lattice
n = 100 # This can be as low as 66 for the original problem, or 78 for the MSB variant
rs_pairs = rs_pairs[:n]
L = pow(2, 8)
if msb:
  L = 1

T = vector([int(r  / (L * s)) for (r, s) in rs_pairs])
U = vector([int(-h / (L * s)) for (r, s) in rs_pairs])
Q = q * matrix.identity(n)

sT = 1
sU = 1
vT = vector([0 for _ in range(n + 2)])
vU = vector([0 for _ in range(n + 2)])
vT[-2] = sT
vU[-1] = sU

'''
        [           | |   | ]
        [    q*I    | 0   0 ]
        [           | |   | ]
    M = [-----------+-------]
        [ --- T --- | sT  0 ]
        [ --- U --- | 0  sU ]
'''

M = Q.stack(T).stack(U).augment(vT).augment(vU)
B = M.LLL()

x = 1
for i, v in enumerate(B):
  if v[-1] == sU:
    x = Rq(-v[-2] / sT)
    break

# Check correctness
assert pow(g, x) == y
print('x: {}'.format(x))

# Sign message 'cat'
h = get_hash('cat')
k = Rq(1234567)
r = Rq(pow(g, k))
s = (h + x * r) / k
print('r: {}'.format(r))
print('s: {}'.format(s))