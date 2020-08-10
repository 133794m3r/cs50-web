from .libctf import *
from random import randint
import re
"""
CTFClub Project
By Macarthur Inbody <admin-contact@transcendental.us>
Licensed AGPLv3 Or later (2020)
"""
def make_index(objects):
	output = {}
	maximum = 0
	for challenge in objects:
		if challenge.category.name not in output:
			output[challenge.category.name] = [challenge]
			maximum +=1
		else:
			#i = categories.index(challenge.category.name)
			output[challenge.category.name].append(challenge)

	return output


def make_hill(plaintext: str, variety: int) -> tuple:
	"""
	make_hill

	The function creates a flag based upon the hill cipher.

	:param plaintext: The plaintext string we're going to encrypt.
	:param variety: 0 or 1. Where 0 means to give them the encryption key, and
	1 is to give them a crib.
	:return: A tuple containing the description for the flag, and the flag itself.
	"""

	#currently I just remove spaces to keep things simple.
	plaintext = plaintext.replace(' ','')
	#to make sure that it's only containing the letters of the alphabet.
	plaintext = re.sub('[^A-Za-z]','',plaintext).upper()
	#to make sure that it's not always an X that's padded at the end.
	padding_char = chr(randint(80,90))
	flag = plaintext
	if len(plaintext) % 4 != 0:
		plaintext += padding_char*(len(plaintext) % 4)
	key = generate_random_key(26)
	ct = hill_encrypt(plaintext,key)

	#doing it raw here b/c it works.
	#eventually I'll make the key be a 1d list.
	key = f'{key[0][0]},{key[0][1]},{key[1][0]},{key[1][1]}'

	crib = plaintext[0:4]
	description = f"""<p>Given the following string of characters you have to decrypt them.<br /> "{ct}".</p><br /> Note that any repeated characters at the end should be discarded. The message will always be made up of real words also. So if a letter seems to not belong(that's at the end) remove it."""

	if variety == 0:
		description+=f"""<p>From your "inside man", you were able to get the following string of numbers. What could they mean?</p><br /> {key}"""
	else:
		description+=f"""<p> From your assistant Watson you realize that the message starts with {crib}.</p>
"""
	return description,flag


def make_rsa(plaintext: str) -> tuple:
	"""
	make_rsa

	The function creates a basic RSA challenge where someone has to decrypt a
	message encrypted with RSA.

	:param plaintext: The plaintext to encrypt.
	:return: The tuple containing the description,flag. Where flag is the answer.
	:rtype: tuple
	"""

	pt_len = len(plaintext)
	M = int(naive_ascii_encode(plaintext, pt_len))
	prime_length = (pt_len * 15)+1
	p,q,N = calc_n(prime_length)
	l_n = calc_lambda(p,q)
	e = calc_e(10,l_n)
	C = rsa_encrypt(M,e,N)
	C = hex(C).replace('L','')
	e = hex(e).replace('L','')
	N = hex(N).replace('L','')
	description = f"""<p>You see a strange message popup on neppit as you're scrolling through your feed it looks interesting
so you click on it. It leads to you to two files one a text file and the other an encrypted disk image....</p>
<p>
As you open up the file you see the message below come across your screen.
</p>
<p>
Recalling your prior training you know that e is the exponent, n is the modulus, and that C is the ciphertext. 
The message seems important, the only hint you're given is that the message is encoded with a naive form.
</p>
<p class="text-monospace">
e={e}<br />
C={C}<br />
n={N}<br />
</p>
"""

	flag = plaintext

	return description,flag


def make_hba(plaintext:str) -> tuple:
	"""
	make_hba

	Makes a Hastad Broadcast Attack flag. The value of e is 3 and the encoding
	is the standard OS2IP to keep it simple for users. That want to attempt to
	complete the challenge.

	:param plaintext: The flag the users are going to be trying to get.
	:return: the description and the flag.
	:rtype: tuple
	"""

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

	#The code below makes sure that python doesn't append an "L" to the end of the hex encoded number.
	c3 = hex(c3).replace('L','')
	c2 = hex(c2).replace('L','')
	c1 = hex(c1).replace('L','')
	n1 = hex(n1).replace('L','')
	n2 = hex(n2).replace('L','')
	n3 = hex(n3).replace('L','')

	description =f"""<p>You were enjoying your leftover Chinese food minding your own business watching reruns of Broadcast tv when your buddy sent you a message. He managed to intercept some secret communications. The messages were encrypted with RSA he's managed to get your the ciphertexts and also the public key components below.</p>
<p>He heard it's from the secretive group calling themselves "The Transcendentalists"</p>
<p class="text-monospace">
e:{e}<br />
c1:{c1}<br />
n1:{n1}<br />
c2:{c2}<br />
n2:{n2}<br />
c3:{c3}<br />
n3:{n3}<br />
</p>
<br />
<p>You need to provide the decrypted message not the numerical representation of the message. The message is encoded with the proper encoding.</p>
<br />
<p>Here's a free hint. Factoring n is not going to help you, Wolfram Alpha also cannot deal with numbers this large. So you need to try something else. This challenge uses the naive encoding instead of the normal encoding that this algorithm generally uses.</p>
	"""
	return description,plaintext


