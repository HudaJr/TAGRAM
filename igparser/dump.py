from . import parsing
from . import output
from . import exception
from .checker import *
import re

def post_home(ses):
	html = ses.session.get("https://instagram.com").text
	json_ = parsing.get_dataLoaded(html)
	data = json_["user"]["edge_web_feed_timeline"]["edges"]
	data = parsing.sorting(lambda x: output.Post(ses, x), data)

	idPeople = json_["user"]["id"]
	next = json_["user"]["edge_web_feed_timeline"]["page_info"].get("end_cursor")
	return output.Output(items = data, data = json_, idPeople = idPeople, next = next)

def post_people(ses, usernamePeople = None):
	try:
		html = ses.session.get("https://instagram.com/{}".format(usernamePeople)).text
		json_ = parsing.get_sharedData(html)
		data = json_["entry_data"]["ProfilePage"][0]["graphql"]["user"]["edge_owner_to_timeline_media"]["edges"]
		data = parsing.sorting(lambda x: output.Post(ses, x), data)
		next = json_["entry_data"]["ProfilePage"][0]["graphql"]["user"]["edge_owner_to_timeline_media"]["page_info"].get("end_cursor")
		idPeople = json_["entry_data"]["ProfilePage"][0]["graphql"]["user"]["id"]
		return output.Output(items = data, data = json_, idPeople = idPeople, next = next)
	except KeyError:
		raise exception.PeopleNotFound(usernamePeople)

def follower_people(ses, usernamePeople = None, idPeople = None):
	@err_handler(json.decoder.JSONDecodeError, lambda: exception.CookiesInvalid())
	@err_handler(KeyError, lambda: exception.PeopleNotFound(usernamePeople if usernamePeople else idPeople))
	def inner(idPeople):
		if not idPeople:
			idPeople = ses.session.get("https://instagram.com/{}?__a=1".format(usernamePeople)).json()["logging_page_id"].replace("profilePage_", "")

		json_ = ses.session.get("https://www.instagram.com/graphql/query/?query_hash=c76146de99bb02f6415203be841dd25a&variables=%7B%22id%22%3A%22{}%22%2C%22include_reel%22%3Atrue%2C%22fetch_mutual%22%3Atrue%2C%22first%22%3A24%7D".format(idPeople)).json()
		data = json_["data"]["user"]["edge_followed_by"]["edges"]
		data = parsing.sorting(lambda x: output.People(ses, x), data)

		next = json_["data"]["user"]["edge_followed_by"]["page_info"].get("end_cursor")
		return output.Output(items = data, data = json_, idPeople = idPeople, next = next)

	return inner(idPeople)

def following_people(ses, usernamePeople = None, idPeople = None):
	@err_handler(json.decoder.JSONDecodeError, lambda: exception.CookiesInvalid())
	@err_handler(KeyError, lambda: exception.PeopleNotFound(usernamePeople if usernamePeople else idPeople))
	def inner(idPeople):
		if not idPeople:
			idPeople = ses.session.get("https://instagram.com/{}?__a=1".format(usernamePeople)).json()["logging_page_id"].replace("profilePage_", "")

		json_ = ses.session.get("https://www.instagram.com/graphql/query/?query_hash=d04b0a864b4b54837c0d870b0e77e076&variables=%7B%22id%22%3A%22{}%22%2C%22include_reel%22%3Atrue%2C%22fetch_mutual%22%3Atrue%2C%22first%22%3A24%7D".format(idPeople)).json()
		data = json_["data"]["user"]["edge_follow"]["edges"]
		data = parsing.sorting(lambda x: output.People(ses, x), data)

		next = json_["data"]["user"]["edge_follow"]["page_info"].get("end_cursor")
		return output.Output(items = data, data = json_, idPeople = idPeople, next = next)

	return inner(idPeople)

