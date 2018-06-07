
from cryptools import *
from CBCExploit import PaddingOracle
from pwn import *

HOST = 'localhost'
PORT = 2000
socket = remote(HOST,PORT)
socket.recvuntil('Can you decrypt it?\n')

cipher = 'JJCs0JMIYpLcqNDYtxM2a4quJihX4R3/xKqaWoxSXDvBFybQv1uG5x4k0/453ycfmkh2iZDk13aAPOvjyWsxrw=='
iv = '8whXbWqehnACf6tZ'

var = s2hex(base64.b64decode(cipher))
iv = s2hex(iv)
class Padding(PaddingOracle):
	def oracle(self, payload, iv, previous_resp, **kwargs):
		payload = base64.b64encode( hex2bytes(iv) + hex2bytes(payload))
		socket.sendline(payload)
		x = socket.recvuntil('\n')
		if x.find(b't')>-1 :
			return True, None
		else :
			return False, None

key_size = 16
po = Padding(key_size)

decrypted = po.decrypt(ciphertext=var,iv=iv,is_correct=True, known_plaintext=None)


#print decrypted

#want_it = 'hahahahahahahahahahahahahahahhah'
#want_it = po.add_padding(want_it).encode('hex')
#orig = po.add_padding(decrypted).encode('hex')

#print po.fake_ciphertext(new_plaintext=want_it, orginal_ciphertext=var, orginal_plaintext=orig, is_correct=True)
