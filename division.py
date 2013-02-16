import urllib2
import collections
import opl_db
import json
import webapp2
import re
import logging
import string
import urllib

from bs4 import *
from bs4 import NavigableString
from collections import OrderedDict
from time import strftime
from google.appengine.api import taskqueue
from google.appengine.api.taskqueue import Task


##################################################################
## Store the divisional standings
##################################################################
def store_all_division_standings(league, division, gender, age, agegroup):
	q = opl_db.Division.all()
	if league:
		q.filter("league =", league)
	if division:
		q.filter("division = ", division)
	if gender:
		q.filter("gender =", gender)
	if age:
		q.filter("age =", age)	
	if agegroup: 
		q.filter("agegroup = ", agegroup)
		
	for r in q.run():
		parms = { 'l' : r.league, 'u' : r.url, 'a' : r.age, 'ag' : r.agegroup, 'g' : r.gender, 'd' : r.division}
		url = '/store-division-standings?'+urllib.urlencode(parms)
		logging.debug('URL:'+url)
		t = Task(payload=None, method='GET', url=url)
		t.add()
	return 'Done'

##################################################################
## Store all the divisions
##################################################################
def store_all_divisions():
	t = opl_db.League.all()
	for r in t.run():
		store_divisions(r.name, r.url)

	return 'Done'
	

##################################################################
## Store the division schedule urls
##################################################################
def store_division_sched_urls(url):
	doc = BeautifulSoup(urllib2.urlopen(url,"html5lib"));
	
	ret_urls = []

	sched_urls = doc.find_all('a', href=re.compile("\/schedules\/.*[0-9]*\.[0-9]*\.html"))
	for u in sched_urls:
	        ret_urls.append("http://www.oregonpremierleague.com"+u['href'])
	
	if not ret_urls:
		ret_urls.append(url)
		
	return ret_urls
	

##################################################################
## Store the divisions
##################################################################
def store_divisions(l, url):
	doc = BeautifulSoup(urllib2.urlopen(url,"html5lib"));

	t = doc.find("table").select(".MainContent")
	doc2 = BeautifulSoup(str(t[0]),"html5lib")
	
	logging.debug('in store_divisions')

	scheds = doc2.find_all("div","tg")
	logging.debug(scheds)

	for g in ['Boys','Girls']:
		p = doc2.find_all('div',text=re.compile(g))
		for ps in p:	
			gender = ps.text.strip()
			enclosing = ps.find_previous('td')
			u = enclosing.find_all('div',text=re.compile('Under'))
			for us in u:
				agegroup = gender[0:1]+'U'+us.text.strip()[6:8]
				tms = us.find_next_sibling('table').find_all('div','tg')
				for tm in tms:
					logging.debug('league'+l)
					league = l
					division = tm.text.strip()
					url = "http://www.oregonpremierleague.com"+tm.a.get('href').strip()
					sched_urls = store_division_sched_urls(url)
					age = agegroup[1:].strip()
					opl_db.Division(league = league, agegroup = agegroup, gender = gender, age = age, division = division, url = url, sched_urls = sched_urls).put()


##################################################################
## Fetch the divisions
##################################################################
def fetch_divisions(league, agegroup):
	t = opl_db.Division.all()

	if league:
		t.filter("league =", league)
	if agegroup: 
		t.filter("agegroup =", agegroup)

	rowarray_list = []
	for r in t.run():
		t = OrderedDict()
		t['id'] = r.key().id()
		t['league'] = r.league
		t['division'] = r.division
		t['agegroup'] = r.agegroup
		t['gender'] = r.gender
		t['age'] = r.age
		t['url'] = r.url
		t['created_date'] = r.created_date.strftime('%d-%b-%Y %H:%M:%S')
		t['last_updated_date'] = r.last_updated_date.strftime('%d-%b-%Y %H:%M:%S')
		rowarray_list.append(t)

	j = json.dumps(rowarray_list)
	return j

##################################################################
## Delete divisions
##################################################################
def delete_all_divisions():
	t = opl_db.Division.all()
	for r in t.run():
		r.delete()


