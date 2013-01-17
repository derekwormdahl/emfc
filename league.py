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

##################################################################
## Store the league
##################################################################
def store_league(name, url):
	opl_db.League(name = name, url = url).put()

##################################################################
## Delete leagues
##################################################################
def delete_league(league):	
	q = opl_db.League.all()
	if league:
		q.filter('name = ', league)
	
	for r in q.run():
		r.delete()

##################################################################
## Fetch the league and return as json
##################################################################
def fetch_leagues():
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
	

##################################################################
##################################################################
## Web handler endpoints
##################################################################
##################################################################

class StoreLeague(webapp2.RequestHandler):
	def get(self): 
		name = self.request.get('n')
		url = self.request.get('u')
		self.response.headers['Content-Type'] = 'text/html'
		self.response.write(store_league(name, url))

		
class FetchLeagues(webapp2.RequestHandler):
	def get(self): 
		self.response.headers['Content-Type'] = 'text/html'
		self.response.write(fetch_leagues())


class DeleteLeague(webapp2.RequestHandler):
	def get(self): 
		league = self.request.get('l')
		self.response.headers['Content-Type'] = 'text/html'
		self.response.write(delete_league(league))
