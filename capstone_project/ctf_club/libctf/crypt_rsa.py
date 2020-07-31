#!/bin/python
# Crypto Lab Library - RSA Library
# This contains all of the functions to deal with the most common RSA attacks
# and also the utilities required to do that.
# Macarthur Inbody 2019 - 2020
# All Rights Reserved


#This does the hard work of actually getting you the plaintext back via the
# common modulus attack. All you need to supply is both exponents, both cipher-
# texts. Then the common Modulus.
import secrets
from .crypt_math import *

def common_modulus_attack(c1,c2,e1,e2,N):
	a=0;
	b=0;
	mx=0;
	my=0;
	i=0;

	if gcd_fast(e1,e2)[0] != 1:
		raise ValueError('e1 and e2 are invalid.')
	a=mod_inv(e1,e2)
	b=(gcd_fast(e1,e2)[0] - e1 * a ) // e2
	i=mod_inv(c2,N)
	mx=pow(c1,a, N)
	my=pow(i,-b, N)

	return (mx*my) % N

# Radford ASCII Decoder
# This function decodes a number into a 7bit ASCII string and returns said string.
def radford_ascii_decode(encoded_number,length):
	i=0;
	j=0;
	val=0;
	tmp='';
	output_str='';
	length=length-1;
	num_len=len(encoded_number)
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
def radford_ascii_encode(string_to_encode,string_length):
	tmp_str='';
	output_str='';

	tmp=0;
	i=0;

	for i in range(0,string_length):
		tmp=ord(string_to_encode[i:i+1])
		tmp_str=str(tmp)
		output_str=output_str+tmp_str

	encoded_number=output_str

	return encoded_number


# this decodes a string of bytes(ASCII text only really otherwise you need to convert it
# to a byte stream.
def rsa_ascii_encode(string_to_encode,string_length):
	tmp_str='';
	output_str='';
	x=0;
	string_to_encode=string_to_encode[::-1]
	tmp=0;
	os=[]
	i=0
	while i<string_length:
		tmp=ord(string_to_encode[i:i+1])
		x+=(tmp*pow(256,i))
		i+=1

	return x


#This converts the number to a string out of it.
def rsa_ascii_decode(x,x_len):
	X = []
	i=0;
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
def get_prime(prime_length):
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

def calc_n(prime_length):
	prime_length = prime_length // 2
	p=get_prime(prime_length)
	q=get_prime(prime_length)
	while p == q:
		q=get_prime(prime_length)

	N=p*q

	return p, q, N

# Creates the value e such that 0 < e < lamda_n
# We only chose prime numbers so that we can simply check if there
# are any common divisors between e and lamda_n and if there are not
# they are coprime and share no divsors and the value works.
def calc_e(prime_length,lamda_n):
	coprime=0
	e=0
	while coprime!=1:
		e=get_prime(prime_length)
		coprime=gcd_fast(e,lamda_n)[0]

	return e

'''
This function implements carmicheal's totient to get the value utilized for generating
the multiplicative inverse of the values later one. Carmicheal's is a lot faster than
the default method represented in the original paper of PHI(p-1*q-1) which requires
a crapton of cputime to count all of the primes in the set. This is much faster.

'''
def calc_lamda(p,q):
	lamda_n=0;
	lamda_n=fast_lcm(p-1,q-1)
	return lamda_n

# Calculates the private key d wherein the following conditions are met.
# d=(e**-1) mod lamda_n. Thus d*e = 1 % lamda_n
# It utilizes previously defined functions for the calculation and works with
# the test vectors.

def calc_d(e,lamda_n):
	d=0
	d=mod_inv(e,lamda_n)

	return d

'''
Calculates the ciphertext using the pure math model for RSA Encryption.
Via the following formula. c=(m**e) % N
Returns the cipher number c.
'''
def rsa_encrypt(m,e,N):
	c=0
#	c=(pow(m,e,N) % N)
	c=pow(m,e,N)

	return c

'''
Implements RSA Decryption via the mathematical formula.
The formula is m=(c**d) % N
Returns the plain "text" really integer representation of the value.
'''
def rsa_decrypt(c,d,N):
	m=0
#	m=(pow(c,d) % N)
	m=pow(c,d,N)

	return m
def crt_e_maker(e,n_len=256):
	p,q,N = calc_n(n_len)
	lamda_n=calc_lamda(p,q)
	gcd=0;
	while gcd != 1:
		p,q,N = calc_n(n_len)
		lamda_n=calc_lamda(p,q)
		gcd=gcd_fast(e,lamda_n)[0]
	return p,q,N

def make_fermat_key(bit_width):
	from sympy import nextprime
	prime_length = bit_width // 2
	p=get_prime(prime_length)
	q_len=(prime_length//4)//2
	p_hex=hex(p).replace('L','');
	zero_pad='0' * (len(p_hex) - q_len)
	q=p_hex[0:q_len]+zero_pad
	q=int(q,16)
	q=nextprime(q)
	n=p*q
	e_len=(n&1) + 15;
	lamda_n=calc_lamda(p,q);
	e=calc_e(e_len,lamda_n);
	d=calc_d(e,lamda_n);
	return p, q, n, e, d

def make_fermat(bit_width):
	p,q,n,e,d = make_fermat_key(bit_width);
	print('n={}'.format(n))
	print('e={}'.format(e))
	print('d={}'.format(d))
	print('Public Key\n{}'.format(make_pubkey(n,e)))
	print('Private Key\n{}'.format(make_privkey(n,e,d)))
	return p,q,n,e,d

def make_pubkey(n,e):
	from Crypto.PublicKey import RSA
	key=RSA.construct((n,e))
	key_str=key.exportKey('PEM').decode('utf-8')
	return key_str

def make_privkey(n,e,d):
	from Crypto.PublicKey import RSA
	key=RSA.construct((n,e,d))
	key_str=key.exportKey('PEM').decode('utf-8')
	return key_str
