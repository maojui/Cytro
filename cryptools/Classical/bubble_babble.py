"""
From : http://www.wiki.yak.net/589

Bubble Babble :

Below, _|X|_ denotes the largest integer not greater than X.
Let the data to be encoded be D[1] ... D[K] where K is the length
of the data in bytes; every D[i] is an integer from 0 to 2^8 - 1.
First define the checksum series C[1] ... C[_|K/2|_] where

    C[1] = 1
    C[n] = (C[n - 1] * 5 + (D[n * 2 - 3] * 7 + D[n * 2 - 2])) mod 36

The data is then transformed into _|K/2|_ `tuples'
T[1] ... T[_|K/2|_] and one `partial tuple' P so that

    T[i] = <a, b, c, d, e>

where

    a = (((D[i * 2 - 3] >> 6) & 3) + C[i]) mod 6
    b = (D[i * 2 - 3] >> 2) & 15
    c = (((D[i * 2 - 3]) & 3) + _|C[i] / 6|_) mod 6
    d = (D[i * 2 - 2] >> 4) & 15; and
    e = (D[i * 2 - 3]) & 15.

The partial tuple P is

    P = <a, b, c>

where if K is even then

    a = (C[i]) mod 6
    b = 16
    c = _|C[i] / 6|_

but if it is odd then

    a = (((D[K] >> 6) & 3) + C[i]) mod 6
    b = (D[K] >> 2) & 15
    c = (((D[K]) & 3) + _|C[i] / 6|_) mod 6

The `vowel table' V maps integers between 0 and 5 to vowels as

    0 - a
    1 - e
    2 - i
    3 - o
    4 - u
    5 - y

and the `consonant table' C maps integers between 0 and 16 to
consonants as

    0 - b
    1 - c
    2 - d
    3 - f
    4 - g
    5 - h
    6 - k
    7 - l
    8 - m
    9 - n
    10 - p
    11 - r
    12 - s
    13 - t
    14 - v
    15 - z
    16 - x

"""
import re

BB_VOWELS = 'aeiouy'
BB_CONSONANTS = 'bcdfghklmnprstvzx'

def bb_encode(s):
    """
    The encoding E(T) of a tuple T = <a, b, c, d, e> is then the string  
        V[a] C[b] V[c] C[d] `-' C[e]
    
    Notice the encoding always begins & ends with "x", 
    so the elements of the encoding of `Pineapple' are not xigak nyryk humil bosek & sonax 
    but rather igak-n yryk-h umil-b osek-s & a final partial record ona .
    """
    buf, c, l = 'x', 1, len(s)
    for i in range(0, l + 2, 2):
        if i >= l:
            buf += f'{BB_VOWELS[c % 6]}{BB_CONSONANTS[16]}{BB_VOWELS[c // 6]}'
            break
        b1 = ord(s[i])
        buf += f'{BB_VOWELS[(((b1 >> 6) & 3) + c) % 6]}{BB_CONSONANTS[(b1 >> 2) & 15]}{BB_VOWELS[((b1 & 3) + (c // 6)) % 6]}'
        if i + 1 >= l:
            break
        b2 = ord(s[i + 1])
        buf += f'{BB_CONSONANTS[(b2 >> 4) & 15]}-{BB_CONSONANTS[b2 & 15]}'
        c = (c * 5 + b1 * 7 + b2) % 36
    buf += 'x'
    return buf

def bb_decode_sub(a1, a2, a3, offset, c):
    h = (a1 - (c % 6) + 6) % 6
    if h >= 4:
        return None, offset
    if a2 > 16:
        return None, offset + 1
    m = a2
    l = (a3 - (c//6) % 6 + 6) % 6
    if l >= 4:
        return None, offset + 2
    return h << 6 | m << 2 | l, offset

def bb_decode(s, exception = False):
    buf, c, l = '', 1, len(s)
    if l != 5 and l % 6 != 5:
        if exception: raise Exception('wrong bb "%s" length' % s)
        return None
    if s[0] != 'x':
        if exception: raise Exception('wrong bb "%s": must begin with "x"' % s)
        return None
    if s[-1:] != 'x':
        if exception: raise Exception('wrong bb "%s": must end with "x"' % s)
        return None
    ts = list(filter(None, re.split('(.{1,%d})' % 6, s[1:-1])))
    lt = len(ts) - 1
    for i in range(lt + 1):
        t = ts[i]
        p = i * 6
        tn = [BB_VOWELS.find(t[0]), BB_CONSONANTS.find(t[1]), BB_VOWELS.find(t[2])]
        if len(t) > 3:
            tn.append(BB_CONSONANTS.find(t[3]))
            tn.append('-')
            tn.append(BB_CONSONANTS.find(t[5]))
        t = tn
        if i == lt:
            if t[1] == 16:
                if t[0] != c % 6:
                    if exception: raise Exception('wrong bb "%s" at position %d (checksum: %d)' % (s, p, c))
                    return None
                if t[2] != int(c // 6):
                    if exception: raise Exception('wrong bb "%s" at position %d (checksum: %d)' % (s, p + 2, c))
                    return None
            else:
                b, wp = bb_decode_sub(t[0], t[1], t[2], p, c)
                if b is None:
                    if exception: raise Exception('wrong bb "%s" at position %d' % (s, wp))
                    return None
                buf += chr(b)
        else:
            b1, wp = bb_decode_sub(t[0], t[1], t[2], p, c)
            if b1 is None:
                if exception: raise Exception('wrong bb "%s" at position %d' % (s, wp))
                return None
            if t[3] > 16:
                if exception: raise Exception('wrong bb "%s" at position %d' % (s, p))
                return None
            if t[5] > 16:
                if exception: raise Exception('wrong bb "%s" at position %d' % (s, p + 2))
                return None
            b2 = (t[3] << 4) | t[5]
            buf += '%s%s' % (chr(b1), chr(b2))
            c = (c * 5 + b1 * 7 + b2) % 36
    return buf