##################################################################
## Fetch the distinct list of agegroups
##################################################################
def fetch_distinct_agegroups(league=None, gender=None, age=None):
	q = opl_db.Division.all()
	if league:
		q.filter("league =", league)
	if gender:
		q.filter("gender =", gender)
	if age:
		q.filter("age =", age)		
		agegroups = OrderedDict()
		
	ur = []
	for obj in q:
		if obj.agegroup not in ur:
			ur.append(obj.agegroup)		

	ur.sort()

	agegroups = OrderedDict()

	rowarray_list = []
	for r in ur:
		t = OrderedDict()
		t['agegroup'] = r
		t['gender'] = r[0:1]
		t['age'] = r[1:]
		rowarray_list.append(t)

	agegroups['agegroups'] = rowarray_list
			
	j = json.dumps(agegroups)
	return j
	

##################################################################
## Delete divisional standings
##################################################################
def delete_division_standings():
	t = opl_db.DivisionStandings.all()
	for r in t.run():
		r.delete()


##################################################################
## Store the divisional standings
##################################################################
def store_division_standings(league, url, age, agegroup, gender, division):
	
	doc = BeautifulSoup(urllib2.urlopen(url, "html5lib"));

	fullscore = False
	
	teamcode = ''
	teamname = ''
	pts = ''
	gp = ''
	w = ''
	l = ''
	t = ''
	gf = ''
	ga = ''
	gd = ''

	if doc.find("td", text=re.compile('Pts')):
		fullscore = True

	t = doc.find("td",text=re.compile('GP'))

 	tbl = t.find_parent("tr").find_parent("table")
	trs = tbl.find_all("tr", "tms")
	for tr in trs:
		teamcode = ''
		teamname = ''
		pts = ''
		gp = ''
		w = ''
		l = ''
		t = ''
		gf = ''
		ga = ''
		gd = ''
		tds = tr.find_all("td")
		if(fullscore):
			teamname = ''.join(unicode(tds[0].a.text.strip()).splitlines())
			pts = tds[1].text.strip()
			gp = tds[2].text.strip()
			w = tds[3].text.strip()
			l = tds[4].text.strip()
			t = tds[5].text.strip()
			gf = tds[6].text.strip()
			ga = tds[7].text.strip()
			gd = tds[8].text.strip()
		else:
			teamname = ''.join(unicode(tds[0].a.text.strip()).splitlines())
			gp = tds[1].text.strip()
			w = tds[2].text.strip()
			l = tds[3].text.strip()
			t = tds[4].text.strip()
		
		opl_db.DivisionStandings(league = league.strip(), division = division.strip(), agegroup = agegroup.strip(), gender = gender.strip(), age = age.strip(), teamname = teamname.strip(), teamcode = teamcode.strip(), pts = pts.strip(), gp = gp.strip(), w = w.strip(), l = l.strip(), t = t.strip(), gf = gf.strip(), ga = ga.strip(), gd = gd.strip()).put()


##################################################################
##################################################################
## Web handler endpoints
##################################################################
##################################################################
class StoreDivisionStandings(webapp2.RequestHandler):
	def get(self): 
		league = self.request.get("l")
		division = self.request.get("d")
		gender = self.request.get("g")
		age = self.request.get("a")
		agegroup = self.request.get('ag')
		url = self.request.get('u')
		self.response.headers['Content-Type'] = 'text/html'
		self.response.write(store_division_standings(league, url, age, agegroup, gender, division))

class StoreAllDivisionStandings(webapp2.RequestHandler):
	def get(self):
		league = self.request.get("l")
		division = self.request.get("d")
		gender = self.request.get("g")
		age = self.request.get("a")
		agegroup = self.request.get('ag')
		delete_division_standings()
		self.response.headers['Content-Type'] = 'text/html'
		self.response.write(store_all_division_standings(league, division, gender, age, agegroup))

class StoreDivisionStandingsWorker(webapp2.RequestHandler):
	def post(self):
		delete_division_standings()
		store_all_division_standings('','','','','')
		self.response.write("Done")

class StoreDivisions(webapp2.RequestHandler):
	def get(self): 
		delete_all_divisions()
		self.response.headers['Content-Type'] = 'text/html'
		self.response.write(store_all_divisions())

class FetchDivisions(webapp2.RequestHandler):
	def get(self): 
		league = self.request.get("l")
		agegroup = self.request.get("ag")
		self.response.headers['Content-Type'] = 'text/html'
		self.response.write(fetch_divisions(league, agegroup))
		
class FetchDistinctAgeGroups(webapp2.RequestHandler):
	def get(self): 
		league = self.request.get("l")
		gender = self.request.get("g")
		age = self.request.get("a")
		self.response.headers['Content-Type'] = 'text/html'
		self.response.write(fetch_distinct_agegroups(league, gender, age))
