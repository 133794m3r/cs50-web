from .libctf import *
from random import randint
import re

def make_index(objects):
	output = {}
	categories = []
	for challenge in objects:
		if output.get(challenge.category) is None:
			output[challenge.category] = [challenge]
			categories.append(challenge.category)
		else:
			output[challenge.category].append(challenge)

	return categories,output


def make_hill(plaintext,variety):

	#currently I just remove spaces to keep things simple.
	plaintext = plaintext.replace(' ','')
	key = generate_random_key(26)
	ct = hill_encrypt(plaintext,key)
	key = ','.join(key)
	flag = plaintext
	crib = plaintext[0:4]
	description = f"""<p>Given the following string of characters you have to decrypt them.<br /> {ct}.</p><br />"""
	if variety == 0:
		description+=f"""<p>From your "inside man", you were able to get the following string of numbers. What could they mean?</p><br /> {key}"""
	else:
		description+=f"""<p> From your assistant Watson you realize that the message starts with {crib}.</p>
"""
	return description,flag


def make_rsa(plaintext):
	pt_len = len(plaintext)
	M = int(radford_ascii_encode(plaintext,pt_len))
	prime_length = (pt_len * 15)+1
	p,q,N = calc_n(prime_length)
	l_n = calc_lamda(p,q)
	e = calc_e(10,l_n)
	C = rsa_encrypt(M,e,N)
	C = hex(C).replace('L','')
	e = hex(e).replace('L','')
	N = hex(N).replace('L','')
	description = f"""<p>You see a strange message popup on neppit as you're scrolling through your feed it looks interesting so you click on it. It leads to you to two files one a text file and the other an encrypted disk image....</p><br />
<p>
As you open up the file you see the message below come across your screen.
</p>
<br />
<p>
Recallling your prior training you know that e is the exponent, n is the modulus, and that C is the ciphertext. The message seems important, the only hint you're given is that the message is encoded with a naive form.
</p><br />
<pre>
e={e}
C={C}
n={N}
</pre>
"""

	flag = plaintext

	return description,flag


def make_hba(plaintext):
	m_len = len(plaintext)
	M = rsa_ascii_encode(plaintext,m_len)
	n_len =(m_len*9)+1
	e=3
	p,q,n1 = crt_e_maker(e,n_len)
	c1=rsa_encrypt(M,e,n1)

	p,q,n2 = crt_e_maker(e,n_len)
	c2=rsa_encrypt(M,e,n2)

	p,q,n3 = crt_e_maker(e,n_len)
	c3=rsa_encrypt(M,e,n3)
	c3 = hex(c3).replace('L','')
	c2 = hex(c2).replace('L','')
	c1 = hex(c1).replace('L','')
	n1 = hex(n1).replace('L','')
	n2 = hex(n2).replace('L','')
	n3 = hex(n3).replace('L','')
	description =f"""<p>You were enjoying your leftover Chinese food minding your own business watching reruns of Broadcast tv when your buddy sent you a message. He managed to intercept some secret communications. The messages were encrypted with RSA he's managed to get your the ciphertexts and also the public key components below.</p>
<p>He heard it's from the secretive group calling themselves "The Transcendentalists"</p>
<pre>
e:{e}
c1:{c1}
n1:{n1}
c2:{c2}
n2:{n2}
c3:{c3}
n3:{n3}
</pre>
<br />
<p>You need to provide the decrypted message not the numerical representation of the message. The message is encoded with the proper encoding.</p>
<br />
<p>Here's a free hint. Factoring n is not going to help you, Wolfram Alpha also cannot deal with numbers this large. So you need to try something else. This challenge uses the naive encoding instead of the normal encoding that this algorithm generally uses.</p>
	"""
	return description,plaintext


def make_common_mod(plaintext):
	m_len = len(plaintext)
	M = int(radford_ascii_encode(plaintext,m_len))
	n_len = (m_len*15)+1
	p,q,n = calc_n(n_len)
	l_n = calc_lamda(p,q)
	e1=calc_e(12,l_n)
	c1 = rsa_encrypt(M,e1,n)
	e2=calc_e(12,l_n)
	c2 = rsa_encrypt(M,e2,n)

	description =f"""<p>The Transcendentalists have given you another challenge. This time they want you to give them the secret phrase. Once again they say this is Elementary for you to solve.</p>
<br />
<br />
<p>They have given you this single hint:</p>
<p>"You cannot factor n as it's far too large to do that. Also, the message is not encoded via OS2IP"</p>
<br />
Challenge is below.
<br />
<pre>
You were given the following information.
e1={e1}
e2={e2}
c1={c1}
c2={c2}
n={n}


Also "The Elementalists" used naive ASCII encoding instead of the standard RSA encoding for the string.
</pre>
<p>
The flag is the original plaintext message.
</p>
"""
	return description,plaintext


