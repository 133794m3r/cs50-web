from django.contrib.auth.hashers import BasePasswordHasher
import hashlib
import binascii
from django.utils.crypto import (get_random_string, constant_time_compare)
class ScryptPasswordHasher(BasePasswordHasher):

	algorithm = 'scrypt'
	#Parameters below are basically as high as Python will allow. It should equate to
	# around ~75ms on my machine. So on the server it should be ~13 logins/s possible per core.
	# So that should be good enough for the server.
	# will benchmark on the wimpy server I have to figure it out.
	# Current version utilizes ~32MiB of RAM.
	#n == 15, and 32MiB of ram means ~67ms per hash have to try on small google server.
	n = 15
	#may make this be 13. Each number higher results in 2MiB of more memory.

	r = 8
	p = 1
	dklen = 32
	#65MiB
	maxmem = 68157440
	def safe_summary(self, encoded: str) -> dict:
		"""
		Returns a summary of safe values.

		The result is a dictionary that will be used where the password field
		must be displayed to construct a safe representation of the password.

		:param encoded: The full encoded hash string.
		:return: The parameters.
		:rtype: dict
		:returns: All parameters exploded.
		"""
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


	def encode(self, password: str, salt: str, n: int = None, r: int = None, p: int = None, dklen: int = None) -> str:
		"""
		Secure password hashing using the scrypt algorithm.

		The default parameters are based upon it taking ~60ms


		:param password: The password to hash.
		:param salt: The salt value to utilize. Default is 16 characters(~98)
		:param n: The small n. Aka 1<<n for the iteration count.
		:param r: The memory factor to utilize.
		:param p: The parellism factor.
		:param dklen: how large the output hash should be.
		:returns: Hashed string
		:rtype: str
		"""
		salt = salt or get_random_string(16,'0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ!-_|#&%')
		n = n or self.n
		r = r or self.r
		p = p or self.p
		dklen = dklen or self.dklen
		N = 1 << n
		password = bytes(password,'utf-8')
		saltb = bytes(salt,'utf-8')
		hash = str(binascii.b2a_base64(hashlib.scrypt(password,salt=saltb,n=N,r=r,p=p,dklen=dklen,maxmem=self.maxmem)),'utf-8')
		return f"scrypt${salt}${n}${r}${p}${dklen}${hash}"


	def decode(self, encoded: str) -> dict:
		"""
		This method will decode the hash into it's component parts so that it can be verified.

		:param encoded: The hashed password you want to decode.
		:return: The hash split to all of the values.
		:returns: String exploded.
		:rtype: dict

		"""
		algorithm,salt,n,r,p,dklen,hash = encoded.split('$')
		assert algorithm == self.algorithm
		return {
			'algorithm':algorithm,
			'salt':salt,
			'n':int(n),
			'r':int(r),
			'p':int(p),
			'dklen':int(dklen),
			'hash':hash
		}


	def verify(self, password: str, encoded: str) -> bool:
		decoded = self.decode(encoded)
		encoded_2 = self.encode(password,decoded['salt'],decoded['n'],decoded['r'],decoded['p'],decoded['dklen'])
		return constant_time_compare(encoded,encoded_2)


	def must_update(self,encoded):
		algorithm,salt,n,r,p,dklen,hash = encoded.split('$')
		assert algorithm == self.algorithm
		return [self.n,self.r,self.p,self.dklen]  != [n,r,p,dklen]


	def harden_runtime(self, password, encoded):
		#Way too complex to do this honestly.
		pass