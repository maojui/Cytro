#-*- coding:utf-8 -*-
import io
import random
import string
import binascii

def chunk(s, size, padding=None) :
    pad = ''
    if padding != None :
        pad_size = size - (len(s) % size)
        if ( type(padding) == str or type(padding) == bytes ) :
            if len(padding) == 1 :
                pad = padding * pad_size
            elif len(padding) == pad_size :
                pad = padding
            else :
                raise TypeError(f"Error padding size, {pad_size} bytes leave.")
            s += pad
    return [s[i:i+size] for i in range(0,len(s),size)]

def bits(n, length=0) :
    return bin(n)[2:].rjust(length,'0') 

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

def h2B(s):
    return binascii.unhexlify(s)

def s2h(s):
    if type(s) == str :
        s = B2s(s) 
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

def s2B(ss):
    """
    Switch string and bytes.
    """
    if type(ss) == bytes :
        return ss
    return bytes([ord(c) for c in ss])

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
 
def B2s(bs):
    """
    Switch bytes and string.
    """
    if type(bs) == type(b''):
        return "".join(map(chr, bs))
    else :
        return bytes([ord(c) for c in bs])
    
def b2s(b):
    """
    Binary to string.
    """
    ret = []
    if type(b) == bytes:
        b = B2s(b)
    for pos in range(0, len(b), 8):
        ret.append(chr(int(b[pos:pos + 8], 2)))
    return ''.join(ret)


def randstr(length):
   letters = string.ascii_letters + string.digits
   return ''.join(random.choice(letters) for i in range(length))

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
