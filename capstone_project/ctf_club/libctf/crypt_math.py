#!/bin/python
# Crypto Lab Library - Math Module
# Macarthur Inbody 2019 - 2020
# All Rights Reserved

"""
gcd calculator using the Generalized Extended Euclidean Algorithm.

Python implementation of the extended euclidean algorithm for calculating the gcd.
This code is the recursive variant as it is simpler.

"""
def gcd_fast(a,b):
	gcd=0;
	x=0;
	y=0;
	x=0
	"""
	if a < 0:
		sign_x=-1
	else:
		sign_x=1
	if b < 0:
		sign_y=-1
	else:
		sign_y=1
	"""
	#if a or b is zero return the other value and the coeffecient's accordingly.
	if a==0:
		return b, 0, 1
	elif b==0:
		return a, 0, 1
	#otherwise actually perform the calculation.
	else:
		#set the gcd x and y according to the outputs of the function.
		# a is b (mod) a. b is just a.
		gcd, x, y = gcd_fast(b % a, a)
		#we're returning the gcd, x equals y - floor(b/a) * x
		# y is thus x.
		return gcd, y - (b // a) * x, x

# Calculates the moduler multiplicative inverse of a and the modulus value
# such that a * x = 1 % mod
# Also mod is the modulus.
# % is the modulus operator in python.
# This version is a generalization and improvement upon the standard extended euclidean algorithm
# It is improved and works for all values a,m set Z.
# That means for all values of a and m that are real integers.
def mod_inv(a,mod):
	gcd=0;
	x=0;
	y=0;
	x=0;
	# if a is less than 0 do this.
#	if a < 0:
		# while a is less than zero keep adding the abs value of the modulus to it.
		#while a < 0:
			#a+=x
#		a %= mod
	#use the extended euclidean algorithm to calculate the gcd and also bezout's coeffecients x and y.
	gcd, x, y = gcd_fast(a,mod)
	"""
	if a < 0:
		x*=-1
	else:
		x=1
	"""
#	print("gcd:{} x:{} y:{}",gcd,x,y);
	#if the gcd is not 1 or -1 tell them that it's impossible to invert.
	if gcd not in (-1,1):
		raise ValueError('Inputs are invalid. No modular multiplicative inverse exists between {} and {} gcd:{}.\n'.format(a,mod,gcd))
	#otherwise do the inversion.
	else:

		"""if(sign_a != 1) and (sign_mod !=1):
			return -1*((x+mod)%mod);
		else:
			return x%mod;
			"""
		#if m is negative do the following.
		return x % mod


# A fast LCM calculator utilizing the extended euler algorithm.

def fast_lcm(a,b):
	lcm=0;
	gcd=0;

	if a==0 or b==0:
		return 0
	elif a==1:
		return b
	elif b==1:
		return a

	gcd=gcd_fast(a,b)[0]
	lcm=(a//gcd)*b

	return lcm


# This function calculates the determinate of A
# via the following formula.
# (a*d) - (b*c)
def det(A):
	d=(A[0][0]*A[1][1])-(A[0][1]*A[1][0])
	return d

# This calculates the inverse of the determinant of A and m.
def inv_det(A,m):
	return mod_inv(det(A),m)

# This function calculates the adjugate of A
# The formula is [[a,b],[c,d]] => [[d,-b],[-c,a]]
def adj(A):
	B=[[0,0],[0,0]]
	B[0][0]=A[1][1]
	B[0][1]=-A[0][1]
	B[1][0]=-A[1][0]
	B[1][1]=A[0][0]
	return B

# This function calculates the inverse of the matrix mod 26.
def matrix_inv(A: list, m: int) -> list:
	"""

	:param A: Input Matrix
	:param m: Modulus
	:return: The inverse 
	"""
	A_inv=[[0,0],[0,0]]
	d=inv_det(A,m)
	a=adj(A)
	A_inv[0][0]=d*a[0][0] % m
	A_inv[0][1]=d*a[0][1] % m
	A_inv[1][0]=d*a[1][0] % m
	A_inv[1][1]=d*a[1][1] % m

	return A_inv

# This function multiplies two matricies A and B and it takes an optional third argument
# m which will take the results and apply a modulus on their matricies. If it is not set
# it will return the normal multiplication.
# ex. matrix_multiply(A,B,m) will return the results of [A]*[B] % m
# If the second variable B is not a matrix then it multiplies A by that value.
# This is not the normal method but it keeps it simplified.
def matrix_mul(A: list, B: list, m: int = 0) -> list:
	C=[[0,0],[0,0]]
	if len(A) != 2 and len(A[0]) != 2:
		raise ValueError('Your matrix must be a 2x2');
	if type(B) == list:
		#>>> 'foo' if (a and b ) != 2 else 'bar'
		if len(B) !=2 and len(B[0]) !=2 :
			raise ValueError('Both matricies must be 2x2');
		C[0][0] = (A[0][0]*B[0][0])+(A[0][1]*B[1][0])
		C[0][1] = (A[0][0]*B[0][1])+(A[0][1]*B[1][1])
		C[1][0] = (A[1][0]*B[0][0])+(A[1][1]*B[1][0])
		C[1][1] = (A[1][0]*B[0][1])+(A[1][1]*B[1][1])
	else:
		C[0][0] = A[0][0]*B
		C[0][1] = A[0][1]*B
		C[1][0] = A[1][0]*B
		C[1][1] = A[1][1]*B

	if m != 0:
		C[0][0] = C[0][0] % m
		C[0][1] = C[0][1] % m
		C[1][0] = C[1][0] % m
		C[1][1] = C[1][1] % m

	return C

def make_numeric_list(input_str: str, input_str_len: int) -> list:
	i=0;
	numeric=list( ord(input_str[i]) - 65 for i in range(input_str_len));

	return numeric;

def make_list_string(input_str,input_str_len):
	i=0;
	out=list([0] * input_str_len)
	for i in range(input_str_len):
		out[i]=chr(65+input_str[i]);

	return ''.join(out);

def affine_encrypt(input_str, a=None, b=None):
	tmp=0
	str_len,numeric_str = affine_setup(input_str)
	coprimes=[1,3,5,7,9,11,15,17,19,21,23,25]
	if a is None:
		tmp=random.randint(0,11)
		a=coprimes[tmp]
	if b is None:
		b=random.randint(1,26)
	for i in range(str_len):
		numeric_str[i]=((numeric_str[i]*a)+b) % 26

	crypt_str=make_list_string(numeric_str,str_len)
	return crypt_str;

def affine_decrypt(input_str, a, b):
	a=mod_inv(a,26);
	str_len, numeric_str = affine_setup(input_str)
	for i in range(str_len):
		numeric_str[i]=( a * (numeric_str[i] - b)) % 26
	pt=make_list_string(numeric_str,str_len)

	return pt