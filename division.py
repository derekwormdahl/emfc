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

def store_all_divisions():
	t = opl_db.League.all()
	for r in t.run():
		store_divisions(r.name)

	return 'Done'

def store_divisions(l):
	doc = BeautifulSoup(urllib2.urlopen("http://www.oregonpremierleague.com/standingsandschedules/Fall2012/index_E.html","html5lib"));

	t = doc.find("table").select(".MainContent")
	doc2 = BeautifulSoup(str(t[0]),"html5lib")

	scheds = doc2.table.table.find_all("div","tg")
	for sched in scheds:
		league = l
		division = sched.text.strip()
		url = sched.a.get('href').strip()
		agegroup = division.split()[0].strip()
		gender = agegroup[:1].strip()
		age = agegroup[1:].strip()
		#gender = division.split()[0][:1].strip()
		#age = division.split()[0][1:].strip()
		opl_db.Division(league = league, agegroup = agegroup, gender = gender, age = age, division = division, url = url).put()


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
