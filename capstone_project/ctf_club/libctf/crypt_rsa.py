"""
Crypto Lab Library - RSA Library

This contains all of the functions to deal with the most common RSA attacks
and also the utilities required to do that.

Macarthur Inbody <admin-contact@transcendental.us>
LGPLv3 or Later (2019 - 2020)
"""

#This does the hard work of actually getting you the plaintext back via the
# common modulus attack. All you need to supply is both exponents, both cipher-
# texts. Then the common Modulus.
from .crypt_math import *


def calc_r(n:int ) -> int:
	"""
	Calculates the value r such that it is co-prime with n and is also itself prime.

	:param n: The modulus n.
	:return: the integer r.
	"""

	from math import gcd
	r=get_prime(8)
	while gcd(r,n) != 1:
		r=get_prime(8)
	if gcd(r,n) != 1:
		r=get_prime(8)
	return r

def common_modulus_attack(c1: int, c2: int, e1: int, e2: int, n: int) -> int:
	"""
	This functionw will carry out the common modulus attack.

	:param c1: Ciphertext integer 1.
	:param c2: Ciphertext integer 2.
	:param e1: encryption exponent 1.
	:param e2: encryption exponent 2.
	:param n: The modulus n.
	:return: The plaintext integer P.
	"""

	if gcd_fast(e1,e2)[0] != 1:
		raise ValueError('e1 and e2 are invalid.')
	a=mod_inv(e1,e2)
	b=(gcd_fast(e1,e2)[0] - e1 * a ) // e2
	i=mod_inv(c2, n)
	mx=pow(c1, a, n)
	my=pow(i, -b, n)

	return (mx*my) % n

# Radford ASCII Decoder
# This function decodes a number into a 7bit ASCII string and returns said string.
def naive_ascii_decode(encoded_number: str, length: int) -> str:
	"""
	This function will decode an integer into a str if it's been encoded with
	naive ASCII encoding.

	:param encoded_number: The encoded integer as a string.
	:param length: The length(in bytes that the output string should be).
	:return: The decoded string.
	"""

	j=0
	output_str=''
	length=length-1

	for i in range(0,length):
		tmp=encoded_number[j]
		if tmp == '1':
			chars=3
		else:
			chars=2

		tmp=encoded_number[j:j+chars]
		val=int(tmp)

		output_str=output_str+chr(val)
		j=j+chars
		if len(encoded_number[j:]) < 2:
			break

	return output_str


# Encodes any string of ASCII(7bit) characters into a number the way that Radford has
# done it for the chal.
def naive_ascii_encode(string_to_encode: str, string_length: int) -> str:
	"""
	Encodes an ASCII string with naive ascii encoding. Where each byte of
	the string is encoded into the ASCII code point and then combined
	together into a string representation of that integer.

	:param string_to_encode: The input string.
	:param string_length: The length of the string.
	:return: The encoded string.
	"""

	output_str=''

	for i in range(0,string_length):
		tmp=ord(string_to_encode[i:i+1])
		tmp_str=str(tmp)
		output_str=output_str+tmp_str

	encoded_number=output_str

	return encoded_number


# this decodes a string of bytes(ASCII text only really otherwise you need to convert it
# to a byte stream.
def rsa_ascii_encode(string_to_encode:str,string_length:int) -> int:
	"""
	OS2IP aka RSA's standard string to integer conversion function.

	:param string_to_encode: The input string.
	:param string_length: How many bytes the string is.
	:return: The integer representation of this string.
	"""
	x=0
	string_to_encode=string_to_encode[::-1]
	i=0
	while i<string_length:
		tmp=ord(string_to_encode[i:i+1])
		x+=(tmp*pow(256,i))
		i+=1

	return x


#This converts the number to a string out of it.
def rsa_ascii_decode(x:int,x_len:int) -> str:
	"""
	I2OSP aka RSA's standard ascii decoder. Decodes the integer X into
	multiple bytes and finally converts those ASCII codepoints into an
	ASCII string.

	:param x: Integer X to be converted to string.
	:param x_len: the length that the string will be.
	:return: A string which represents teh decoded value of X.
	"""

	X = []
	string=''
	#max_len=len(x)
	if x>=pow(256,x_len):
		raise ValueError('Number is too large to fit in output string.')

	while x>0:
		X.append(int(x % 256))
		x //=256
	for i in range(x_len-len(X)):
		X.append(0)
	X=X[::-1]
	for i in range(len(X)):
		string+=chr(X[i])

	return string


# consistent for the library.
def get_prime(prime_length:int) -> int:
	"""
	Returns a prime number. Doing it this way to require less modules.

	:param prime_length: The length in bits that the prime has to be.
	:return: A prime integer.
	"""

	from secrets import randbits
	from sympy import isprime

	num = randbits(prime_length)
	while not isprime(num):
		num = randbits(prime_length)
	return num


# creates and returns p,q, and N. of length prime_length
# prime_length is a value of 2**prime_length. Aka the bits for prime length
# and returns both p and q. Both of which are that length in bits. Then we
# multiply p and q to get the value.
# This could be done via built-in C functions but it's best to visualize
# how it's working so people understand it.

