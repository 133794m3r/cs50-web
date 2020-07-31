from .libctf import *
from random import randint

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
	description = f"""Given the following string of characters you have to decrypt them. {ct}.<br />"""
	if variety == 1:
		description+=f"""From your "inside man", you were able to get the following string of numbers. What could they mean?<br /> {key}"""

	return description,flag


def make_rsa(plaintext):
	M = rsa_ascii_encode(plaintext,len(plaintext))

def make_common_mod(plaintext):
	pass

def make_hba(plaintext):
	pass

def make_bsa(plaintext):
	pass

def make_fermat(plaintext):
	pass

def make_affine(plaintext,variety):
	pass

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

		description = f"""Write a program that adds all numbers together from {start} to {max_num-1}(inclusive). If the number is even divisible by {num1} then add 3 and that number to the total. If the number is evenly divisible by {num2} then add that number minus 2 to the running total. If the number is divisble by {num1} and {num2} then add that number squared. Otherwise simply add the number to the total. Your test case is given below.<br /><br /> Running this algorithm on all numbers between {start} and {(num1*num2)+9} would result in the number {summed}. Verify that your program gets the same result before attempting to submit. You are free to use any language that you wish."""
	elif variety == 2:
		num1 = randint(4,13)
		num2=randint(num1+1,num1+5)
		num3 = num1*num2
		num1_counts = 0
		num2_counts = 0
		num3_counts = 0
		other_counts = 0

		for i in range(start,max_num):
			if not(i % num1):
				num1_counts += 1
			elif not(i%num2):
				num2_counts += 1
			elif not(i%num3):
				num3_counts += 1
			else:
				other_counts +=1

		flag = f"{num1_counts},{num2_counts},{num3_counts},{other_counts}"
		summed = 0
		num1_counts = 0;num2_counts=0;num3_counts=0;other_counts=0;
		for i in range(start,(num1*num2)+10):
			if not(i%num1):
				num1_counts +=1
			elif not(i%num2):
				num2_counts += 1
			elif not(i%num3):
				num3_counts +=1
			else:
				other_counts +=1

		description = f"""Write a program that goes from {start} to {max_num - 1}(inclusvie). Get the number of times that a number is divisible by {num1},{num2},{num3}, and a count for the numbers no divisible by any of the previous 3. At the end arrange the counts like so(seperated by a comma. num1_count,num2_count,num3_count,other_count. The example case is given to you below.<br /><br /> If you run the same algoright on all numbers between {start} and {(num1*num2)+9}(inclusive). You'd get the following answer. {num1_counts},{num2_counts},{num3_counts},{other_counts}. So your flag would be the preceeding string. with the numbers seperated by a single "," and no other characters around them.
				"""

	return description,flag

CHALLENGE_FUNCS = {
	"fizzbuzz":make_fizzbuzz,
	"hba":make_hba,
	"fermat":make_fermat,
	"hill":make_hill,
	"bsa":make_bsa,
	"rsa":make_rsa,
	"affine":make_affine
}
CATEGORIES = ["Classical Crypto","Modern Crypto","Programming"]

CHALLENGES = [
		{"name":"Cola and the Bee", "sn":"fizzbuzz", "category":"Programming", "description":"Please provide a min an maximum number for the Fizzbuzz like challenge."},
		{"name":"Broadcast TV", "sn":"hba", "category":"Modern Crypto", "description":"This is an attack on RSA. The HBA requires you to provide the plain-text for the challenge. Then the flag will be created for more info refer to the resources page."},
		{"name":"Frenchman's Revenge", "sn":"fermat", "category":"Modern Crypto", "description":"This is an attack on RSA. This challenge is also known as 'Fermat's Near prime' attack. Provide the plain-text and the app will do the rest."},
		{"name":"Master of Hill Climbing", "sn":"hill", "category":"Classical Crypto", "description":"This challenge is all about the hill cipher. Select the easy version for one where the user is given the key. The hard mode for when they shouldn't be given the key at the start."},
		{"name":"Really Simple Algorithm", "sn":"rsa", "category":"Classical Crypto", "description":"This challenge is just a simple RSA based challenge that requires the user to decrypt some message."},
		{"name":"Signature of the Blind", "sn":"bsa", "category":"Modern Crypto", "description":"This is an attack on RSA called the 'Blind Signature Attack'. To keep it simple we're going to have them work with a message that's already been signed."},
		{"name":"A-fine Cipher", "sn":"affine", "category":"Classical Crypto", "description":"This challenge is all about the affine cipher which is basically just a 2-step Ceaser Cipher."}
]
