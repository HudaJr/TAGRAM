import re, json
from . import dump
from . import action

class Post:
	def __init__(self, ses, data):
		try:
			if type(data) == str:
				data = json.loads(data)

			self.ses = ses
			self.data = data["node"]

			if self.data.get("id"):
				self.id = self.data["id"]
			else:
				self.id = ""
		except:
			self.id = ""

	def __repr__(self):
		return self.id

	def like(self):
		self.action.like_post(ses, self.id)

	def unlike(self):
		self.action.unlike_post(ses, self.id)

class People:
	def __init__(self, ses, data):
		if type(data) == str:
			data = json.loads(data)

		self.ses = ses
		self.data = data["node"]
		self.username = self.data["username"]
		self.id = self.data["id"]
		self.name = self.data["full_name"]
		self.profile_picture = self.data["profile_pic_url"]

	def __repr__(self):
		return self.username

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

class Output:
	def __init__(self, items = None, data = None, idPeople = None, next = None):
		self.items = items
		self.next = next.replace("==", "%3D") if next else None
		self.data = data
		self.idPeople = idPeople
		self.isNext = bool(self.next)

	def __repr__(self):
		return "<total_items: {}, next: {}>".format(len(self.items), self.next)

