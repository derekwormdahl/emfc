import datetime
from google.appengine.ext import db
from google.appengine.api import users

class GameDay(db.Model):
  	gamedate = db.StringProperty()
  	created_date = db.DateProperty(default = datetime.datetime.now().date())
  	last_updated_date = db.DateProperty(default = datetime.datetime.now().date())

class Game(db.Model):
  	gamecode = db.StringProperty()
  	gameday_id = db.IntegerProperty()
  	gametime = db.StringProperty()
  	hometeam = db.StringProperty()
  	awayteam = db.StringProperty()
  	homescore = db.IntegerProperty()
	awayscore = db.IntegerProperty()
  	created_date = db.DateProperty(default = datetime.datetime.now().date())
  	last_updated_date = db.DateProperty(default = datetime.datetime.now().date())

class Division(db.Model):
	gender = db.StringProperty()
	age = db.StringProperty()
	title = db.StringProperty()
	url = db.StringProperty()
  	created_date = db.DateTimeProperty(auto_now_add = True)
  	last_updated_date = db.DateTimeProperty(auto_now = True)


