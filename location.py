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

def fetch_location(url):
	baseurl = "http://maps.googleapis.com/maps/api/geocode/json?address="
	sensor = "&sensor=false"
	result = json.load(urllib2.urlopen(baseurl + url + sensor))
	#j = result.read()
	lat = result['results'][0]['geometry']['location']['lat']
	long = result['results'][0]['geometry']['location']['lng']
	street_number = result['results'][0]['address_components'][0]['short_name']
	address = result['results'][0]['address_components'][1]['short_name']
	city = result['results'][0]['address_components'][2]['short_name']
	county = result['results'][0]['address_components'][3]['short_name']
	state = result['results'][0]['address_components'][4]['short_name']
	country = result['results'][0]['address_components'][5]['short_name']
	zip = result['results'][0]['address_components'][6]['short_name']

	return street_number + "  " + address + "  " + city + "  " + county + "  " + state + "  " + country + "  " + zip
	
class LocationHandler(webapp2.RequestHandler):
	def get(self): 
		self.response.headers['Content-Type'] = 'text/html'
		self.response.write(fetch_location('+5105+SE+302nd+Avenue+Gresham'))
