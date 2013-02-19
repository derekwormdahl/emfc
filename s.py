from bs4 import *
from decimal import *
from datetime import datetime
from bs4 import NavigableString
from collections import OrderedDict
from google.appengine.api.taskqueue import Task

import re
import json
import collections
import urllib2
import webapp2
import opl_db
import logging
import urllib

def convert(data):
    if isinstance(data, unicode):
        return str(data)
    elif isinstance(data, collections.Mapping):
        return dict(map(convert, data.iteritems()))
    elif isinstance(data, collections.Iterable):
        return type(data)(map(convert, data))
    else:
        return data


##################################################################
## Store the games and results 
##################################################################
def store_schedule(url, league, division, gender, age):

	logging.debug(url)
	doc = BeautifulSoup(urllib2.urlopen(url,"html5lib"));

	## fix
	try:
		t = doc.find("table").find(id="tblListGames2").find("tbody")

		for sib in t.tr.next_siblings:
			if not isinstance(sib, NavigableString):
				gamedate = ''
				gametime = ''
				hometeam = ''
				awayteam = ''
				gamelocation = ''
				gamelocation_url = ''
				homescore = ''
				awayscore = ''
				
				if(sib.select(".GameHeader")):
					gdate = sib.previous_sibling.previous_sibling.text.strip()
					gdatef = datetime.strptime(gdate.strip(), '%a, %B %d, %Y')	
					gd = opl_db.GameDay.get_or_insert(key_name = gdate, gamedate = gdatef)
					gd.put()
					logging.debug('Found gameheader: '+gdate)

				logging.debug(t)
				t = sib.get("class")
				if isinstance(t,list):
					try: 
						idx = t.index('sch-main-gm')
						for td in sib.find_all('td'):
							try:
								if 'gamecode' in td.span['class']:
									gamecode = td.span.text.strip()
							except KeyError:
								pass
							except TypeError:
								pass
							try:
								if 'tim' in td['class']:
									gametime = td.text.strip()
							except KeyError:
								pass
							except TypeError:
								pass
							try:
								if 'schedtm1' in td['class']:
									hometeam = td.text.strip()
							except KeyError:
								pass
							except TypeError:
								pass
							try:
								if 'schedtm2' in td['class']:
									awayteam = td.text.strip()
							except KeyError:
								pass
							except TypeError:
								pass
							try:
								if 'tmcode' in td.span['class']:
									gamelocation = td.text.strip()
									gamelocation_url = td.span.a['href']
							except KeyError:
								pass
							except TypeError:
								pass
							try:
								if 'sch-main-sc' in td['class']:
									# if td.span.text.strip() != 'vs':
									if td.span:
										homescore = td.span.text.strip().split('-')[0]
										awayscore = td.span.text.strip().split('-')[1]
							except KeyError:
								pass
							except TypeError:
								pass

						logging.debug(division+ " awayscore ="+awayscore)
						opl_db.Game(gamecode = gamecode.strip(), gamedate = gdatef, gametime = gametime.strip(), hometeam = hometeam.strip(), awayteam = awayteam.strip(), homescore = homescore.strip(), awayscore = awayscore.strip(), league = league.strip(), division = division.strip(), gender = gender.strip(), age = age.strip()).put()
					except ValueError:
						pass

	except ValueError as e:
		logging.debug('---- ValueError')
		logging.debug(e)
		pass
						

##################################################################
## Fetch the schedule and results and return via json to user
##################################################################
def fetch_schedule(gd=None, league=None, division=None, gender=None, age=None):
	q = opl_db.Game.all()
	if gd:
		q.filter("gamedate = ", gd)
	if league:
		q.filter("league = ", league)
	if division:
		q.filter("division = ", division)
	if gender:
		q.filter("gender = ", gender)
	if age:
		q.filter("age = ", age)
	q.order("gamedate")

	games = OrderedDict()

	rowarray_list = []
	for r in q.run():
		t = OrderedDict()
		t['id'] = r.key().id()
		t['gamecode'] = r.gamecode
		t['gamedate'] = r.gamedate.strftime('%a, %B %d, %Y')
		t['gametime'] = r.gametime
		t['hometeam'] = r.hometeam
		t['awayteam'] = r.awayteam
		t['homescore'] = r.homescore
		t['awayscore'] = r.awayscore
		t['created_date'] = r.created_date.strftime('%d-%b-%Y %H:%M:%S')
		t['last_updated_date'] = r.last_updated_date.strftime('%d-%b-%Y %H:%M:%S')
		rowarray_list.append(t)

	games['games'] = rowarray_list
	
	j = json.dumps(games)
	return j

