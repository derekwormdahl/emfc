#from bs4 import BeautifulSoup
from bs4 import *
import urllib2
from decimal import *
from datetime import datetime
from bs4 import NavigableString
import collections
from collections import OrderedDict
import json
import webapp2
import opl_db
import re
import logging

def convert(data):
    if isinstance(data, unicode):
        return str(data)
    elif isinstance(data, collections.Mapping):
        return dict(map(convert, data.iteritems()))
    elif isinstance(data, collections.Iterable):
        return type(data)(map(convert, data))
    else:
        return data

def t():

	doc = BeautifulSoup(urllib2.urlopen("http://www.oregonpremierleague.com/schedules/Fall2012/47896539.20129.html","html5lib"));

	t = doc.find("table").find(id="tblListGames2").find("tbody")
	
	#return t.tr

	# if 'RowHeader' in t.tr.td['class']:
	try: 
		#if 'GameHeader' in t.tr.td['class']:	
		t2 = t.tr.find_all('td',{'class': re.compile(r'/GameHeader/')})
		return t2
			#t1 = t.tr.td.find_previous_sibling('tr')
			#gd = opl_db.GameDay(gamedate = t.tr.td.text.strip())
			#gd.put()
			### print "GameDay: ",t.tr.td.text.strip()
	except KeyError:
		pass
 

def fetch_schedule_results(url, league, agegroup, gender, age):

	#doc = BeautifulSoup(urllib2.urlopen("http://www.oregonpremierleague.com/schedules/Fall2012/47896539.20129.html","html5lib"));
	logging.debug(url)
	doc = BeautifulSoup(urllib2.urlopen(url,"html5lib"));

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
				gd = opl_db.GameDay.get_or_insert(key_name = gdate, gamedate = gdate)
				#gd = opl_db.GameDay(key_name = gdate, gamedate = gdate)
				gd.put()

			##t = convert(sib.get("class",''))
			t = sib.get("class")
			if isinstance(t,list):
				if(t.index('sch-main-gm') > 0):
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

					logging.debug(agegroup + " awayscore ="+awayscore)
					opl_db.Game(gamecode = gamecode.strip(), gamedate = gd.gamedate.strip(), gametime = gametime.strip(), hometeam = hometeam.strip(), awayteam = awayteam.strip(), homescore = homescore.strip(), awayscore = awayscore.strip(), league = league.strip(), agegroup = agegroup.strip(), gender = gender.strip(), age = age.strip()).put()
						

def fetch_all_schedule_results(gd=None, league=None, agegroup=None, gender=None, age=None):
	q = opl_db.Game.all()
	if gd:
		logging.debug("gamedate ="+gd)
		q.filter("gamedate = ", gd)
	if league:
		q.filter("league = ", league)
	if agegroup:
		q.filter("agegroup = ", agegroup)
	if gender:
		q.filter("gender = ", gender)
	if age:
		q.filter("age = ", age)

	games = OrderedDict()

	rowarray_list = []
	for r in q.run():
		t = OrderedDict()
		t['id'] = r.key().id()
		t['gamecode'] = r.gamecode
		t['gamedate'] = r.gamedate
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

def delete_all_schedule_results():
	t = opl_db.GameDay.all()
	for r in t.run():
		r.delete()

	t1 = opl_db.Game.all()
	for r1 in t1.run():
		r1.delete()
	return 'Done'

def store_game_schedule(gender):
	
	q = opl_db.AgeGroup.all()
	if gender:
		q.filter("gender =",gender)

	for r in q.run():
		fetch_schedule_results(r.url, r.league, r.name, r.gender, r.age)
	return 'done'
		


class THandler(webapp2.RequestHandler):	
	def get(self):
		self.response.headers['Content-Type'] = 'text/html'
		self.response.write(t())

class DeleteGameSchedule(webapp2.RequestHandler):
	def get(self):
		self.response.headers['Content-Type'] = 'text/html'
		self.response.write(delete_all_schedule_results())

class StoreGameSchedule(webapp2.RequestHandler):
	def get(self):
		gender = self.request.get("g")
		self.response.headers['Content-Type'] = 'text/html'
		self.response.write(store_game_schedule(gender))
		

class FetchGameSchedule(webapp2.RequestHandler):
	def get(self):
		dt = self.request.get("d")
		league = self.request.get("l")
		agegroup = self.request.get("ag")
		gender = self.request.get("g")
		age = self.request.get("a")
		self.response.headers['Content-Type'] = 'text/html'
		self.response.write(fetch_all_schedule_results(dt, l, ag, g, a))

		
