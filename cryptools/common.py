
def xor_string(s1,s2):
    return ''.join([chr(ord(a) ^ ord(b)) for a,b in zip(s1,s2)])
