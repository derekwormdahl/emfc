#!/usr/bin/env python
#

import webapp2
import urllib2
import collections
import division
import logging
import opl_db

from bs4 import *
from bs4 import NavigableString
from google.appengine.api import users
from division import StoreDivisions
from division import FetchDivisions
from division import StoreDivisionStandings
from opl import FetchSchedule
from location import FetchLocation
from league import StoreLeague
from league import FetchLeagues
from division import FetchDistinctAgeGroups
from opl import StoreGameSchedule
from opl import StoreSchedule
from opl import DeleteSchedules
from opl import StoreAllSchedules

class MainPage(webapp2.RequestHandler):
    def get(self):
		self.response.headers['Content-Type'] = 'text/html'
		self.response.write("home")

app = webapp2.WSGIApplication([
	(r'/', MainPage),
 	(r'/store-league', StoreLeague),
	(r'/fetch-leagues', FetchLeagues),
	(r'/store-schedule', StoreSchedule),
	(r'/worker/store-all-schedules', StoreAllSchedules),
	(r'/fetch-schedule', FetchSchedule),
	(r'/delete-schedules', DeleteSchedules),
	(r'/store-division-standings', StoreDivisionStandings),
	(r'/store-divisions', StoreDivisions),
	(r'/fetch-divisions', FetchDivisions),
	(r'/fetch-location', FetchLocation),
#	(r'/fetch-agegroups', FetchAgeGroups),
	(r'/fetch-distinct-agegroups', FetchDistinctAgeGroups),
],
debug=True)

