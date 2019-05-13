from cytro import *

class PaddingOracle:
        
    def __init__(self, key_size=16):
        if key_size%8!=0:
            raise ValueError("Incorrect key length: %d",key_size)
        self.key_size=key_size

    def oracle(self, payload, iv, previous_resp, **kwargs):
        """
        payload - hex encoded ciphertext to check
        iv - hex encoded inicialization vector (most often: append it at beggining of payload)
        previous_resp - value returned by previous call to oracle
        Return tuple: (True/False, response)
        True if padding is correct, Flase otherwise; Be carefull while sending original ciphertext
        response will be send as previous_response to next call
        """
        raise NotImplementedError

    def decrypt(self, ciphertext, iv=None, amount=0, is_correct=False, known_plaintext=None, **kwargs):
        """
        ciphertext - hex encoded
        iv - usually it's first block of ciphertext, but may be specified separate
        amount - how much blocks decrypt (counting from last), default is all
        is_correct - if True, then first decrypted byte will be treated as correct padding (speed up decryption)
        known_plaintext - hex encoded, with padding, from end
        kwargs - push forward to oracle function
        Return hex encoded plaintext
        """

        ciphertext = hex2bytes(ciphertext)
        
        if len(ciphertext)%self.key_size!=0:
            raise ValueError("Incorrect ciphertext length: %d"%(len(ciphertext)))

        #prepare blocks
        blocks = re.findall(b'.{%d}'%(self.key_size), ciphertext, re.DOTALL)

        resp = None
        if iv != None:
            log.info("Set iv")
            iv = hex2bytes(iv)
            log.info("iv is : %s"%iv)
            blocks.insert(0,iv)

        if amount!=0:
            amount=len(blocks)-amount-1

        if amount<0 or amount>=len(blocks):
            raise ValueError("Incorrect amount of blocks to decrypt: %d (have to be [0,%d)"%(amount,len(blocks)))
        
        #add known plaintext
        plaintext = ''
        position_known = 0
        FIRST_MODIFY = False

        if known_plaintext != None :
            if len(known_plaintext) == 0:
                raise ValueError("Knowing plaintext cannot be empty, must be None or bytes."%(amount,len(blocks)))
            else :
                FIRST_MODIFY=True
                kp = hex2bytes(known_plaintext)
                print(kp)
                plaintext = kp
                blocks_decoded = len(kp)//self.key_size
                chars_decoded = len(kp) % self.key_size
                if blocks_decoded>=len(blocks):
                    raise RuntimeError("Too long known plaintext (%d blocks)" % blocks_decoded)
                blocks = blocks[:len(blocks)-blocks_decoded]
                position_known = chars_decoded


        for count_block in range(len(blocks)-1, amount, -1):
            # For every block 
            payload_prefix = b''.join(blocks[:count_block-1])
            
            if FIRST_MODIFY :
                FIRST_MODIFY = False
                payload_modify = blocks[-2][:-position_known]+xor(kp[:position_known],blocks[-2][-position_known:],position_known+1)
            else :
                payload_modify = blocks[count_block-1]

            payload_decrypt = blocks[count_block]

            position = self.key_size-1-position_known
            position_known = 0
            while position >= 0 :
                # Every position in block 

                for one in range(256):
                    modified = payload_modify[:position] + byte(one) + payload_modify[position+1:]
                    
                    payload = b''.join([payload_prefix, modified, payload_decrypt])
                    iv = s2hex(payload[:self.key_size])
                    payload = s2hex(payload[self.key_size:])
                    is_ok = False

                    correct, resp = self.oracle(payload=payload, iv=iv, previous_resp=resp, **kwargs)
                    if correct :
                        """ oracle return True """
                        padding = self.key_size-position
                        
                        decrypted_char = byte(payload_modify[position]^one^padding)
                        if is_correct == True and count_block == len(blocks)-1 and position == self.key_size-1 and known_plaintext == None:
                            """ Have original padding value, can skip some bytes """
                            dc = ord(decrypted_char)
                            # log.info("Found padding value: %d", dc)
                            if dc == 0 or dc > self.key_size:
                                raise RuntimeError("Found bad padding value (given ciphertext may not be correct)")

                            plaintext = decrypted_char*dc
                            payload_modify = payload_modify[:-dc] + xor(payload_modify[-dc:],dc,dc+1)
                            position = position-dc+1
                        else:
                            payload_modify = payload_modify[:position] + xor(byte(one) + payload_modify[position+1:], padding, padding+1)
                            plaintext = decrypted_char+plaintext

                        is_ok = True
                        print('Plaintext: %s'% plaintext,end='\r')
                        break
                position -= 1
                if is_ok == False:
                    raise RuntimeError("Can't find corrent padding (oracle function return False 256 times)")
        
        return s2hex(plaintext)