def make_bsa(plaintext):
	m_len = len(plaintext)
	M=rsa_ascii_encode(plaintext,m_len)
	n_len=(m_len*9)+1
	p,q,n = calc_n(n_len)
	l_n = calc_lambda(p,q)
	e = calc_e(16,l_n)
	d = mod_inv(e,l_n)
	r = calc_r(n)
	M_fake = (M*pow(r,e)) % n
	S = pow(M_fake,d,n)
	S_fake = (S*mod_inv(r,n)) %n
	M_fake = hex(M_fake).replace('L','')
	S_fake = hex(S_fake).replace('L','')
	n = hex(n).replace('L','')
	description = f"""
<p>The Transcendentalists want you to forge a signature on the message "Use hashes to mitigate Blind Signing Attacks". They have thankfully let you send your message to their signing server to have it signed.</p>
<p>You and your friend already setup a blinded signature now it's up to you to get the signature on the original message.</p>
<p>You set your random integer r as {r}. The server sent you back the information attached.</p>
<br />
<p>They want you to give to them a signature on the original message encoded in hex. Just the hex digits without any extra information.</p>
<br />
<p>Here's the information you already had.</p>
<pre>
M={M}
N={n}
e={e}
r={r}
</pre>
<p>
You sent the server your blinded message M'.
</p>
<p>The server replied with the following message.</p>
==============================================================================================<br />
Your message M has been signed and the response S has been given along with your message.<br />
<pre>
M={M_fake}

S={S}
</pre>
=============================================================================================="""
	flag = S_fake

	return description,flag


def make_fermat(plaintext):
	m_len = len(plaintext)
	M = rsa_ascii_encode(plaintext,m_len)
	n_len = (m_len * 9) + 1
	p,q,n,e,d = make_fermat(n_len)
	C = rsa_encrypt(M,e,n)
	C = hex(C).replace('L','')
	e = hex(e).replace('L','')
	n = hex(n).replace('L','')
	description =f"""<p>our friend told you about a group called the Transcendentalists. They gave you a challenge to get into their group. They say the answer is simply "Elementary". They want you to decrypt the message they gave you. </p>
<p>When you see that the key is {n_len}bits in length they still tell you "It's Elementary my dear Watson." and refuse to say anything more.</p>

<pre>
C = {C}
e = {e}
n = {n}
</pre>
<br />
Free hint. This plaintext was encoded with OS2IP.
"""
	return description,plaintext


def make_affine(plaintext,variety):
	plaintext = plaintext.replace(' ','X').upper()
	plaintext = re.sub('[^A-Za-z]',plaintext)

	input_len = len(plaintext)
	if input_len == 0:
		plaintext="IXHATEXMONDAYS"
		input_len = len(plaintext)
	coprimes=[1,3,5,7,9,11,15,17,19,21,23,25]
	a = coprimes[randint(0,11)]
	b = randint(1,26)
	ct = affine_encrypt(plaintext,a,b)
	crib = plaintext[0:4]
	description = f"""<p>You happen upon a message scrawled on some old parchment.<br />The message is recreated below. It seems a man of culture has written it.</p>
	<pre>
{ct}
</pre>
	"""
	if variety == 0:
		description+=f"""You were able to find the 2 numbers scrawled on the back of the page. <pre>{a},{b}</pre>"""
	else:
		description+=f"""You can make out the first few letters of the original message and they read "{crib}"
"""

	return description,flag

