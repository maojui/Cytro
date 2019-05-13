#!/usr/bin/env python
#-*- coding:utf-8 -*-

import unittest
from cytro import *

class TestHash(unittest.TestCase) :

    def test_sha1_collision(self) :
        self.assertEqual(sha1_collision('./test/otaku.jpg','./test/Sotaku.jpg'),True)
    
    def test_lea(self):
        key         = b'flag.' * 3
        orig_data   = b'hello'
        append_data = b'XD'
        for algorithm in [hashlib.md5, hashlib.sha1, hashlib.sha256, hashlib.sha512] :
            orig_hash = algorithm(key + orig_data).hexdigest()
            lea_hash, new_data = LEA(orig_hash,orig_data,append_data,len(key))
            verify_hash = algorithm(key + new_data).hexdigest()
            self.assertEqual(lea_hash,verify_hash)

        