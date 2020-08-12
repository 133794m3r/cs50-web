#Programming Chals
from .libctf import make_masterhacker,make_fizzbuzz
#RSA Flags
from .libctf import make_fermat_chal, make_bsa, make_hba, make_rsa, make_common_mod
#Classical Ciphers
from .libctf import make_hill, make_affine

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

CHALLENGE_FUNCS = {
	"fizzbuzz":make_fizzbuzz,
	"hba":make_hba,
	"fermat":make_fermat_chal,
	"hill":make_hill,
	"bsa":make_bsa,
	"rsa":make_rsa,
	"affine":make_affine,
	"common_mod":make_common_mod,
	"master_hacker":make_masterhacker,
}

CATEGORIES = ["Classical Crypto","Modern Crypto","Programming"]

#TODO: Move all of this into an SQL table that'll actually hold this meta-data for me.

CHALLENGES_TEMPLATES = [
	{"name":"Cola and the Bee", "sn":"fizzbuzz", "category":"Programming", "description":
		"""This is a basic fizzbuzz challenge where you have to  provide a min an maximum number.
		The maximum minus 1 is the number that is counted to.""",
	 "points":75, "variety":False,"files":False},
	{"name":"Really Simple Algorithm - Frenchman's Revenge", "sn":"fermat", "category":"Modern Crypto", "description":
		"This is an attack on RSA. This challenge is also known as 'Fermat's Near prime' attack."
		" Provide the plain-text and the app will do the rest.",
	 "points":240,"variety":False,"files":False},
	{"name":"Master of Hill Climbing", "sn":"hill", "category":"Classical Crypto", "description":
		"This challenge is all about the hill cipher. Select the easy version for one where the user is given the key. "
		"The medium mode for when they shouldn't be given the key at the start.",
	 "points":70, "variety":True,"files":False},
	{"name":"Really Simple Algorithm - Intro", "sn":"rsa", "category":"Modern Crypto",
	 "description":"This challenge is just a simple RSA based challenge that requires the user to decrypt some message.",
	 "points":150, "variety":False,"files":False},
	{"name":"Really Simple Algorithm - Fake it till you make it", "sn":"bsa", "category":"Modern Crypto",
	 "description":
		 "This is an attack on RSA called the 'Blind Signature Attack'. To keep it simple we're going to have them work "
		 "with a message that's already been signed.", "points":225, "variety":False,"files":False},
	{"name":"A-fine Cipher", "sn":"affine", "category":"Classical Crypto", "description":
		"This challenge is all about the affine cipher which is basically just a 2-step Ceaser Cipher."
		" Easy mode gives them the key. Medium mode doesn't give them a key but does give them a crib.",
	 "points":100, "variety":True,"files":False},
	{"name":"Really Simple Algorithm - It's all the Same", "sn":"common_mod", "category":"Modern Crypto",
	 "description":"This challenge requires someone to carry out a common modulus attack against RSA.",
	 "points":45, "variety":False,"files":False},
	{"name":"Really Simple Algorithm - Leftover Chinese Food", "sn":"hba", "category":"Modern Crypto",
	 "description":"This challenge requires the solver to utilize the Hastaad Broadcast Attack against RSA.",
	 "points":300, "variety":False,"files":False},
	{"name":"The Master Hacker", "sn":"master_hacker", "category":"Programming",
	 "description":"This challenge is the bounded knapsack problem. A staple of algorithm interview questions.",
	 "points":200, "variety":False,"files":True},
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

def rot_encode(msg):
	shift = randint(1,25)
	out = ''
	for c in msg:
		x = ord(c)
		if 65 <= x <= 90:
			#add the shift.
			x+=shift;
			#if it's greater than 'Z'.
			if x>=90:
				#handle overflows.
				x=(x-90)+64;
		
		#else if it's lowercase ascii.
		elif 97 <= x <= 122:
			#same thing again.
			x+=shift;
			#same if it's greater than 'z'.
			if x>=122:
				#handle overflow.
				x=(x-122)+96;
		
		out += chr(x)
	return out

#since this is a ctf site I'll have them solve a simple ceaser cipher message along with a basic math question.
def make_rot_captcha():
	translation = {'A':['Alpha','Afirm','Able'],
	'B':['Bravo','Baker','Buy'],
	'C':['Charlie','Charlie','Cast'],
	'D':['Delta','Dog','Dock'],
	'E':['Echo','Easy','Easy'],
	'F':['Foxtrot','Fox','France'],
	'G':['Golf','George','Greece'],
	'H':['Hotel','How','Have'],
	'I':['India','Italy','Item'],
	'J':['Juliet','Jig','John'],
	'K':['Kilo','Kimberly','King'],
	'L':['Lima','Love','Lima'],
	'M':['Mama','Mary','Mike'],
	'N':['November','Nan','Nap'],
	'O':['Oscar','Oboe','Opal'],
	'P':['Papa','Peter','Pup'],
	'Q':['Quebec','Queen','Quack'],
	'R':['Romeo','Roger','Rush'],
	'S':['Sierra','Sugar','Sail'],
	'T':['Tango','Tare','Tape'],
	'U':['Uniform','Uncle','Unit'],
	'V':['Victor','Victor','Vice'],
	'W':['Whiskey','William','Watch'],
	'X':['Xray','X-ray','X-Ray'],
	'Y':['Yankee','York','Yoke'],
	'Z':['Zulu','Zebra','Zed']}

	words = ['COME', 'DEAD', 'DIED', 'FOUR', 'FROM', 'FULL', 'GAVE', 'HAVE', 'HERE', 'LAST', 'LIVE', 'LONG', 'NOTE', 'POOR', 'TAKE', 'TASK', 'THAT', 'THEY', 'THIS', 'THUS', 'VAIN', 'WHAT', 'WILL', 'WORK', 'ABOVE', 'BIRTH', 'BRAVE', 'CAUSE', 'CIVIL', 'EARTH', 'EQUAL', 'FIELD', 'FINAL', 'FORTH', 'GREAT', 'LIVES', 'MIGHT', 'NEVER', 'NOBLY', 'PLACE', 'POWER', 'SCORE', 'SENSE', 'SEVEN', 'SHALL', 'THEIR', 'THESE', 'THOSE', 'UNDER', 'WHICH', 'WORLD', 'YEARS', 'BEFORE', 'ENDURE', 'FORGET', 'FOUGHT', 'GROUND', 'HALLOW', 'HIGHLY', 'LARGER', 'LITTLE', 'LIVING', 'NATION', 'PEOPLE', 'PERISH', 'PROPER', 'RATHER', 'SHOULD', 'BROUGHT', 'CREATED', 'DETRACT']
	word_len = 70
	word = words[randint(0,70)]
	msg = ''
	for c in word:
		msg += translation[c][randint(0,2)] + ' '
	captcha_msg = rot_encode(msg)

	return captcha_msg,msg


def simple_math():
	a = randint(0,12)
	b = randint(0,12)
	ans = 0
	captcha_str = ''
	method = randint(0,3)

	if method == 0:
		b = randint(0,12)
		ans = a+b
		op = "plus" if randint(1,3) == 1 else "+"

	elif method == 1:
		a = randint(b,12)
		ans = a - b
		op = "minus" if randint(1,3) == 1 else "-"
	elif method == 2:
		ans = a * b
		op = "times" if randint(1,3) == 1 else "*"
	elif method == 3:
		c = a * b
		if b > a:
			ans = a
			a = c
		else:
			ans = b
			b = a
			a = c
		op = "divided by" if randint(0,1) == 1 else "/"

	num_str = {0: 'Zero', 1: 'One', 2: 'Two', 3: 'Three',
	           4: 'Four', 5: 'Five', 6: 'Six', 7: 'Seven',
	           8: 'Eight', 9: 'Nine', 10: 'Ten', 11: 'Eleven',
	           12:'Twelve'}
	b = num_str[b] if randint(1,5) == 1 else b

	return f"{a} {op} {b}",ans

