#from bs4 import BeautifulSoup
from bs4 import *
import urllib2
from bs4 import NavigableString
import collections
import opl_db
import json
from collections import OrderedDict
from time import strftime
import webapp2
from google.appengine.ext import db
import logging

def store_leagues():
	f2012 = opl_db.League(name="Fall 2012")
	f2012.put()

	opl_db.AgeGroup(name="BU11 Timbers NPL Premier Division",gender="B",age="U11",url="http://www.oregonpremierleague.com/schedules/Fall2012/47896535.html", league="Fall 2012").put()
	opl_db.AgeGroup(name="BU11 First Division",gender="B",age="U11",url="http://www.oregonpremierleague.com/schedules/Fall2012/47896543.html", league="Fall 2012").put()
	opl_db.AgeGroup(name="BU11 Second Division",gender="B",age="U11",url="http://www.oregonpremierleague.com/schedules/Fall2012/47896548.html", league="Fall 2012").put()
	opl_db.AgeGroup(name="BU11 Third Division",gender="B",age="U11",url="http://www.oregonpremierleague.com/schedules/Fall2012/51445521.html", league="Fall 2012").put()
	
	opl_db.AgeGroup(name="BU12 Timbers NPL Premier Division",gender="B",age="U12",url="http://www.oregonpremierleague.com/schedules/Fall2012/47896544.html", league="Fall 2012").put()
	opl_db.AgeGroup(name="BU12 First Division",gender="B",age="U12",url="http://www.oregonpremierleague.com/schedules/Fall2012/47896541.html", league="Fall 2012").put()
	opl_db.AgeGroup(name="BU12 Second Division",gender="B",age="U12",url="http://www.oregonpremierleague.com/schedules/Fall2012/47896547.html", league="Fall 2012").put()
	opl_db.AgeGroup(name="BU12 Third Division",gender="B",age="U12",url="http://www.oregonpremierleague.com/schedules/Fall2012/47896558.html", league="Fall 2012").put()
	opl_db.AgeGroup(name="BU12 Fourth Division",gender="B",age="U12",url="http://www.oregonpremierleague.com/schedules/Fall2012/51445522.html", league="Fall 2012").put()
	
	opl_db.AgeGroup(name="BU13 Timbers NPL Premier Division",gender="B",age="U13",url="http://www.oregonpremierleague.com/schedules/Fall2012/47896536.html", league="Fall 2012").put()
	opl_db.AgeGroup(name="BU13 First Division",gender="B",age="U13",url="http://www.oregonpremierleague.com/schedules/Fall2012/47896552.html", league="Fall 2012").put()
	opl_db.AgeGroup(name="BU13 Second Division",gender="B",age="U13",url="http://www.oregonpremierleague.com/schedules/Fall2012/47896546.html", league="Fall 2012").put()
	opl_db.AgeGroup(name="BU13 Third Division",gender="B",age="U13",url="http://www.oregonpremierleague.com/schedules/Fall2012/51445523.html", league="Fall 2012").put()

	opl_db.AgeGroup(name="BU14 Timbers NPL Premier Division",gender="B",age="U14",url="http://www.oregonpremierleague.com/schedules/Fall2012/47896537.html", league="Fall 2012").put()
	opl_db.AgeGroup(name="BU14 First Division",gender="B",age="U14",url="http://www.oregonpremierleague.com/schedules/Fall2012/47896550.html", league="Fall 2012").put()
	opl_db.AgeGroup(name="BU14 Second Division",gender="B",age="U14",url="http://www.oregonpremierleague.com/schedules/Fall2012/47896554.html", league="Fall 2012").put()
	opl_db.AgeGroup(name="BU14 Third Division",gender="B",age="U14",url="http://www.oregonpremierleague.com/schedules/Fall2012/47896534.html", league="Fall 2012").put()

	opl_db.AgeGroup(name="GU11 Timbers NPL Premier Division",gender="G",age="U11",url="http://www.oregonpremierleague.com/schedules/Fall2012/47896534.html", league="Fall 2012").put()
	opl_db.AgeGroup(name="GU11 First Division",gender="G",age="U11",url="http://www.oregonpremierleague.com/schedules/Fall2012/47896542.html", league="Fall 2012").put()
	opl_db.AgeGroup(name="GU11 Second Division",gender="G",age="U11",url="http://www.oregonpremierleague.com/schedules/Fall2012/47896545.html", league="Fall 2012").put()
	opl_db.AgeGroup(name="GU11 Third Division",gender="G",age="U11",url="http://www.oregonpremierleague.com/schedules/Fall2012/51449135.html", league="Fall 2012").put()
	opl_db.AgeGroup(name="GU11 Fourth Division",gender="G",age="U11",url="http://www.oregonpremierleague.com/schedules/Fall2012/5144136.html", league="Fall 2012").put()

	opl_db.AgeGroup(name="GU12 Timbers NPL Premier Division",gender="G",age="U12",url="http://www.oregonpremierleague.com/schedules/Fall2012/47896538.html", league="Fall 2012").put()
	opl_db.AgeGroup(name="GU12 First Division",gender="G",age="U12",url="http://www.oregonpremierleague.com/schedules/Fall2012/47896553.html", league="Fall 2012").put()
	opl_db.AgeGroup(name="GU12 Second Division",gender="G",age="U12",url="http://www.oregonpremierleague.com/schedules/Fall2012/47896555.html", league="Fall 2012").put()
	opl_db.AgeGroup(name="GU12 Third Division",gender="G",age="U12",url="http://www.oregonpremierleague.com/schedules/Fall2012/47896560.html", league="Fall 2012").put()

	opl_db.AgeGroup(name="GU13 Timbers NPL Premier Division",gender="G",age="U13",url="http://www.oregonpremierleague.com/schedules/Fall2012/47896539.html", league="Fall 2012").put()
	opl_db.AgeGroup(name="GU13 First Division",gender="G",age="U13",url="http://www.oregonpremierleague.com/schedules/Fall2012/47896551.html", league="Fall 2012").put()
	opl_db.AgeGroup(name="GU13 Second Division",gender="G",age="U13",url="http://www.oregonpremierleague.com/schedules/Fall2012/47896556.html", league="Fall 2012").put()
	opl_db.AgeGroup(name="GU13 Third Division",gender="G",age="U13",url="http://www.oregonpremierleague.com/schedules/Fall2012/47896561.html", league="Fall 2012").put()
	opl_db.AgeGroup(name="GU13 Fourth Division",gender="G",age="U13",url="http://www.oregonpremierleague.com/schedules/Fall2012/51449141.html", league="Fall 2012").put()

	opl_db.AgeGroup(name="GU14 Timbers NPL Premier Division",gender="G",age="U14",url="http://www.oregonpremierleague.com/schedules/Fall2012/47896540.html", league="Fall 2012").put()
	opl_db.AgeGroup(name="GU14 First Division",gender="G",age="U14",url="http://www.oregonpremierleague.com/schedules/Fall2012/47896549.html", league="Fall 2012").put()
	opl_db.AgeGroup(name="GU14 Second Division",gender="G",age="U14",url="http://www.oregonpremierleague.com/schedules/Fall2012/47896557.html", league="Fall 2012").put()
	opl_db.AgeGroup(name="GU14 Third Division",gender="G",age="U14",url="http://www.oregonpremierleague.com/schedules/Fall2012/47896562.html", league="Fall 2012").put()
	

