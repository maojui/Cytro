#-*- coding:utf-8 -*-

import unittest
import os
from cytro import *


class StringsTest(unittest.TestCase):
    
    def test_ns(self):
        s = b"long string to test"
        val = 2418187513319072758194084480823884981773628276
        self.assertEqual(s2n(s), val)
        self.assertEqual(n2s(val), s)
        self.assertRaises(TypeError, s2n, 100)
        self.assertRaises(TypeError, n2s, "qwe")

    def test_bs(self):
        a = os.urandom(100)
        b = "".join(map(chr, a))
        print(s2b(a) == s2b(b))
        a == b2s(s2b(a))
        self.assertEqual( a, B2s(B2s(a)))
        self.assertEqual( s2b(a), s2b(b) )
        self.assertEqual( b2s('10'), '\x02')
        self.assertEqual( b2s(b'10'), '\x02')
    
    def test_str_bits(self):
        while True :
            random_str = os.urandom(100)
            bit_rstr = bin(int.from_bytes(random_str,'big'))[2:]
            if len(bit_rstr) == 800 :
                break
        self.assertEqual( s2b(random_str), bit_rstr)
        self.assertEqual( b2s(bit_rstr), B2s(random_str))



if __name__ == "__main__":
    unittest.main()