def make_common_mod(plaintext: str) -> tuple:
	"""
	make_common_mod
	
	Creates a challenge based upon the RSA Common Modulus Attack. The message is
	encoded with naive ascii encoding. The flag and answer are both included.
	
	:param plaintext: The string that we're going to use for the flag.
	:return: A tuple containing the descriptiona nd the flag.
	:rtype: tuple
	"""

	m_len = len(plaintext)
	M = int(naive_ascii_encode(plaintext, m_len))
	n_len = (m_len*15)+1
	p,q,n = calc_n(n_len)
	l_n = calc_lambda(p,q)
	e1=calc_e(12,l_n)
	c1 = rsa_encrypt(M,e1,n)
	c1 = hex(c1).replace('L','')
	e2=calc_e(12,l_n)
	c2 = rsa_encrypt(M,e2,n)
	c2 = hex(c2).replace('L','');
	n = hex(n).replace('L','')
	description =f"""<p>The Transcendentalists have given you another challenge. This time they want you to give them the secret phrase. Once again they say this is Elementary for you to solve.</p>
<br />
<br />
<p>They have given you this single hint:</p>
<p>"You cannot factor n as it's far too large to do that. Also, the message is not encoded via OS2IP"</p>
<br />
Challenge is below.
<br />
<p class="text-monospace">
You were given the following information.<br />
e1={e1}<br />
e2={e2}<br />
c1={c1}<br />
c2={c2}<br />
n={n}<br />
</p>

Also "The Elementalists" used naive ASCII encoding instead of the standard RSA encoding for the string.
<p>
The flag is the original plaintext message.
</p>
"""
	return description,plaintext


def make_bsa(plaintext: str) -> tuple:
	"""
	Creates a blind signature attack with the value of r already chosen for them.
	This is due to simplicity's reasons. So that the person solving doesn't have
	to actually caluclate the value of r themselves.

	:param plaintext: The plaintext message we're going to be forging a signature on.
	:return: description,flag Where description is the description of the program and
	the flag is the fake signature we're asking them to provide to us.
	"""
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
	M = hex(M).replace('L','')
	e = hex(e).replace('L','')
	S = hex(S).replace('L','')
	description = f"""
<p>The Transcendentalists want you to forge a signature on the message "Use hashes to mitigate Blind Signing Attacks". They have thankfully let you send your message to their signing server to have it signed.</p>
<p>You and your friend already setup a blinded signature now it's up to you to get the signature on the original message.</p>
<p>You set your random integer r as {r}. The server sent you back the information attached.</p>
<p>They want you to give to them a signature on the original message encoded in hex. Just the hex digits without any extra information.</p>
<p>Here's the information you already had.</p>
<p class="text-monospace">
M={M}<br />
N={n}<br />
e={e}<br />
r={r}
</p>
<p>
You sent the server your blinded message M'.
</p>
<p>The server replied with the following message.</p>
===============<br />
Your message M has been signed and the response S has been given along with your message.<br />
<p class="text-monospace">
M={M_fake}
<br /><br />
S={S}
</p>
==============="""
	flag = S_fake
	return description,flag


def make_fermat_chal(plaintext: str) -> tuple:
	"""
	Makes a challenge that requires the person to factor the public key via
	Fermat's Near Prime Factorization method.

	:param plaintext: The plaintext message they have to provide as the flag.
	:return: description,plaintext The description of the flag and the plaintext itself.
	"""

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

<p class="text-monospace">
C = {C}<br />
e = {e}<br />
n = {n}<br />
</p>
<br />
Free hint. This plaintext was encoded with OS2IP.
"""
	return description,plaintext


def make_affine(plaintext: str, variety: int) -> tuple:
	"""
	Makes a flag with the affine crypto system. Either one where they're given
	the key or just a crib to utilize.
	:param plaintext: The plaintext message aka the flag.
	:param variety: Whether they're given the flag or key 0 = key, 1=crib.
	:return: description,plaintext the flag's description and teh plaintext aka the flag.
	"""

	plaintext = plaintext.replace(' ','').upper()
	plaintext = re.sub('[^A-Za-z]','',plaintext)
	input_len = len(plaintext)
	if input_len == 0:
		plaintext="IXHATEXMONDAYS"
	coprimes=[1,3,5,7,9,11,15,17,19,21,23,25]
	a = coprimes[randint(0,11)]
	b = randint(1,26)
	ct = affine_encrypt(plaintext,a,b)
	crib = plaintext[0:4]
	description = f"""<p>You happen upon a message scrawled on some old parchment.<br />The message is recreated below. It seems a man of culture has written it.</p>
	<p class="text-monospace">
{ct}
</p>
	"""
	if variety == 0:
		description+=f"""You were able to find the 2 numbers scrawled on the back of the page. <pre>{a},{b}</pre>"""
	else:
		description+=f"""You can make out the first few letters of the original message and they read "{crib}"
