#-*- coding:utf-8 -*-
import binascii
import io

def len_in_bits(n):
    """
    Return number of bits in binary representation of @n.
    """
    try:
        return n.bit_length() 
    except AttributeError:
        if n == 0:
            return 0
        return len(bin(n)) - 2

def hex2bytes(s):
    return binascii.unhexlify(s)

def s2hex(s):
    if type(s) == str :
        s = switchBS(s) 
    return binascii.hexlify(s)

def byte(x):
    s = io.BytesIO()
    s.write( bytearray( (x,) ) )
    return s.getvalue()

def s2n(s):
    """
    String to number.
    """
    if not len(s):
        return 0
    if type(s) == str :
        return int(''.join( hex(ord(c))[2:].rjust(2,'0') for c in s),16)
    if type(s) == bytes :
        return int.from_bytes(s,'big')

def n2s(n,byteorder='big'):
    """
    Number to string.
    """
    length = (len(hex(n))-1)//2
    return int(n).to_bytes(length=length,byteorder=byteorder)

def s2b(s):
    """
    String to binary.
    """
    ret = []
    if type(s) == type(b''):
        s = "".join(map(chr, s))
    for c in s:
        ret.append(bin(ord(c))[2:].zfill(8))
    return "".join(ret)
 
def switchBS(bs):
    """
    Switch bytes and string.
    """
    if type(bs) == type(b''):
        return "".join(map(chr, bs))
    return n2s(int(''.join( hex(ord(c))[2:].rjust(2,'0') for c in bs),16))
    
def b2s(b):
    """
    Binary to string.
    """
    ret = []
    if type(b) == bytes:
        b = switchBS(b)
    for pos in range(0, len(b), 8):
        ret.append(chr(int(b[pos:pos + 8], 2)))
    return ''.join(ret)

def xor_string(s1,s2):
    """
    Exclusive OR (XOR) @s1, @s2 byte by byte
    return the xor result with minimun length of s1,s2
    """
    if type(s1) != type(s2) :
        raise TypeError('Input must be the same type, both str or bytes.')
    if type(s1) == type(s2) == bytes :
        return b''.join([byte(a^b) for a,b in zip(s1,s2)])
    return ''.join([chr(ord(a) ^ ord(b)) for a,b in zip(s1,s2)])
