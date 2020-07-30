class CookiesInvalid(Exception):
	class CookiesInvalid(Exception):
		def __init__(self):
			super(CookiesInvalid.CookiesInvalid, self).__init__("cookies not valid")

	def __init__(self):
		raise CookiesInvalid.CookiesInvalid

class PeopleNotFound(Exception):
	class PeopleNotFound(Exception):
		def __init__(self, username):
			super(PeopleNotFound.PeopleNotFound, self).__init__("not found people with username '{}'".format(username))

	def __init__(self, username):
		raise PeopleNotFound.PeopleNotFound(username)

class Error429(Exception):
	def __init__(self):
		super(Error429, self).__init__("limit is obtained")