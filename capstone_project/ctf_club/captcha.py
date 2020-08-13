#  Macarthur Inbody <admin-contact@transcendental.us>
#  Licensed under LGPLv3 Or Later (2020)
from io import BytesIO
from random import randint
from datetime import datetime, timedelta
from django.core.serializers.json import DjangoJSONEncoder
from json import dumps
def simple_math():
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

	:return: correct_letters,color_name, img_str
	"""
	from PIL import Image, ImageDraw, ImageFont, ImagePalette
	from random import randint
	import base64
	#pallete = [(0, 0, 0), (255, 0, 0,), (0, 127, 0), (0, 0, 255), (255, 255, 255)]
	#ImagePalette.ImagePalette('P', pallete, size=5)
	charset = 'ybndrfg8ejkmcpqxot1uwisza345h769'
	chars = 31
	text = ''
	for i in range(6):
		text += charset[randint(0, chars)]

	font_size = 26
	fnt = ImageFont.truetype('SourceCodePro-Bold.otf', font_size)
	size = fnt.getsize(text)
	width = (size[0] // len(text))
	size = (int(size[0] + (width * 2)), int(font_size * 1.5))
	img = Image.new('RGB', size, color=(255, 255, 255))
	d = ImageDraw.Draw(img)
	colors = [(0, 0, 0), (255, 0, 0), (0, 127, 0), (0, 0, 255)]
	color_names = ['black', 'red', 'green', 'blue']
	correct_index = randint(0, 3)
	correct_letters = ''
	start = width - 8
	for i, x in enumerate(text):
		index = randint(0, 3)
		if index == correct_index:
			correct_letters+=x
		color = colors[index]
		d.text((start + (i * width) + 3, 0), x, font=fnt, fill=color)

	if len(correct_letters) == 0:
		i = randint(0, 4)
		x = text[i]
		d.text((start + (i * width) + 3, 0), x, font=fnt, fill=colors[correct_index])
		correct_letters+=x
	buffered = BytesIO()
	img.save(buffered,format="PNG")
	buffered.seek(0)
	img_bytes = buffered.getvalue()
	img_str = base64.b64encode(img_bytes).decode()
	color_name = color_names[correct_index]
	print(size)
	return correct_letters, color_name, img_str

def check_captchas(request,user_letters,user_math_ans):
	math_msg = ''
	color_name = ''
	img_str = ''
	print(request.session['captcha_answer'], user_math_ans, request.session['correct_letters'], user_letters)
	if request.session['captcha_answer'] == user_math_ans and request.session['correct_letters'] == user_letters:
		request.session['captcha_valid'] = True
		print('valid')

	else:
		time = datetime.now() + timedelta(seconds=29)
		request.session['captcha_expires'] = time.timestamp()
		correct_letters,color_name, img_str = img_captcha()
		math_msg,correct_ans = simple_math()
		request.session['correct_letters'] = correct_letters
		request.session['captcha_answer'] = correct_ans
		request.session['captcha_valid'] = False
	return math_msg,color_name,img_str