"""

	return description,plaintext


def make_fizzbuzz(start: int, end: int) -> tuple:
	"""
	make_fizzbuzz
	
	Makes a challenge based upon a basic fizzbuzz challenge for the users to try to solve.
	
	:param start: The starting value we're going to count from.
	:param end: The end number they're going to be counting to.
	:return: A tuple containing the description and the flag.
	"""

	flag = ''
	description = ''
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
		num1_counts = 0;num2_counts=0;num3_counts=0;other_counts=0
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
	"fermat":make_fermat_chal,
	"hill":make_hill,
	"bsa":make_bsa,
	"rsa":make_rsa,
	"affine":make_affine,
	"common_mod":make_common_mod,
}

CATEGORIES = ["Classical Crypto","Modern Crypto","Programming"]

#TODO: Move all of this into an SQL table that'll actually hold this meta-data for me.

CHALLENGES_TEMPLATES = [
	{"name":"Cola and the Bee", "sn":"fizzbuzz", "category":"Programming", "description":
		"""This is a basic fizzbuzz challenge where you have to  provide a min an maximum number. 
		The maximum minus 1 is the number that is counted to.""",
	 "points":75, "variety":False},
	{"name":"Really Simple Algorithm - Frenchman's Revenge", "sn":"fermat", "category":"Modern Crypto", "description":
		"This is an attack on RSA. This challenge is also known as 'Fermat's Near prime' attack."
		" Provide the plain-text and the app will do the rest.",
	 "points":240,"variety":False},
	{"name":"Master of Hill Climbing", "sn":"hill", "category":"Classical Crypto", "description":
		"This challenge is all about the hill cipher. Select the easy version for one where the user is given the key. "
		"The medium mode for when they shouldn't be given the key at the start.",
	 "points":70, "variety":True},
	{"name":"Really Simple Algorithm - Intro", "sn":"rsa", "category":"Modern Crypto",
	 "description":"This challenge is just a simple RSA based challenge that requires the user to decrypt some message.",
	 "points":150, "variety":False},
	{"name":"Really Simple Algorithm - Fake it till you make it", "sn":"bsa", "category":"Modern Crypto",
	 "description":
		 "This is an attack on RSA called the 'Blind Signature Attack'. To keep it simple we're going to have them work "
		 "with a message that's already been signed.", "points":225, "variety":False},
	{"name":"A-fine Cipher", "sn":"affine", "category":"Classical Crypto", "description":
		"This challenge is all about the affine cipher which is basically just a 2-step Ceaser Cipher."
		" Easy mode gives them the key. Medium mode doesn't give them a key but does give them a crib.", "points":100, "variety":True},
	{"name":"Really Simple Algorithm - It's all the Same", "sn":"common_mod", "category":"Modern Crypto",
	 "description":"This challenge requires someone to carry out a common modulus attack against RSA.",
	 "points":45, "variety":False},
	{"name":"Really Simple Algorithm - Leftover Chinese Food", "sn":"hba", "category":"Modern Crypto",
	 "description":"This challenge requires the solver to utilize the Hastaad Broadcast Attack against RSA.",
	 "points":300, "variety":False}
]


def __func():
	CHALLENGES_TEMPLATES_NAMES = {}
	for i,chal in enumerate(CHALLENGES_TEMPLATES):
		CHALLENGES_TEMPLATES_NAMES[chal['name']] = [chal['sn'],i]
	return CHALLENGES_TEMPLATES_NAMES


CHALLENGES_TEMPLATES_NAMES = __func()

def jsonify_queryset(queryset: object) -> dict:
	"""
	jsonify_queryset will take a queryset object from the Django.models result
	and return a list of dicts that are ready to be serialized into JSON for
	the use by the API and consumed by the client.


	:param queryset: The object we're working with. May already be a dict.o
	:return: {dict} A dict that's ready to be serialized as JSON.
	"""

	out = []
	if type(queryset) is dict:
		return queryset
	elif len(queryset) > 1:
		for result in queryset:
			print(result)
			if type(result) is dict:
				out.append(result)
			else:
				out.append(result.to_dict())
	else:
		try:
			if queryset.count() == 1:
				tmp = queryset.first()
				if type(tmp) is dict:
					return tmp
				else:
					return tmp.to_dict()
		except AttributeError:
			return queryset.to_dict()

	return out
