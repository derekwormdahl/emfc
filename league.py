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

def store_league(name, url):
	#f2012 = opl_db.League(name="Fall 2012", url="http://www.oregonpremierleague.com/standingsandschedules/Fall2012/index_E.html")
	opl_db.League(name = name, url = url).put()

def delete_all_leagues():	
	t = opl_db.League.all()
	for r in t.run():
		r.delete()

def ld(msg):
	logging.debug(msg)
	


def fetch_leagues(gender, age):
	q = opl_db.League.all()
	leagues = OrderedDict()

	rowarray_list = []
	for r in q.run():
		t = OrderedDict()
		t['name'] = r.name
		t['url'] = r.url
		rowarray_list.append(t)

	leagues['leagues'] = rowarray_list
			
	j = json.dumps(leagues)
	return j		
	
class StoreLeague(webapp2.RequestHandler):
	def get(self): 
		name = self.request.get('n')
		url = self.request.get('u')
		self.response.headers['Content-Type'] = 'text/html'
		self.response.write(store_league(name, url))

		
class FetchLeagues(webapp2.RequestHandler):
	def get(self): 
		gender = self.request.get("g")
		age = self.request.get("a")
		self.response.headers['Content-Type'] = 'text/html'
		self.response.write(fetch_leagues(gender, age))