def make_fizzbuzz(start,end):
	start = start or randint(1,3)
	max_num = end or randint(2500,3000)
	variety = randint(1,2)

	if variety == 1:
		num1 = randint(4,13)
		num2 = randint(num1+1,num1+5)
		num3 = num1*num2
		summed = 0
		for i in range(start,max_num):
			if not(i % num1):
				summed += i+3
			elif not(i%num2):
				summed += i - 2
			elif not(i%num3):
				summed += i * i
			else:
				summed += i

		flag = summed
		summed = 0
		for i in range(start,(num1*num2)+10):
			if not(i%num1):
				summed += i+3
			elif not(i%num2):
				summed += i-2
			elif not(i%num3):
				summed += i*i
			else:
				summed += i

		description = f"""<p>Write a program that adds all numbers together from {start} to {max_num-1}(inclusive). If the number is even divisible by {num1} then add 3 and that number to the total. If the number is evenly divisible by {num2} then add that number minus 2 to the running total. If the number is divisble by {num1} and {num2} then add that number squared. Otherwise simply add the number to the total. Your test case is given below.</p><br /><br /> <p>Running this algorithm on all numbers between {start} and {(num1*num2)+9} would result in the number {summed}. Verify that your program gets the same result before attempting to submit. You are free to use any language that you wish.</p>"""
	elif variety == 2:
		num1 = randint(4,13)
		num2=randint(num1+1,num1+5)
		num3 = num1*num2
		num1_counts = 0
		num2_counts = 0
		num3_counts = 0
		other_counts = 0

		for i in range(start,max_num):
			if not(i%num3):
				num3_counts += 1
				num1_counts +=1
				num2_counts +=1
			elif not(i % num1):
				num1_counts += 1
			elif not(i%num2):
				num2_counts += 1
			else:
				other_counts +=1

		flag = f"{num1_counts},{num2_counts},{num3_counts},{other_counts}"
		summed = 0
		num1_counts = 0;num2_counts=0;num3_counts=0;other_counts=0;
		for i in range(start,(num1*num2)+10):
			if not(i%num3):
				num3_counts += 1
				num1_counts += 1
				num2_counts += 1
			elif not(i%num1):
				num1_counts += 1
			elif not(i%num2):
				num2_counts += 1
			else:
				other_counts += 1

		description = f"""<p>Write a program that goes from {start} to {max_num - 1}(inclusvie). Get the number of times that a number is divisible by {num1},{num2},{num3}, and a count for the numbers no divisible by any of the previous 3. At the end arrange the counts like so(seperated by a comma. num1_count,num2_count,num3_count,other_count. The example case is given to you below.</p><br /> <p>If you run the same algoright on all numbers between {start} and {(num1*num2)+9}(inclusive). You'd get the following answer. {num1_counts},{num2_counts},{num3_counts},{other_counts}. So your flag would be the preceeding string. with the numbers seperated by a single "," and no other characters around them.</p>"""

	return description,flag


CHALLENGE_FUNCS = {
	"fizzbuzz":make_fizzbuzz,
	"hba":make_hba,
	"fermat":make_fermat,
	"hill":make_hill,
	"bsa":make_bsa,
	"rsa":make_rsa,
	"affine":make_affine,
	"common_mod":make_common_mod,
}

CATEGORIES = ["Classical Crypto","Modern Crypto","Programming"]

CHALLENGES_TEMPLATES = [
	{"name":"Cola and the Bee", "sn":"fizzbuzz", "category":"Programming", "description":"This is a basic fizzbuzz challgen where you have to  provide a min an maximum number."},
	{"name":"Really Simple Algorithm - Frenchman's Revenge", "sn":"fermat", "category":"Modern Crypto", "description":"This is an attack on RSA. This challenge is also known as 'Fermat's Near prime' attack. Provide the plain-text and the app will do the rest."},
	{"name":"Master of Hill Climbing", "sn":"hill", "category":"Classical Crypto", "description":"This challenge is all about the hill cipher. Select the easy version for one where the user is given the key. The hard mode for when they shouldn't be given the key at the start."},
	{"name":"Really Simple Algorithm - Intro", "sn":"rsa", "category":"Classical Crypto", "description":"This challenge is just a simple RSA based challenge that requires the user to decrypt some message."},
	{"name":"Really Simple Algorithm - Fake it till you make it", "sn":"bsa", "category":"Modern Crypto", "description":"This is an attack on RSA called the 'Blind Signature Attack'. To keep it simple we're going to have them work with a message that's already been signed."},
	{"name":"A-fine Cipher", "sn":"affine", "category":"Classical Crypto", "description":"This challenge is all about the affine cipher which is basically just a 2-step Ceaser Cipher."},
	{"name":"Really Simple Algorithm - It's all the Same","sn":"common_mod","category":"Modern Crypto","description":"This challenge requires someone to carry out a common modulus attack against RSA."},
	{"name":"Really Simple Algorithm - Leftover Chinese Food","sn":"hba","category":"Modern Crypto","description":"This challenge requires the solver to utilize the Hastaad Broadcast Attack against RSA."}
]
CHALLENGES_TEMPLATES_NAMES = {}

for i,chal in enumerate(CHALLENGES_TEMPLATES):
	CHALLENGES_TEMPLATES_NAMES[chal['name']] = [chal['sn'],i]