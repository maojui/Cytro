from cryptools.strings import xor_string

def CBC_XOR(cipher, origin, to) :
    """   
    Give : 
        @cipher : CBC cipher 
        @origin : origin plaintext
        @to     : fake plaintext
    """
    if len(cipher)%8 == 0 :
        raise Exception('Error block size')
        
    if not len(cipher) == len(origin) == len(to):
        raise Exception('cipher, origin plaintext, fake plaintext must be the same length.')

    return xor_string(xor_string(cipher,origin), to)