def delete_all_leagues():	
	t = opl_db.League.all()
	for r in t.run():
		r.delete()

def delete_all_agegroups():	
	t = opl_db.AgeGroup.all()
	for r in t.run():
		r.delete()		

def ld(msg):
	logging.debug(msg)
		

def get_agegroups(league=None, gender=None, age=None):

	ld("in get agegroups")
	q = opl_db.AgeGroup.all()
	if league:
		ld("league is not none: "+league)
		q.filter("league =", league)
	if gender:
		ld("gender is not none: "+gender)
		q.filter("gender =", gender)
	if age:
		ld("age is not none: "+age)
		q.filter("age =", age)
	

	agegroups = OrderedDict()

	rowarray_list = []
	for r in q.run():
		t = OrderedDict()
		t['id'] = r.key().id()
		t['name'] = r.name
		t['league'] = r.league
		t['gender'] = r.gender
		t['age'] = r.age
		t['url'] = r.url
		t['created_date'] = r.created_date.strftime('%d-%b-%Y %H:%M:%S')
		t['last_updated_date'] = r.last_updated_date.strftime('%d-%b-%Y %H:%M:%S')
		rowarray_list.append(t)

	agegroups['agegroups'] = rowarray_list
			
	j = json.dumps(agegroups)
	return j		
		

class LeagueHandler(webapp2.RequestHandler):
	def get(self): 
		delete_all_leagues()
		delete_all_agegroups()
		self.response.headers['Content-Type'] = 'text/html'
		self.response.write(store_leagues())
		
class GetAgeGroups(webapp2.RequestHandler):
	def get(self): 
		league = self.request.get("l")
		gender = self.request.get("g")
		age = self.request.get("a")
		self.response.headers['Content-Type'] = 'text/html'
		self.response.write(get_agegroups(league, gender, age))
