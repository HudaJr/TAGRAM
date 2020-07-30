from . import parsing
from . import exception
import json

def err_handler(exceptFunc, errFunc):
	def decorator(func):
		def wrapper(*args, **kwargs):
			try:
				return func(*args, **kwargs)
			except exceptFunc:
				return errFunc()
		return wrapper
	return decorator

def check_login(html = None):
	def decorator(func):
		def wrapper(*args, **kwargs):
			data = func(*args, **kwargs)
			if not parsing.get_sharedData(html if html else data)["config"].get("viewer"):
				raise exception.CookiesInvalid
		return wrapper
	return decorator

def actionChecker(func):
	def wrapper(*args, **kwargs):
		data = func(*args, **kwargs)
		try:
			data = json.loads(data)
		except:
			if "html" in data:
				raise Exception("not found data")
		return data
	return wrapper