import re
from pycipher import Caesar

def brute_caesar(ct):
    """
    Show all possible 26 character decipher.
    """
    # make sure ciphertext has all spacing/punc removed and is uppercase
    ct = re.sub('[^A-Z]','',ct.upper())
    pts = []
    for i in range(26):
        pt = Caesar(i).decipher(ct)
        pts.append(pt)
        print(f'{i:02} : {pt}')
    return pts


class ExCaesar():
    
    def __init__(self, init="a", base=26):
        self.init = init
        self.base = base
        self._list = ''.join([chr(ord(init) + i) for i in range(base)])
    
    def decrypt(self, cipher, key):
        if not key < self.base :
            raise ValueError("key is not in the list.")
        p = ''
        
        for c in cipher :
            if c in self._list:
                p += chr(ord(self.init) + ((ord(c)-ord(self.init)) + key) % self.base)
            else :
                p += c
        return p