
#!/usr/bin/env python
#-*- coding:utf-8 -*-

import unittest
import hashlib
import random
from cytro.classical import bubble_babble_encode, bubble_babble_decode
from cytro.strings import n2s, randstr

class TestClassical(unittest.TestCase) :

    def test_knwon_bubble_babble(self):
        assert(bubble_babble_encode('Pineapple') == 'xigak-nyryk-humil-bosek-sonax')
        assert(bubble_babble_decode('xesef-disof-gytuf-katof-movif-baxux', True) == '1234567890')
        assert(bubble_babble_decode('xigak-nyryk-humil-bosek-sonax', True) == 'Pineapple')
    
    def test_bubble_babble(self):
        n = random.randint(0,100)
        test = randstr(n)
        x = bubble_babble_encode(test)
        assert(test == bubble_babble_decode(x))

if __name__ == '__main__':
    unittest.main()