##################################################################
## Delete game days
##################################################################
def delete_gamedays():
	q = opl_db.GameDay.all()
	for r in q.run():
		r.delete()

##################################################################
## Delete game schedule results
##################################################################
def delete_schedules(league=None, division=None, gender=None, age=None):


	q1 = opl_db.Game.all()
	if league:
		q.filter("league = ", league)
	if division:
		q.filter("division = ", division)
	if gender:
		q.filter("gender =",gender)
	if age:
		q.filter("age = ", age)

	for r1 in q1.run():
		r1.delete()
	return 'Done'


##################################################################
## Store all game schedule results
## 	* for all the Division entries add a new Queue task
##        to call the /store-schedule-results handler.
##        this allows us to break up all the work of parsing
##        the page
##################################################################
def store_all_schedules(league=None, division=None, gender=None, age=None):
	
	q = opl_db.Division.all()
	if league:
		q.filter("league = ", league)
	if division:
		q.filter("division = ", division)
	if gender:
		q.filter("gender =",gender)
	if age:
		q.filter("age = ", age)

	for r in q.run():
		logging.debug('R:',r.league,'  ',r.gender)
		if len(r.sched_urls) > 0:
			for u in r.sched_urls:
				parms = { 'u' : u, 'l' : r.league, 'g' : r.gender, 'd' : r.division, 'a' : r.age }
				t = Task(method='GET', url='/store-schedule?'+urllib.urlencode(parms));
				t.add()
				##fetch_schedule_results(u, r.league, r.division, r.gender, r.age)
		else:
			##fetch_schedule_results(r.url, r.league, r.division, r.gender, r.age)
			parms = { 'u' : r.url, 'l' : r.league, 'g' : r.gender, 'd' : r.division, 'a' : r.age }
			t = Task(method='GET', url='/store-schedule?'+urllib.urlencode(parms));
			t.add()
	return 'done'
		

##################################################################
##################################################################
## Web handler endpoints
##################################################################
##################################################################


class THandler(webapp2.RequestHandler):	
	def get(self):
		self.response.headers['Content-Type'] = 'text/html'
		self.response.write(t())

class StoreAllSchedules(webapp2.RequestHandler):
	def get(self):
		league = self.request.get("l")
		division = self.request.get("d")
		gender = self.request.get("g")
		age = self.request.get("a")
		self.response.headers['Content-Type'] = 'text/html'
		self.response.write(store_all_schedules(league, division, gender, age))

class StoreSchedule(webapp2.RequestHandler):
	def get(self):
		url = self.request.get("u")
		league = self.request.get("l")
		division = self.request.get("d")
		gender = self.request.get("g")
		age = self.request.get("a")
		self.response.headers['Content-Type'] = 'text/html'
		self.response.write(store_schedule(url, league, division, gender, age))

class FetchSchedule(webapp2.RequestHandler):
	def get(self):
		dt = self.request.get("dt")
		league = self.request.get("l")
		division = self.request.get("d")
		gender = self.request.get("g")
		age = self.request.get("a")
		self.response.headers['Content-Type'] = 'text/html'
		self.response.write(fetch_schedule(dt, league, division, gender, age))

class DeleteSchedules(webapp2.RequestHandler):
	def get(self):
		league = self.request.get("l")
		division = self.request.get("d")
		gender = self.request.get("g")
		age = self.request.get("a")
		self.response.headers['Content-Type'] = 'text/html'
		self.response.write(delete_schedules(league, division, gender, age))

class DeleteGameDays(webapp2.RequestHandler):
	def get(self):
		self.response.headers['Content-Type'] = 'text/html'
		self.response.write(delete_gamedays())
		
