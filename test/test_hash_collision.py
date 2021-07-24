#!/usr/bin/env python
#-*- coding:utf-8 -*-

import unittest
import pathlib
import hashlib
from cytro.hash import *
from cytro.strings import s2B,randstr

current_path = pathlib.Path(__file__).parent.absolute()
class TestHash(unittest.TestCase) :

    def test_sha1_collision(self) :
        self.assertEqual(sha1_collision(
            os.path.join(current_path,'./res/otaku.jpg'),os.path.join(current_path,'./res/Sotaku.jpg')),True)
    
    def test_lea(self):
        k,o,a = [random.randint(1,100) for i in range(3)]
        key         = randstr(k)
        orig_data   = randstr(o)
        append_data = randstr(a)
        hash_dict = {
            # 'md5':hashlib.md5,
            'sha1':hashlib.sha1,
            'sha256':hashlib.sha256,
            'sha512':hashlib.sha512,
        }
        for name, algorithm in hash_dict.items():
            orig_hash = algorithm( s2B(key + orig_data) ).hexdigest()
            _hash = LEA.new(name)
            new_data = _hash.extend(append_data, orig_data, len(key), orig_hash)
            lea_hash = _hash.hexdigest()
            verify_hash = algorithm( s2B(key + new_data) ).hexdigest()
            self.assertEqual(lea_hash,verify_hash)

if __name__ == "__main__":
    unittest.main()
        