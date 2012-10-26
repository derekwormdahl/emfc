import datetime
from google.appengine.ext import db
from google.appengine.api import users

class League(db.Model):
  	name = db.StringProperty()
  	url = db.StringProperty()
	created_date = db.DateTimeProperty(auto_now_add = True)
	last_updated_date = db.DateTimeProperty(auto_now = True)

class AgeGroup(db.Model):
  	name = db.StringProperty()
	agegroup = db.StringProperty()
	gender = db.StringProperty()
	age = db.StringProperty()
	url = db.StringProperty()
	#league = db.ReferenceProperty(League, collection_name='leagues')
	league = db.StringProperty()
	created_date = db.DateTimeProperty(auto_now_add = True)
	last_updated_date = db.DateTimeProperty(auto_now = True)

class GameDay(db.Model):
  	gamedate = db.StringProperty()
	#game = db.ReferenceProperty(Game, collection_name='games')
	created_date = db.DateTimeProperty(auto_now_add = True)
	last_updated_date = db.DateTimeProperty(auto_now = True)

class Game(db.Model):
  	gamecode = db.StringProperty()
	league = db.StringProperty()
  	division = db.StringProperty()
	gender = db.StringProperty()
	age = db.StringProperty()
	url = db.StringProperty()
	gamedate = db.StringProperty()
  	gametime = db.StringProperty()
  	hometeam = db.StringProperty()
  	awayteam = db.StringProperty()
  	homescore = db.StringProperty()
	awayscore = db.StringProperty()
	created_date = db.DateTimeProperty(auto_now_add = True)
	last_updated_date = db.DateTimeProperty(auto_now = True)

class Division(db.Model):
	league = db.StringProperty()
	division = db.StringProperty()
	agegroup = db.StringProperty()
	gender = db.StringProperty()
	age = db.StringProperty()
	url = db.StringProperty()
  	created_date = db.DateTimeProperty(auto_now_add = True)
  	last_updated_date = db.DateTimeProperty(auto_now = True)


class Location(db.Model):
	name = db.StringProperty()
	map_url = db.StringProperty()
	formatted_address = db.StringProperty()
	street_number = db.StringProperty()
	address = db.StringProperty()
	city = db.StringProperty()
	state = db.StringProperty()
	country = db.StringProperty()
	latitude = db.StringProperty()
	longitude = db.StringProperty()
	created_date = db.DateTimeProperty(auto_now_add = True)
	last_updated_date = db.DateTimeProperty(auto_now = True)
