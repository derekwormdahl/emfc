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
import re
import logging

def store_all_divisions():
	t = opl_db.League.all()
	for r in t.run():
		store_divisions(r.name)

	return 'Done'
	
def store_division_sched_urls(url):
	doc = BeautifulSoup(urllib2.urlopen(url,"html5lib"));
	
	ret_urls = []

	sched_urls = doc.find_all('a', href=re.compile("\/schedules\/.*[0-9]*\.[0-9]*\.html"))
	for u in sched_urls:
	        ret_urls.append("http://www.oregonpremierleague.com"+u['href'])
	return ret_urls
	
	
def store_divisions(l):
	doc = BeautifulSoup(urllib2.urlopen("http://www.oregonpremierleague.com/standingsandschedules/Fall2012/index_E.html","html5lib"));

	t = doc.find("table").select(".MainContent")
	doc2 = BeautifulSoup(str(t[0]),"html5lib")
	
	logging.debug('in store_divisions')

	#scheds = doc2.table.table.find_all("div","tg")
	scheds = doc2.find_all("div","tg")
	logging.debug(scheds)
	for sched in scheds:
		logging.debug('league'+l)
		league = l
		division = sched.text.strip()
		url = "http://www.oregonpremierleague.com"+sched.a.get('href').strip()
		sched_urls = store_division_sched_urls(url)
		agegroup = division.split()[0].strip()
		gender = agegroup[:1].strip()
		age = agegroup[1:].strip()
		opl_db.Division(league = league, agegroup = agegroup, gender = gender, age = age, division = division, url = url, sched_urls = sched_urls).put()


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

def delete_all_divisions():
	t = opl_db.Division.all()
	for r in t.run():
		r.delete()

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
	
def store_division_standings():
	doc = BeautifulSoup(urllib2.urlopen("http://www.oregonpremierleague.com/standingsandschedules/Fall2012/index_E.html","html5lib"));

	t = doc.find("tr", "tg hd")  ##.select(".MainContent")
	doc2 = BeautifulSoup(str(t[0]),"html5lib")
		
	logging.debug('in store_divisions')
	
	#scheds = doc2.table.table.find_all("div","tg")
	scheds = doc2.find_all("div","tg")
	logging.debug(scheds)
	for sched in scheds:
		logging.debug('league'+l)
		league = l
		division = sched.text.strip()
		url = "http://www.oregonpremierleague.com"+sched.a.get('href').strip()
		sched_urls = store_division_sched_urls(url)
		agegroup = division.split()[0].strip()
		gender = agegroup[:1].strip()
		age = agegroup[1:].strip()
		opl_db.Division(league = league, agegroup = agegroup, gender = gender, age = age, division = division, url = url, sched_urls = sched_urls).put()


	

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
