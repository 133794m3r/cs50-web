#  Macarthur Inbody <admin-contact@transcendental.us>
#  Licensed under LGPLv3 Or Later (2020)

import datetime
from urllib import parse
import pyotp
import qrcode

class TotpAuthorize:
	def __init__(self, secret=None):
		if secret is None:
			secret = pyotp.random_base32()
		self.secret = secret
		self.totp = pyotp.TOTP(secret)

	def generate_token(self):
		return self.totp.now()

	def valid(self, token):
		token = int(token)
		now = datetime.datetime.now()
		prior_time = now + datetime.timedelta(seconds=-30)
		try:
			valid_now = self.totp.verify(token)
			valid_past = self.totp.verify(token, for_time=prior_time)
			return valid_now or valid_past
		except:
			return False

	def qrcode(self, username):
		print(username)
		#username = ' %8&'
		uri = self.totp.provisioning_uri(username)

		uri = parse.unquote(uri)
		return qrcode.make(uri)