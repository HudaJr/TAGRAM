from . import data as dt
from . import parsing
from . import output
from . import exception
from . import dump
from .checker import *
import json

def more_dump(func, args = [], kwargs = {}, limit = 20):
	data = func(*args, **kwargs)
	ses = args[0]
	if limit > 3000:
		limit = 3000

	if func == dump.post_home:
		query_hash = dt.POST_IN_HOME
		func_items = lambda data: data["data"]["user"]["edge_web_feed_timeline"]["edges"]
		next_func = lambda data: data["data"]["user"]["edge_web_feed_timeline"]["page_info"].get("end_cursor")
		output_func = output.Post

	elif func == dump.post_people:
		query_hash = dt.POST_IN_PEOPLE
		func_items = lambda data: data["data"]["user"]["edge_owner_to_timeline_media"]["edges"]
		next_func = lambda data: data["data"]["user"]["edge_owner_to_timeline_media"]["page_info"].get("end_cursor")
		output_func = output.Post

	elif func == dump.follower_people:
		query_hash = dt.FOLLOWER
		func_items = lambda data: data["data"]["user"]["edge_followed_by"]["edges"]
		next_func = lambda data: data["data"]["user"]["edge_followed_by"]["page_info"].get("end_cursor")
		output_func = output.People

	elif func == dump.following_people:
		query_hash = dt.FOLLOWING
		func_items = lambda data: data["data"]["user"]["edge_follow"]["edges"]
		next_func = lambda data: data["data"]["user"]["edge_follow"]["page_info"].get("end_cursor")
		output_func = output.People


	else:
		raise Exception("function '{}' not support for more dump".format(func.__name__))

	rv = data.items
	ses = args[0]
	del args[0]

	next = data.next
	idPeople = data.idPeople
	if not data.isNext or len(rv) >= limit:
		return data.items[:limit]

	while next:
		url = "https://www.instagram.com/graphql/query/?query_hash={}&variables=%7B%22id%22%3A%22{}%22%2C%22first%22%3A12%2C%22after%22%3A%22{}%3D%22%7D".format(query_hash, idPeople, next)
		data = ses.session.get(url).json()
		items = func_items(data)
		items = parsing.sorting(lambda x: output_func(ses, x), items)
		next = next_func(data)
		if type(next) == str:
			next = next.replace("==", "%3D")

		rv += items
		if len(rv) >= limit:
			return rv[:limit]
	return rv[:limit]

@actionChecker
def comment_post(ses, idPost, comment):
	data = ses.session.post("https://www.instagram.com/web/comments/{}/add/".format(idPost), data = {"comment_text":comment}).text
	return data

@actionChecker
def like_post(ses, idPost):
	#url = ses.session.get('https://i.instagram.com/api/v1/media/2362590223910854800_37474448914/permalink/').json()["permalink"]
	#ses.session.get(url)
	
	data = ses.session.post("https://www.instagram.com/web/likes/{}/like/".format(idPost)).text
	return data

@actionChecker
@err_handler(KeyError, lambda: "people not found")
def unlike_post(ses, idPost):
	data = ses.session.post("https://www.instagram.com/web/likes/{}/unlike/".format(idPost)).text
	return data

@actionChecker
@err_handler(KeyError, lambda: "people not found")
def follow_people(ses, usernamePeople, idPeople = None):
	hulu = {'accept': '*/*', 'accept-encoding': 'gzip, deflate, br', 'accept-language': 'en-US,en;q=0.9', 'content-length': '0', 'content-type': 'application/x-www-form-urlencoded', 'origin': 'https://www.instagram.com', 'referer': 'https://www.instagram.com/{}/'.format(usernamePeople), 'sec-fetch-dest': 'empty', 'sec-fetch-mode': 'cors', 'sec-fetch-site': 'same-origin', 'x-ig-app-id': '936619743392459', 'x-instagram-ajax': '649268ec3eb2', 'x-requested-with': 'XMLHttpRequest'}

	if not idPeople:
		try:
			idPeople = ses.session.get("https://instagram.com/{}?__a=1".format(usernamePeople)).json()["logging_page_id"].replace("profilePage_", "")
		except json.decoder.JSONDecodeError:
			return "people not found"
			
	data = ses.session.post("https://www.instagram.com/web/friendships/{}/follow/".format(idPeople), headers = {**ses.session.headers, **hulu}).text
	return data

@actionChecker
def unfollow_people(ses, usernamePeople, idPeople = None):
	if not idPeople:
		try:
			idPeople = ses.session.get("https://instagram.com/{}?__a=1".format(usernamePeople)).json()["logging_page_id"].replace("profilePage_", "")
		except json.decoder.JSONDecodeError:
			return "people not found"

	data = ses.session.post("https://www.instagram.com/web/friendships/{}/unfollow/".format(idPeople)).text
	return data