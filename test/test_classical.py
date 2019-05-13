
#!/usr/bin/env python
#-*- coding:utf-8 -*-

import unittest
from cytro.strings import n2s
from Vulnerability import *
from cytro.classical import *

class TestClassical(unittest.TestCase) :

    def bubble_babble_tests():
        assert(bb_encode('1234567890') == 'xesef-disof-gytuf-katof-movif-baxux')
        assert(bb_encode('Pineapple') == 'xigak-nyryk-humil-bosek-sonax')
        assert(bb_decode('xesef-disof-gytuf-katof-movif-baxux', True) == '1234567890')
        assert(bb_decode('xigak-nyryk-humil-bosek-sonax', True) == 'Pineapple')
