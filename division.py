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

def fetch_divisions():
	doc = BeautifulSoup(urllib2.urlopen("http://www.oregonpremierleague.com/standingsandschedules/Fall2012/index_E.html","html5lib"));

	t = doc.find("table").select(".MainContent")
	doc2 = BeautifulSoup(str(t[0]),"html5lib")

	scheds = doc2.table.table.find_all("div","tg")
	for sched in scheds:
		title = sched.text.strip()
		url = sched.a.get('href').strip()
		gender = title.split()[0][0].strip()
		age = title.split()[0][1:].strip()
		opl_db.Division(gander = gender, age = age, title = title, url = url).put()


def get_all_divisions():
	t = opl_db.Division.all()

	rowarray_list = []
	for r in t.run():
		t = OrderedDict()
		t['id'] = r.key().id()
		t['gender'] = r.gender
		t['age'] = r.age
		t['title'] = r.title
		t['url'] = r.url
		t['created_date'] = r.created_date.strftime('%d-%b-%Y %H:%M:%S')
		t['last_updated_date'] = r.last_updated_date.strftime('%d-%b-%Y %H:%M:%S')
		#t['created_date'] = strftime(r.created_date, '%d-%b-%Y %H:%M:%S')
		#t['last_updated_date'] = strftime(r.last_updated_date, '%d-%b-%Y %H:%M:%S')
		rowarray_list.append(t)

	j = json.dumps(rowarray_list)
	return j

def delete_all_divisions():
	t = opl_db.Division.all()
	for r in t.run():
		r.delete()

class FetchDivisions(webapp2.RequestHandler):
	def get(self): 
		delete_all_divisions()
		fetch_divisions()
		##t = opl_db.Division.all()
		self.response.headers['Content-Type'] = 'text/html'
		self.response.write(get_all_divisions())
