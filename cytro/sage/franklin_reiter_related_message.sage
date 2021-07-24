import sys

def franklin_reiter_related_message(n,e,c1,c2,r,a) :

    R.<X> = Zmod(n)[]
    f1 = X^e - c1
    f2 = (a*X + r)^e - c2

    def fun_gcd(a, b):
        if a == 0: return b
        if b == 0: return a
        print("Dimensionality reduction : ")
        while b:
            print(str(a.degree()))
            a, b = b, a % b
        return a.monic()

    return str(-fun_gcd(f1, f2).coefficients()[0])

