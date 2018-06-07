import sys

n = int(sys.argv[1])
e = int(sys.argv[2])
c1 = int(sys.argv[3])
c2 = int(sys.argv[4])
r = int(sys.argv[5])
a = int(sys.argv[6])

R.<X> = Zmod(n)[]
f1 = X^e - c1
f2 = (a*X + r)^e - c2

def fun_gcd(a, b):
    if a == 0: return b
    if b == 0: return a
    # print("Dimensionality reduction : ")
    while b:
        # print(str(a.degree()))
        a, b = b, a % b
    return a.monic()

print(-fun_gcd(f1, f2).coefficients()[0])
