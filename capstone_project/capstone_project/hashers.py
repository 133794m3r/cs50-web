from django.contrib.auth.hashers import BasePasswordHasher
import hashlib
import binascii
from django.utils.crypto import (get_random_string, constant_time_compare)
class ScryptPasswordHasher(BasePasswordHasher):
	self.algorithm = 'scrypt'
	self.n = 14
	self.r = 15
	self.p = 8
	self.dklen = 32
	def safe_summary(self, encoded):
		decoded = self.decode(encoded)
		return {
			_('algorithm'):decoded['algorithm'],
			_('n'):decoded['n'],
			_('r'):decoded['r'],
			_('p'):decoded['p'],
			_('dklen'):decoded['dklen'],
			_('hash'):mask_hash(decoded['hash']),
			_('salt'):mask_hash(decoded['salt'])
		}


	def encode(self, password, salt,n,r,p,dklen):
		salt = salt or super().salt()
		n = n or self.n
		r = r or self.r
		p = p or self.p
		dklen = dklen or self.dklen
		n = 1 << n
		password = bytes(password,'utf-8')
		saltb = bytes(salt,'utf-8')
		hash = str(binascii.b2a_base64(hashlib.scrypt(password,salt=saltb,n=n,r=r,p=p,dklen=dklen)),'utf-8')
		return f"scrypt${salt}${n}${r}${p}${dklen}${hash}"

	def decode(self,encoded):
		algorithm,salt,n,r,p,dklen,hash = encoded.split('$')
		assert algorithm == self.algorithm
		return {
			'algorithm':algorithm,
			'salt':salt,
			'n':n,
			'r':r,
			'p':p,
			'dklen':dklen,
			'hash':hash
		}

	def verify(self, password, encoded):
		decoded = self.decode(encoded)
		encoded_2 = self.encode(password,decoded['salt'],decoded['n'],decoded['r'],decoded['p'],decoded['dklen'])
		return constant_time_compare(encoded,encoded_2)

	def harden_runtime(self, password, encoded):
		pass