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
from division import FetchDivisions
from opl import FetchGameSchedule
from location import FetchLocation
from league import StoreLeagues
from league import FetchLeagues
from league import FetchAgeGroups
from league import FetchDistinctAgeGroups
from opl import StoreGameSchedule
from opl import DeleteGameSchedule
import logging

class MainPage(webapp2.RequestHandler):
    def get(self):
		self.response.headers['Content-Type'] = 'text/html'
		self.response.write("testing")

app = webapp2.WSGIApplication([
	(r'/', MainPage),
	(r'/fetch-divisions', FetchDivisions),
	(r'/store-schedule', StoreGameSchedule),
	(r'/fetch-schedule', FetchGameSchedule),
	(r'/fetch-location', FetchLocation),
	(r'/store-leagues', StoreLeagues),
	(r'/fetch-agegroups', FetchAgeGroups),
	(r'/delete-schedule', DeleteGameSchedule),
	(r'/fetch-distinct-agegroups', FetchDistinctAgeGroups),
	(r'/fetch-leagues', FetchLeagues),
],
debug=True)

"""
def main():
	logging.getLogger().setLevel(logging.DEBUG)
	webapp2.util.run_wsgi_app(app)
	
if __name__ = "__main__":
	main()
"""
