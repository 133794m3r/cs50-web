#  Macarthur Inbody <admin-contact@transcendental.us>
#  Licensed under LGPLv3 Or Later (2020)
from io import BytesIO
from random import randint
from datetime import datetime, timedelta

def simple_math() -> tuple:
	"""
	This will generate a simple captcha where the user has to either +,-,*,/
	two numbers. For division it is actually the answer / number a or b.
	All numbers are from 0-12.

	:return: str:math_formula, int:answer
	"""
	a = randint(0, 12)
	b = randint(0, 12)
	ans = 0
	captcha_str = ''
	method = randint(0, 3)

	if method == 0:
		b = randint(0, 12)
		ans = a + b
		op = "plus" if randint(1, 3) == 1 else "+"

	elif method == 1:
		a = randint(b, 12)
		ans = a - b
		op = "minus" if randint(1, 3) == 1 else "-"
	elif method == 2:
		ans = a * b
		op = "times" if randint(1, 3) == 1 else "*"
	elif method == 3:
		c = a * b
		if b > a:
			ans = a
			a = c
		else:
			ans = b
			b = a
			a = c
		op = "divided by" if randint(0, 1) == 1 else "/"

	num_str = {0: 'Zero', 1: 'One', 2: 'Two', 3: 'Three',
	           4: 'Four', 5: 'Five', 6: 'Six', 7: 'Seven',
	           8: 'Eight', 9: 'Nine', 10: 'Ten', 11: 'Eleven',
	           12: 'Twelve'}
	b = num_str[b] if randint(1, 5) == 1 else b

#expires = datetime.now() + timedelta(seconds=30)
	return f"{a} {op} {b}", ans


def img_captcha():
	"""
	Generates an image captcha where each letter is of a randomly selected
	color. All letters are chosen from the Zbase32 alphabet. The person
	solving the captcha has to enter all characters that are of a certain color.
	it always makes sure that there is at least 1.

	:return: str:correct_letters,str:color_name, str:img_str
	"""
	from PIL import Image, ImageDraw, ImageFont, ImagePalette
	from random import randint
	import base64
	charset = 'ybndrfg8ejkmcpqxot1uwisza345h769'
	chars = 31
	text = ''
	for i in range(6):
		text += charset[randint(0, chars)]

	font_size = 26
	fnt = ImageFont.truetype('SourceCodePro-Bold.otf', font_size)
	size = fnt.getsize(text)
	width = (size[0] // len(text))
	size = (int(size[0] + (width * 1.2)), int(font_size * 1.5))
	img = Image.new('RGB', size, color=(255, 255, 255))
	d = ImageDraw.Draw(img)
	colors = [(0, 0, 0), (255, 0, 0),  (0, 0, 255)]
	color_names = ['black', 'red', 'blue']
	correct_index = randint(0, 2)
	correct_letters = ''
	start = 4
	for i, x in enumerate(text):
		index = randint(0, 2)
		if index == correct_index:
			correct_letters+=x
		color = colors[index]
		d.text((start + (i * width) + 2, 0), x, font=fnt, fill=color)

	if len(correct_letters) == 0:
		i = randint(0, 4)
		x = text[i]
		d.text((start + (i * width) + 2, 0), x, font=fnt, fill=colors[correct_index])
		correct_letters+=x

	buffered = BytesIO()
	img.save(buffered,format="PNG")
	buffered.seek(0)
	img_bytes = buffered.getvalue()
	img_str = base64.b64encode(img_bytes).decode()
	color_name = color_names[correct_index]

	return correct_letters, color_name, img_str


def generate_captchas(request: object) -> tuple:
	"""
	This function will generate the captchas, and also sets up the session
	variables so that when the user tries to solve the captcha it is all setup.
	The captcha is also set to expire after 45 seconds. This way a normal user
	can attempt to solve it but a bot/automated system shouldn't be able to handle it.

	:param request: The UWSGI Request object.
	:return: str:math_msg, str:color_name, str:img_str
	"""
	time = datetime.utcnow() + timedelta(seconds=45)
	# print(time.timestamp())
	request.session['captcha_expires'] = time.timestamp()
	correct_letters, color_name, img_str = img_captcha()
	math_msg, correct_ans = simple_math()
	request.session['correct_letters'] = correct_letters
	request.session['captcha_answer'] = correct_ans
	request.session['captcha_valid'] = False

	return math_msg,color_name,img_str


def check_captchas(request: object, user_letters: str, user_math_ans: int) -> bool:
	"""
	This function will check the answers provided by the user against the values
	stored for their session. If they answer it correctly then it sets the
	captcha expires to be 1m from this time. This is mainly for the login form
	because it means that the user doesn't have to solve another captcha for this
	amount of time if they become rate-limited again.

	:param request: The UWSGI Request Object.
	:param user_letters: The letters the user provided.
	:param user_math_ans: The answer the user provided to us.
	:return:
	"""
	math_msg = ''
	color_name = ''
	img_str = ''
	#print(request.session['captcha_answer'], user_math_ans, request.session['correct_letters'], user_letters)
	if request.session['captcha_answer'] == user_math_ans and request.session['correct_letters'] == user_letters:
		request.session['captcha_valid'] = True
		#If they solve it then they don't have to try to do another one for a good while. 1m feels like long enough.
		request.session['captcha_expires'] = (datetime.utcnow() + timedelta(minutes=1)).timestamp()
		return True
	else:
		return False
