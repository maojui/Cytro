def bacon_encode():
    pass

def bacon_decode(cipher):
    binary = ''.join([str(int(c.isupper())) for c in cipher if c.isalpha()])
    if len(binary)%5 != 0 :
        raise "Length Error : (%d), length must be multiples of 5."%len(binary)
    result = ''.join([chr(ord('A')+int(binary[i:i+5],2)) for i in range(0,len(binary),5)])
    return result
