#!/usr/bin/env python
#
# Copyright 2007 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
import webapp2
from bs4 import *
import urllib2
from bs4 import NavigableString
import collections
import division
from google.appengine.api import users
import opl_db
from division import StoreDivisions
from division import FetchDivisions
from division import StoreDivisionStandings
from opl import FetchGameSchedule
from location import FetchLocation
from league import StoreLeague
from league import FetchLeagues
# from league import FetchAgeGroups
from division import FetchDistinctAgeGroups
from opl import StoreGameSchedule
from opl import StoreSchedule
from opl import DeleteSchedules
from opl import StoreAllSchedules
import logging

class MainPage(webapp2.RequestHandler):
    def get(self):
		self.response.headers['Content-Type'] = 'text/html'
		self.response.write("testing")

app = webapp2.WSGIApplication([
	(r'/', MainPage),
	##(r'/store-schedule', StoreGameSchedule),
 	(r'/store-league', StoreLeague),
	(r'/fetch-leagues', FetchLeagues),
	(r'/store-schedule', StoreSchedule),
	(r'/worker/store-all-schedules', StoreAllSchedules),
	(r'/fetch-schedule', FetchGameSchedule),
	(r'/delete-schedules', DeleteSchedules),
	(r'/store-division-standings', StoreDivisionStandings),
	(r'/store-divisions', StoreDivisions),
	(r'/fetch-divisions', FetchDivisions),
	(r'/fetch-location', FetchLocation),
#	(r'/fetch-agegroups', FetchAgeGroups),
	(r'/fetch-distinct-agegroups', FetchDistinctAgeGroups),
],
debug=True)

"""
def main():
	logging.getLogger().setLevel(logging.DEBUG)
	webapp2.util.run_wsgi_app(app)
	
if __name__ = "__main__":
	main()
"""
