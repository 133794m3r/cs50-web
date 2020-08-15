from random import randint


def make_fizzbuzz(start: int, end: int) -> tuple:
	"""
	Makes a challenge based upon a basic fizzbuzz challenge for the users to try to solve.

	:param start: The starting value we're going to count from.
	:param end: The end number they're going to be counting to.
	:return: A tuple containing the description and the flag.
	"""

	flag = ''
	description = ''
	start = start or randint(1, 3)
	max_num = end or randint(2500, 3000)
	variety = randint(1, 2)

	if variety == 1:
		num1 = randint(4, 13)
		num2 = randint(num1 + 1, num1 + 5)
		num3 = num1 * num2
		summed = 0
		for i in range(start, max_num):
			if not (i % num1):
				summed += i + 3
			elif not (i % num2):
				summed += i - 2
			elif not (i % num3):
				summed += i * i
			else:
				summed += i

		flag = summed
		summed = 0
		for i in range(start, (num1 * num2) + 10):
			if not (i % num1):
				summed += i + 3
			elif not (i % num2):
				summed += i - 2
			elif not (i % num3):
				summed += i * i
			else:
				summed += i

		description = f"""<p>Write a program that adds all numbers together from {start} to {max_num - 1}(inclusive). If the number is even divisible by {num1} then add 3 and that number to the total. If the number is evenly divisible by {num2} then add that number minus 2 to the running total. If the number is divisble by {num1} and {num2} then add that number squared. Otherwise simply add the number to the total. Your test case is given below.</p><br /><br /> <p>Running this algorithm on all numbers between {start} and {(num1 * num2) + 9} would result in the number {summed}. Verify that your program gets the same result before attempting to submit. You are free to use any language that you wish.</p>"""
	elif variety == 2:
		num1 = randint(4, 13)
		num2 = randint(num1 + 1, num1 + 5)
		num3 = num1 * num2
		num1_counts = 0
		num2_counts = 0
		num3_counts = 0
		other_counts = 0

		for i in range(start, max_num):
			if not (i % num3):
				num3_counts += 1
				num1_counts += 1
				num2_counts += 1
			elif not (i % num1):
				num1_counts += 1
			elif not (i % num2):
				num2_counts += 1
			else:
				other_counts += 1

		flag = f"{num1_counts},{num2_counts},{num3_counts},{other_counts}"
		summed = 0
		num1_counts = 0
		num2_counts = 0
		num3_counts = 0
		other_counts = 0
		for i in range(start, (num1 * num2) + 10):
			if not (i % num3):
				num3_counts += 1
				num1_counts += 1
				num2_counts += 1
			elif not (i % num1):
				num1_counts += 1
			elif not (i % num2):
				num2_counts += 1
			else:
				other_counts += 1

		description = f"""<p>Write a program that goes from {start} to {max_num - 1}(inclusvie). Get the number of times that a number is divisible by {num1},{num2},{num3}, and a count for the numbers no divisible by any of the previous 3. At the end arrange the counts like so(seperated by a comma. num1_count,num2_count,num3_count,other_count. The example case is given to you below.</p><br /> <p>If you run the same algoright on all numbers between {start} and {(num1 * num2) + 9}(inclusive). You'd get the following answer. {num1_counts},{num2_counts},{num3_counts},{other_counts}. So your flag would be the preceeding string. with the numbers seperated by a single "," and no other characters around them.</p>"""

	return description, flag
