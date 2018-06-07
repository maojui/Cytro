#!/usr/bin/env python
#-*- coding:utf-8 -*-

import unittest
from cryptools.strings import n2s
from Vulnerability import *
from cryptools.RSA import *

class TestRSA(unittest.TestCase) :

    def test_wiener(self) :
        n,e,*g = WienerVulnerability(1024)
        p,q    = wiener(n,e)
        self.assertEqual(p*q,n)
    
    def test_fermat_factorization(self):
        p = 103591
        q = 104729
        n = p*q
        pp,qq = fermat_factorization(n)
        print(pp,qq)
        self.assertEqual(n,pp*qq)

    def test_hastad_broadcast(self):
        p = 103591
        q = 104729
        m = 1234
        c1 = pow(m,3,p)
        c2 = pow(m,3,q)
        self.assertEqual(pow(m,3,p*q), hastad_broadcast([c1,c2],[p,q]))

    def test_boneh_durfee(self):
        flag = b'easyctf{keblftftzibatdsqmqotemmty}'
        n = 9247606623523847772698953161616455664821867183571218056970099751301682205123115716089486799837447397925308887976775994817175994945760278197527909621793469
        e = 27587468384672288862881213094354358587433516035212531881921186101712498639965289973292625430363076074737388345935775494312333025500409503290686394032069
        c = 7117565509436551004326380884878672285722722211683863300406979545670706419248965442464045826652880670654603049188012705474321735863639519103720255725251120
        d = boneh_durfee(n,e)
        self.assertEqual(flag,n2s(RSAKey((n,e,d)).decrypt(c)))