
from ..formula import gcd
from ..modular import invmod  


class LFSR:

    def __init__(self, register, taps):
        '''
        LFSR(register,taps)
        @register (seed) - initial value : [0,1,0,0,1,0 ... , 1] (integer array)
        @taps - XOR'd sequentially with the output bit and then fed back into the leftmost bit : [0,1,0 ... , 1] (integer array) 
        '''
        self.register = register
        self.taps = taps
        # assert max(taps) <= len(register), "Taps' length is greater than register ??"
        self.n = len(register)

    def next(self):
        '''
        pop out the rightmost bit and xor'd sequentially with the output bit and then fed back into the leftmost bit.
        '''
        ret = self.register[0]
        new = 0
        for i in self.taps:
            new ^= self.register[i]
        self.register.append(new)
        self.register = self.register[1:]
        # print(self.register)
        return ret

def Berlekamp_Massey_algorithm(sequence):
    """
    Berlekamp_Massey_algorithm:

    Copyright (C) 2012 Bo Zhu http://about.bozhu.me

    Permission is hereby granted, free of charge, to any person obtaining a
    copy of this software and associated documentation files (the "Software"),
    to deal in the Software without restriction, including without limitation
    the rights to use, copy, modify, merge, publish, distribute, sublicense,
    and/or sell copies of the Software, and to permit persons to whom the
    Software is furnished to do so, subject to the following conditions:

    The above copyright notice and this permission notice shall be included in
    all copies or substantial portions of the Software.

    THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
    IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
    FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL
    THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
    LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
    FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER
    DEALINGS IN THE SOFTWARE.

    The Berlekamp–Massey algorithm is an algorithm that will find the shortest linear feedback shift register (LFSR) for a given binary output sequence. The algorithm will also find the minimal polynomial of a linearly recurrent sequence in an arbitrary field. The field requirement means that the Berlekamp–Massey algorithm requires all non-zero elements to have a multiplicative inverse.

    Input the bit sequence x ([0,0,1,0,1, .... ])
    return the minimal polynomial of a linearly recurrent sequence
    """
    N = len(sequence)
    s = sequence[:]

    for k in range(N):
        if s[k] == 1:
            break
    f = set([k + 1, 0])  # use a set to denote polynomial
    l = k + 1

    g = set([0])
    a = k
    b = 0

    for n in range(k + 1, N):
        d = 0
        for ele in f:
            d ^= s[ele + n - l]

        if d == 0:
            b += 1
        else:
            if 2 * l > n:
                f ^= set([a - b + ele for ele in g])
                b += 1
            else:
                temp = f.copy()
                f = set([b - a + ele for ele in f]) ^ g
                l = n + 1 - l
                g = temp
                a = b
                b = n - l + 1

    # output the polynomial
    def print_poly(polynomial):
        result = ''
        lis = sorted(polynomial, reverse=True)
        for i in lis:
            if i == 0:
                result += '1'
            else:
                result += 'x^%s' % str(i)

            if i != lis[-1]:
                result += ' + '

        return result

    return (print_poly(f), l, f)

def known_keystream():
    pass

def non_consecutive_keystream(sequence, dist, keylength=0):
    '''
    @sequence : first bit at the leftmost.
    '''
    poly, n, f = Berlekamp_Massey_algorithm(sequence)
    print(poly,n,f)
    sequence = sequence[:n]
    period = (1<<n) - 1
    taps = sorted(list(f))[:-1]
    lfsr = LFSR(sequence,taps)
    # return lfsr 
    # if k <= 40 :
    #     pass
    # elif k <= 75 :
    #     # baby-step/giant-step
    #     pass
    # else :
    #     pass
    
    assert gcd(dist,period) == 1
    mi = invmod(dist,period)

    c = []
    for i in range(1<<n):
        c.append(lfsr.next())


    if keylength == 0 :
        keystream = [None] * (1<<n)
        for i in range(1<<n):
            keystream[i] = c[(i * mi) % period]
        print(Berlekamp_Massey_algorithm(keystream))
        return c, keystream
    else :
        keystream = [None] * keylength
        for i in range(keylength):
            keystream[i] = c[(i * mi) % period]
        print(Berlekamp_Massey_algorithm(keystream))
        return c,keystream
    
    
    
#  [0, 1, 1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 1, 0, 1, 1, 1, 0, 1, 1, 1, 0, 1, 1, 0, 1, 0, 1, 1]
register = [1, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 0, 1, 1, 0, 1, 0, 1, 1, 0, 0, 0, 0, 1, 0, 1, 1, 1, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 1, 0, 1, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 1, 0, 0, 1, 0, 0, 1, 1, 0, 1, 1, 1, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 1, 1, 0, 0, 1, 0, 1, 1, 0, 1, 1, 0, 0, 1, 0, 1, 1, 1, 0, 0, 1, 0, 0, 1, 1, 1, 1, 1, 1, 0, 1, 0, 0, 1, 0, 1, 1, 0, 1, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 1, 1, 1, 1, 1, 1, 0, 1, 0, 1, 1, 1, 0, 1, 1, 1, 0, 0, 0, 0, 0, 0, 1, 0, 0, 1, 1, 0, 0, 0, 1, 0, 0, 1, 0]
ans =   [1, 0, 0, 0, 0, 0, 1, 1, 0, 1, 1, 1, 0, 1, 1, 1, 0, 1, 1, 0, 1, 0, 1, 1]
# https://crypto.stackexchange.com/questions/59856/find-a-lfsr-given-2n-or-more-non-consecutive-keystream-bits
# period = pow(2,16) - 1

# m = 8
# mi = invmod(m,period)
# keystream = [None] * (len(binary)-6)
# assert gcd(m,period) == 1
# for i in range(len(binary)-6):
#     if i < 100 :
#         print('b' + str(i), '= c' + str((i * mi) % period))

#     keystream[i] = seq[(i * mi) % period]