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
from division import StoreAllDivisionStandings
from division import StoreDivisionStandingsWorker
from location import FetchLocation
from league import StoreLeague
from league import FetchLeagues
from league import DeleteLeague
from division import FetchDistinctAgeGroups
from schedule import FetchSchedule
from schedule import StoreSchedule
from schedule import DeleteSchedules
from schedule import StoreAllSchedules

class MainPage(webapp2.RequestHandler):
    def get(self):
		self.response.headers['Content-Type'] = 'text/html'
		output = []
		output.append("<html><body>")
		output.append("<table>")
		output.append("<tr><td>Delete all schedules</td><td><a href='/delete-schedules'>Run</a>")
		output.append("<tr><td>Store all schedules</td><td><a href='/worker/store-all-schedules'>Run</a>")
		output.append("<tr><td>Store and delete all division standings</td><td><a href='/worker/store-all-division-standings'>Run</a>")
		output.append('</table>')
		output.append('</body></html>')
		
		self.response.write(''.join(output))

app = webapp2.WSGIApplication([
	(r'/', MainPage),
 	(r'/store-league', StoreLeague),
	(r'/fetch-leagues', FetchLeagues),
	(r'/delete-league', DeleteLeague),
	(r'/store-schedule', StoreSchedule),
	(r'/worker/store-all-schedules', StoreAllSchedules),
	(r'/fetch-schedule', FetchSchedule),
	(r'/delete-schedules', DeleteSchedules),
	(r'/store-division-standings', StoreDivisionStandings),
	(r'/store-divisions', StoreDivisions),
	(r'/worker/store-all-division-standings', StoreAllDivisionStandings),
	(r'/fetch-divisions', FetchDivisions),
	(r'/fetch-location', FetchLocation),
#	(r'/fetch-agegroups', FetchAgeGroups),
	(r'/fetch-distinct-agegroups', FetchDistinctAgeGroups),
	(r'/fetch-leagues', FetchLeagues),
	(r'/worker/std', StoreDivisionStandingsWorker)
],
debug=True)

