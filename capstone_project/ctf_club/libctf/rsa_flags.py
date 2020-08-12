#  Macarthur Inbody <admin-contact@transcendental.us>
#  Licensed under LGPLv3 Or Later (2020)

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
	prime_length = (pt_len * 15) + 1
	p, q, N = calc_n(prime_length)
	l_n = calc_lambda(p, q)
	e = calc_e(10, l_n)
	C = rsa_encrypt(M, e, N)
	C = hex(C).replace('L', '')
	e = hex(e).replace('L', '')
	N = hex(N).replace('L', '')
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

	return description, flag


def make_hba(plaintext: str) -> tuple:
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
	M = rsa_ascii_encode(plaintext, m_len)
	n_len = (m_len * 9) + 1
	e = 3
	p, q, n1 = crt_e_maker(e, n_len)
	c1 = rsa_encrypt(M, e, n1)

	p, q, n2 = crt_e_maker(e, n_len)
	c2 = rsa_encrypt(M, e, n2)

	p, q, n3 = crt_e_maker(e, n_len)
	c3 = rsa_encrypt(M, e, n3)

	# The code below makes sure that python doesn't append an "L" to the end of the hex encoded number.
	c3 = hex(c3).replace('L', '')
	c2 = hex(c2).replace('L', '')
	c1 = hex(c1).replace('L', '')
	n1 = hex(n1).replace('L', '')
	n2 = hex(n2).replace('L', '')
	n3 = hex(n3).replace('L', '')

	description = f"""<p>You were enjoying your leftover Chinese food minding your own business watching reruns of Broadcast tv when your buddy sent you a message. He managed to intercept some secret communications. The messages were encrypted with RSA he's managed to get your the ciphertexts and also the public key components below.</p>
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
	return description, plaintext


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
	n_len = (m_len * 15) + 1
	p, q, n = calc_n(n_len)
	l_n = calc_lambda(p, q)
	e1 = calc_e(12, l_n)
	c1 = rsa_encrypt(M, e1, n)
	c1 = hex(c1).replace('L', '')
	e2 = calc_e(12, l_n)
	c2 = rsa_encrypt(M, e2, n)
	c2 = hex(c2).replace('L', '');
	n = hex(n).replace('L', '')
	description = f"""<p>The Transcendentalists have given you another challenge. This time they want you to give them the secret phrase. Once again they say this is Elementary for you to solve.</p>
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
	return description, plaintext


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
	M = rsa_ascii_encode(plaintext, m_len)
	n_len = (m_len * 9) + 1
	p, q, n = calc_n(n_len)
	l_n = calc_lambda(p, q)
	e = calc_e(16, l_n)
	d = mod_inv(e, l_n)
	r = calc_r(n)
	M_fake = (M * pow(r, e)) % n
	S = pow(M_fake, d, n)
	S_fake = (S * mod_inv(r, n)) % n
	M_fake = hex(M_fake).replace('L', '')
	S_fake = hex(S_fake).replace('L', '')
	n = hex(n).replace('L', '')
	M = hex(M).replace('L', '')
	e = hex(e).replace('L', '')
	S = hex(S).replace('L', '')
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
	return description, flag


def make_fermat_chal(plaintext: str) -> tuple:
	"""
	Makes a challenge that requires the person to factor the public key via
	Fermat's Near Prime Factorization method.

	:param plaintext: The plaintext message they have to provide as the flag.
	:return: description,plaintext The description of the flag and the plaintext itself.
	"""

	m_len = len(plaintext)
	M = rsa_ascii_encode(plaintext, m_len)
	n_len = (m_len * 9) + 1
	p, q, n, e, d = make_fermat(n_len)
	C = rsa_encrypt(M, e, n)
	C = hex(C).replace('L', '')
	e = hex(e).replace('L', '')
	n = hex(n).replace('L', '')
	description = f"""<p>our friend told you about a group called the Transcendentalists. They gave you a challenge to get into their group. They say the answer is simply "Elementary". They want you to decrypt the message they gave you. </p>
<p>When you see that the key is {n_len}bits in length they still tell you "It's Elementary my dear Watson." and refuse to say anything more.</p>

<p class="text-monospace">
C = {C}<br />
e = {e}<br />
n = {n}<br />
</p>
<br />
Free hint. This plaintext was encoded with OS2IP.
"""
	return description, plaintext