def calc_n(prime_length:int) -> int:
	"""
	Creates and returns p,q, and N of length prime_length.

	:param prime_length: The number of bits that the value N should be.
	:return:
	"""
	prime_length = prime_length // 2
	p=get_prime(prime_length)
	q=get_prime(prime_length)
	while p == q:
		q=get_prime(prime_length)

	N=p*q

	return p, q, N


def calc_e(prime_length: int, lambda_n: int) -> int:
	from math import gcd
	"""
	Creates the value e such that 0 < e < lambda_n
	We only chose prime numbers so that we can simply check if there
	are any common divisors between e and lambda_n and if there are not
	they are coprime and share no divisors and the value works.
	
	:param prime_length: The length for the prime in bits.
	:param lambda_n: The LAMBDA(N) value(or PHI(N))
	:return: the prime e that'll work with RSA.
	"""

	coprime=0
	e=0
	while coprime!=1:
		e=get_prime(prime_length)
		coprime=gcd(e, lambda_n)

	return e


def calc_lambda(p: int,q: int) -> int:
	"""
	This function implements carmicheal's totient to get the value utilized
	for generating the multiplicative inverses later on in the rsa setup.

	:param p: the prime p
	:param q: the prime q
	:return: the totient value.
	"""

	lambda_n=fast_lcm(p-1,q-1)
	return lambda_n


def calc_d(e: int, lambda_n: int) -> int:
	"""
	calc_d

	Calculates the private key d wherein the following conditions are met.
	d=(e**-1) mod lamda_n. Thus d*e = 1 % lamda_n
	It utilizes previously defined functions for the calculation and works with
	the test vectors.

	:param e: the public key exponent.
	:param lambda_n: the Carmachael's lambda of n.
	:return: the decryption exponent.
	"""

	d=mod_inv(e, lambda_n)

	return d


def rsa_encrypt(m: int, e: int, n: int) -> int:
	"""
	rsa_encrypt

	Calculates the ciphertext using the pure math model for RSA Encryption.
	Via the following formula. c=(m**e) % N
	Returns the cipher number c.

	:param m: the plaintext message.
	:param e: the encryption exponent.
	:param n: the modulus.
	:return: The ciphertext integer.
	"""

	c=pow(m, e, n)

	return c


def rsa_decrypt(c: int, d: int, n: int) -> int:
	"""

	Implements RSA Decryption via the mathematical formula.
	The formula is m=(c**d) % N
	Returns the plain "text" really integer representation of the value.

	:param c: Ciphertext integer.
	:param d: the private key exponent.
	:param n: the modulus.
	:return: the plaintext integer M.
	"""

	m=pow(c, d, n)
	return m


def crt_e_maker(e: int, n_len: int = 256) -> tuple:
	"""
	creates the value for e for the chinese remainder theory attack aka the
	hastaad broadcast attack. It will make sure that n works with the provided
	e instead of the other way around.

	:param e: the public key exponent
	:param n_len: the length of the value of N in bits.
	:return: a tuple containing the values of p,q, and n respectively.
	"""

	p,q,N = calc_n(n_len)
	gcd=0
	while gcd != 1:
		p,q,N = calc_n(n_len)
		lambda_n=calc_lambda(p,q)
		gcd=gcd_fast(e,lambda_n)[0]
	return p,q,N


def make_fermat_key(bit_width: int) -> tuple:
	"""
	Makes a key that will allow it to be factored using fermat's factorization
	technique. Then it will return p,q,n,e, and d.

	:param bit_width: the size of the key in bits.
	:return: The values p,q,n,e, and d.
	"""

	from sympy import nextprime
	prime_length = bit_width // 2
	p=get_prime(prime_length)
	q_len=(prime_length//4)//2
	p_hex=hex(p).replace('L','')
	zero_pad='0' * (len(p_hex) - q_len)
	q=p_hex[0:q_len]+zero_pad
	q=int(q,16)
	q=nextprime(q)
	n=p*q
	e_len=(n&1) + 15
	lambda_n=calc_lambda(p,q)
	e=calc_e(e_len,lambda_n)
	d= calc_d(e, lambda_n)
	return p, q, n, e, d


def make_fermat(bit_width):
	"""
	Makes the fermat challenge. Just a wrapper around make_fermat_key right now.

	:param bit_width: The size of the key in bits.
	:return: p,q,n,e,d
	:rtype: tuple
	"""

	p,q,n,e,d = make_fermat_key(bit_width)
	return p,q,n,e,d


def make_pubkey(n: int, e: int) -> str:
	"""
	Makes a public key from the values of n and e.

	:param n: the modulus to utilize.
	:param e: the public key exponent.
	:return: A PEM encoded version of the public key.
	"""

	from Crypto.PublicKey import RSA
	key=RSA.construct((n,e))
	key_str=key.exportKey().decode('utf-8')
	return key_str


def make_privkey(n: int,e: int,d: int) -> str:
	"""
	Makes a private key encoded in PEM format
	from the public key components.

	:param n: The public key modulus.
	:param e: The public key exponent e.
	:param d: The private key exponent d.
	:return: A PEM encoded version of the private key.
	"""

	from Crypto.PublicKey import RSA
	key=RSA.construct((n,e,d))
	key_str=key.exportKey().decode('utf-8')
	return key_str
