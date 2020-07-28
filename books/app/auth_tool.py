import struct

import scrypt

# the struct that we utilize.
_BASE = struct.Struct("!BBBB")


def _pack_data(n, r, p, salt, password_hash):
	return _BASE.pack(n, r, p, 16) + salt + password_hash


def _unpack_data(packed_data: bytes) -> tuple:
	n, r, p, salt_size = _BASE.unpack_from(packed_data)
	i = _BASE.size + salt_size
	salt = packed_data[_BASE.size:i]
	password_hash = packed_data[i:]
	return n, r, p, salt, password_hash


def hash_password(password: str, pepper: str, n: int = 12, r: int = 8, p: int = 1, salt_len: int = 16,
                  hash_len: int = 32) -> str:
	"""

	:param password:
	:param pepper:
	:param n:
	:param r:
	:param p:
	:param salt_len:
	:param hash_len:
	:return:
	"""
	import codecs
	from binascii import b2a_base64 as b64_encode
	from Crypto.Random import get_random_bytes
	salt: bytes = get_random_bytes(salt_len)
	password_hash = scrypt.hash(password + pepper, salt, 1 << n, r, p, hash_len)
	# since pycharm will basically select from it the raw data I might as well see if this'll work.
	# return _pack_data(n, r, p, salt, password_hash)
	return codecs.decode(b64_encode(_pack_data(n, r, p, salt, password_hash)).rstrip(), "utf-8")


def verify_password(password: str, pepper: str, verifier: str) -> bool:
	from binascii import a2b_base64 as b64_decode
	verifier = b64_decode(verifier)
	password_hash: bytes
	n, r, p, salt, password_hash = _unpack_data(verifier)
	new_hash = scrypt.hash(password + pepper, salt, 1 << n, r, p, len(password_hash))
	return new_hash == password_hash
