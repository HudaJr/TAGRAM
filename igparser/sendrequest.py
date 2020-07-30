import requests
from . import exception
from . import parsing

class HttpRequest(requests.Session):
	def __init__(self):
		super(HttpRequest, self).__init__()
		self.headers.update({"user-agent":"Mozilla/5.0 (iPhone; CPU iPhone OS 12_3_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148 Instagram 105.0.0.11.118 (iPhone11,8; iOS 12_3_1; en_US; en-US; scale=2.00; 828x1792; 165586599)"})
		self.html = "<h1>Salis Tamvan</h1>"

	def set_cookies(self, cookies):
		try:
			if type(cookies) == str:
				cookies = self.dict_cookies(cookies)
			if not "csrftoken" in cookies.keys():
				raise exception.CookiesInvalid("csrftoken not found in cookies")
			self.cookies = requests.utils.cookiejar_from_dict(cookies)
			self.headers.update({"x-csrftoken":cookies["csrftoken"]})
		except (IndexError, KeyError):
			pass

	def dict_cookies(self, cookies):
		data = cookies.replace(" ", "").split(";")
		data = list(map(lambda x: x.split("="), data))
		data = {x[0]:x[1] for x in data}
		return data

	def bs4(self):
		return parsing.to_bs4(self.html)

	def get(self, url, **kwargs):
		rv = super(HttpRequest, self).get(url, **kwargs)
		self.html = rv.text

		if rv.status_code == 429:
			raise exception.Error429

		return rv

	def post(self, url, **kwargs):
		rv = super(HttpRequest, self).post(url, **kwargs)
		self.html = rv.text

		if rv.status_code == 429:
			raise exception.Error429

		return rv



