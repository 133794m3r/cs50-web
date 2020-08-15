import re
from random import randint

from ctf_club.libctf import generate_random_key, hill_encrypt, affine_encrypt


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
