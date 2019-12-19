# cytro.CBC

In this module provides several methods to try with CBC encryption.

- Bitflips Attack
- Padding Oracle
- POODLE

Usage : 

```python

class Exploit(PaddingOracle):

    def oracle(self, payload, iv, previous_resp, **kwargs):
        r = sendPayload(iv + payload)
        if b'Padding decrypted OK:' in r:
            return True, None
        else :
            return False, None

blocksize = 8
exp = Exploit(blocksize)
decrypted = exp.decrypt(ciphertext=raw_cipher, iv=raw_iv, is_correct=True, known_plaintext=b'\x02\x02')

```