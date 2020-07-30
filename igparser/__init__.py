# coded by: salism3
# 30 - 07 - 2020

from . import sendrequest
from . import parsing
from . import exception
from . import action
from .checker import *
import json, re

class Account:
	def __init__(self, cookies):
		self.session = sendrequest.HttpRequest()
		self.__logged = False
		self.name = None
		self.username = None
		self.id = None
		self.profile_picture = None
		self.biography = None
		self.total_followers = None
		self.total_following = None
		self.login(cookies)

	def __repr__(self):
		return "<logged: {}, name: {}, username: {}, followers: {}, following: {}>".format(self.logged, self.name, self.username, self.total_followers, self.total_following)

	@property
	def logged(self):
		return self.__logged

	def login(self, cookies):
		self.session.set_cookies(cookies)
		html = self.session.get("https://instagram.com").text
		data = parsing.get_sharedData(html)
		if not "prefill_phone_number" in str(data):
			self.setup(data)
			self.__logged = True

	
	def setup(self, data):
		username = data["config"]["viewer"]["username"]
		self.data = self.session.get("https://instagram.com/{}?__a=1".format(username)).text
		self.sharedData = json.loads(self.data)
		self.name = self.sharedData["graphql"]["user"]["full_name"]
		self.username = self.sharedData["graphql"]["user"]["username"]
		self.id = self.sharedData["graphql"]["user"]["id"]
		self.profile_picture = self.sharedData["graphql"]["user"]["profile_pic_url_hd"]
		self.biography = self.sharedData["graphql"]["user"]["biography"]
		self.total_followers = self.sharedData["graphql"]["user"]["edge_followed_by"]["count"]
		self.total_following = self.sharedData["graphql"]["user"]["edge_follow"]["count"]

class People:
	def __init__(self, ses, username):
		self.ses = ses
		self.username = username
		self.setup()

	def __repr__(self):
		return "<name: {}, username: {}, followers: {}, following: {}>".format(self.name, self.username, self.total_followers, self.total_following)

	def setup(self):
		@check_login()
		@err_handler(KeyError, lambda: exception.PeopleNotFound(self.username))
		def inner():
			self.data = self.ses.session.get("https://instagram.com/" + self.username).text
			self.sharedData = parsing.get_sharedData(self.data)

			data = self.sharedData["entry_data"]["ProfilePage"][0]["graphql"]["user"]
			self.name = data["full_name"]
			self.username = data["username"]
			self.id = data["id"]
			self.profile_picture = data["profile_pic_url_hd"]
			self.biography = data["biography"]
			self.total_followers = data["edge_followed_by"]["count"]
			self.total_following = data["edge_follow"]["count"]
			return self.data

		inner()

	def follow(self):
		return action.follow_people(self.ses, self.username, idPeople = self.id)

	def unfollow(self):
		return action.unfollow_people(self.ses, self.username, idPeople = self.id)

	def follower(self):
		return dump.follower_people(self.ses, usernamePeople = self.username, idPeople = self.id)

	def following(self):
		return dump.following_people(self.ses, usernamePeople = self.username, idPeople = self.id)

	def post(self):
		return dump.post_people(self.ses, usernamePeople = self.username)
