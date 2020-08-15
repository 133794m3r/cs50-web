"""
Crypto Lab Library - Hill Module
Macarthur Inbody <admin-contact@transcendental.us>
Licensed LGPLv3 or Later (2019 - 2020)
"""

from random import randint

def gcd_fast(a: int, b: int) -> tuple:
	"""
	GCD using Euler's Extended Algorithm generalized for all integers of the
	set Z. Including negative values.

	:param a: The first number.
	:param b: The second number.
	:return: gcd,x,y. Where x and y are bezout's coeffecients.
	"""

	gcd=0
	x=0
	y=0
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


def mod_inv(a:int,mod:int) -> int:
	"""
	Calculates the moduler multiplicative inverse of a and the modulus value
	 such that a * x = 1 % mod
	This version is a generalization and improvement upon the standard extended
	 euclidean algorithm It is improved and works for all values a,m set Z.

	:param a: The integer a.
	:param mod: The modulus..
	:return: Int the modular mutiplicative inverse of a and m.
	"""

	gcd=0
	x=0
	y=0
	x=0

	#use the extended euclidean algorithm to calculate the gcd and also bezout's coeffecients x and y.
	gcd, x, y = gcd_fast(a,mod)


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


def fast_lcm(a: int, b: int) -> object:
	"""
	a fast lcm calculator utilizing the extended euler algorithm.

	:param a:
	:param b:
	:return:
	"""

	lcm=0
	gcd=0

	if a==0 or b==0:
		return 0
	elif a==1:
		return b
	elif b==1:
		return a

	gcd=gcd_fast(a,b)[0]
	lcm=(a//gcd)*b

	return lcm



def det(a: list) -> int:
	"""
	Calculates the determinant of a 2x2 Matrix, via the shortcut
	(a*d) - (b*c)

	:param a: The matrix A.
	:return: The determinant.
	"""

	d= (a[0][0] * a[1][1]) - (a[0][1] * a[1][0])
	return d


def inv_det(a:list,m:int) -> int:
	"""
	Calculates the inverse determinant some value.

	:param a: The matrix A(2x2)
	:param m: The value m.
	:return: The inverse of the determinant modulus the value m.
	"""

	return mod_inv(det(a), m)


def adj(a):
	"""
	Calculates the adjugate of A via just swapping the values.
	The formula is [[a,b],[c,d]] => [[d,-b],[-c,a]]
	:param a: the matrix A(2x2)
	:return:
	"""

	B=[[0,0],[0,0]]
	B[0][0]=a[1][1]
	B[0][1]=-a[0][1]
	B[1][0]=-a[1][0]
	B[1][1]=a[0][0]
	return B


def matrix_inv(a: list, m: int) -> list:
	"""
	Calculates the matrix inverse with modulus.

	:param a: Input Matrix
	:param m: Modulus
	:return: The inverse of the matrix A and the modulus m.
	"""

	A_inv=[[0,0],[0,0]]
	d= inv_det(a, m)
	a= adj(a)
	A_inv[0][0]=d*a[0][0] % m
	A_inv[0][1]=d*a[0][1] % m
	A_inv[1][0]=d*a[1][0] % m
	A_inv[1][1]=d*a[1][1] % m

	return A_inv


def matrix_mul(a: list, b: list, m: int = 0) -> list:
	"""
	This function will naively multiply Matrix A and B(both must be 2x2),
	modulus some value m.

	:param a: The first Matrix.
	:param b: The second Matrix.
	:param m: The modulus.
	:return:
	"""

	C=[[0,0],[0,0]]
	if len(a) != 2 and len(a[0]) != 2:
		raise ValueError('Your matrix must be a 2x2')
	if type(b) == list:
		#>>> 'foo' if (a and b ) != 2 else 'bar'
		if len(b) !=2 and len(b[0]) !=2 :
			raise ValueError('Both matricies must be 2x2')
		C[0][0] = (a[0][0] * b[0][0]) + (a[0][1] * b[1][0])
		C[0][1] = (a[0][0] * b[0][1]) + (a[0][1] * b[1][1])
		C[1][0] = (a[1][0] * b[0][0]) + (a[1][1] * b[1][0])
		C[1][1] = (a[1][0] * b[0][1]) + (a[1][1] * b[1][1])
	else:
		C[0][0] = a[0][0] * b
		C[0][1] = a[0][1] * b
		C[1][0] = a[1][0] * b
		C[1][1] = a[1][1] * b

	if m != 0:
		C[0][0] = C[0][0] % m
		C[0][1] = C[0][1] % m
		C[1][0] = C[1][0] % m
		C[1][1] = C[1][1] % m

	return C

def make_numeric_list(input_str: str, input_str_len: int) -> list:
	"""
	This converts an uppercase string of letters into a list of it's numeric
	values for use in the Hill cipher. All values are converted into their
	index of the standard english alphabet.

	:param input_str: The string to be listified.
	:param input_str_len: The length of that string.
	:return: a list of integers.
	"""

	numeric=list( ord(input_str[i]) - 65 for i in range(input_str_len))

	return numeric


def make_list_string(input_list: list, input_list_len: int) -> str:
	"""
	This function will take the numeric list, and map vall values back
	into ASCII uppercase text.

	:param input_list: The input list.
	:param input_list_len:  How long it is.
	:return: An uppercase string.
	"""

	out=list([0] * input_list_len)
	for i in range(input_list_len):
		out[i]=chr(65 + input_list[i])

	return ''.join(out)


def affine_setup(string:str) -> tuple:
	"""
	Affine setup function.

	:param string: Input string.
	:return: length of the string, and the numeric list.
	"""
	str_len=len(string)
	numeric_str=make_numeric_list(string, str_len)

	return str_len, numeric_str


def affine_encrypt(input_str:str, a:int=None, b:int=None) -> str:
	"""
	This function will encrypt a string of text with an optionally provided
	key or generate one itself.

	:param input_str: The plaintext.
	:param a: The integer a.
	:param b: The integer b.
	:return: The ciphertext.
	"""

	tmp=0
	str_len,numeric_str = affine_setup(input_str)
	coprimes=[1,3,5,7,9,11,15,17,19,21,23,25]
	if a is None:
		tmp=randint(0,11)
		a=coprimes[tmp]
	if b is None:
		b=randint(1,26)
	for i in range(str_len):
		numeric_str[i]=((numeric_str[i]*a)+b) % 26

	crypt_str= make_list_string(numeric_str, str_len)
	return crypt_str


def affine_decrypt(input_str:str, a:int, b:int) -> str:
	"""
	This function will decrypt an affine encrypted string with the key a and b.

	:param input_str: The ciphertext.
	:param a: The intger a part of the key.
	:param b: The integer b part of the key.
	:return: The plaintext.
	"""

	a=mod_inv(a,26)
	str_len, numeric_str = affine_setup(input_str)
	for i in range(str_len):
		numeric_str[i]=( a * (numeric_str[i] - b)) % 26
	pt= make_list_string(numeric_str, str_len)

	return pt
