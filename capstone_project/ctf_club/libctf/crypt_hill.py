from .crypt_math import *
"""
Crypto Lab Library - Hill Module
Macarthur Inbody <admin-contact@transcendental.us>
Licensed LGPLv3 or Later (2019 - 2020)
"""
def make_matricies(num_matricies):
	return list( list([[0,0],[0,0]]) for i in range(num_matricies))


def fill_matrix(input_matrix,items,items_len):

	for i in range(items_len):
		i_4=i*4
		input_matrix[i][0][0]=items[i_4]
		input_matrix[i][1][0]=items[i_4+1]
		input_matrix[i][0][1]=items[i_4+2]
		input_matrix[i][1][1]=items[i_4+3]

	return input_matrix



def matrix_to_list_string(input_str,input_str_len):
	out=list([0] * input_str_len*4)
	for i in range(input_str_len):
		i_4=i*4
		out[i_4]=chr(65+input_str[i][0][0])
		out[i_4+1]=chr(65+input_str[i][1][0])
		out[i_4+2]=chr(65+input_str[i][0][1])
		out[i_4+3]=chr(65+input_str[i][1][1])

	return ''.join(out)


def hill_decrypt(input_str,key):
	decryption_key= matrix_inv(key, 26)
	#Encryption and decryption are the same with just the key being different.
	return hill_encrypt(input_str,decryption_key)

def hill_encrypt(input_str,key):
	input_str_len=len(input_str)
	input_str_matrices=input_str_len//4
	numeric=make_numeric_list(input_str,input_str_len)
	ct=make_matricies(input_str_matrices)
	pt=make_matricies(input_str_matrices)
	pt=fill_matrix(pt,numeric,input_str_matrices)

	for i in range(input_str_matrices):
		ct[i]= matrix_mul(key, pt[i], 26)

	return matrix_to_list_string(ct,input_str_matrices)

def generate_random_key(modulus):
	gcd=0;a=0;b=0;c=0;d=0
	key=[[0,0],[0,0]]
	maximum = modulus -1
	while gcd != 1:
		a=randint(0,maximum)
		b=randint(0,maximum)
		c=randint(0,maximum)
		d=randint(0,maximum)
		key[0][0]=a
		key[0][1]=b
		key[1][0]=c
		key[1][1]=d
		dt=(a*d)-(b*c) % modulus
		#dt=det(key)%modulus
		gcd=gcd_fast(dt,modulus)[0]
   
	return [[a,b],[c,d]]

#input_str='ZAGXENGUFOHMGXENOAOWIRFCQNOYAFFPBDFCSXMU'
