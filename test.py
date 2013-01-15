#from bs4 import BeautifulSoup
from bs4 import *
import urllib2
from decimal import *
from datetime import datetime
from bs4 import NavigableString
import collections
##from collections import OrderedDict
import json
###import webapp2
###import opl_db
import re
import sys

def convert(data):
    if isinstance(data, unicode):
        return str(data)
    elif isinstance(data, collections.Mapping):
        return dict(map(convert, data.iteritems()))
    elif isinstance(data, collections.Iterable):
        return type(data)(map(convert, data))
    else:
        return data



def t():

	doc = BeautifulSoup(urllib2.urlopen("http://www.oregonpremierleague.com/schedules/Fall2012/47896539.20129.html","html5lib"));

	t = doc.find("table").find(id="tblListGames2").find("tbody")
	
	#return t.tr

	# if 'RowHeader' in t.tr.td['class']:
	try: 
		#if 'GameHeader' in t.tr.td['class']:	
		t2 = t.tr.find_all('td',{'class': re.compile(r'/GameHeader/')})
		return t2
			#t1 = t.tr.td.find_previous_sibling('tr')
			#gd = opl_db.GameDay(gamedate = t.tr.td.text.strip())
			#gd.put()
			### print "GameDay: ",t.tr.td.text.strip()
	except KeyError:
		pass
 

def fetch_schedule_results():

	doc = BeautifulSoup(urllib2.urlopen("http://www.oregonpremierleague.com/schedules/Fall2012/47896539.20129.html","html5lib"));

	t = doc.find("table").find(id="tblListGames2").find("tbody")

	print "in fetch scehd results"

	for sib in t.tr.next_siblings:
		if not isinstance(sib, NavigableString):
			gamedate = ''
			gametime = ''
			hometeam = ''
			awayteam = ''
			gamelocation = ''
			gamelocation_url = ''
			homescore = ''
			awayscore = ''
			
			###if(sib.select(".RowHeader")):
			if(sib.select(".GameHeader")):
				gd = sib.previous_sibling.previous_sibling.text.strip()
				#gd = sib.td.text.strip()
				#gd.put()
				print "    gd:",gd

			##t = convert(sib.get("class",''))
			t = sib.get("class")
			if isinstance(t,list):
				if(t.index('sch-main-gm') > 0):
					for td in sib.find_all('td'):
						try:
							if 'gamecode' in td.span['class']:
								gamecode = td.span.text.strip()
						except KeyError:
							pass
						except TypeError:
							pass
						try:
							if 'tim' in td['class']:
								gametime = td.text.strip()
						except KeyError:
							pass
						except TypeError:
							pass
						try:
							if 'schedtm1' in td['class']:
								hometeam = td.text.strip()
						except KeyError:
							pass
						except TypeError:
							pass
						try:
							if 'schedtm2' in td['class']:
								awayteam = td.text.strip()
						except KeyError:
							pass
						except TypeError:
							pass
						try:
							if 'tmcode' in td.span['class']:
								gamelocation = td.text.strip()
								gamelocation_url = td.span.a['href']
						except KeyError:
							pass
						except TypeError:
							pass
						try:
							if 'sch-main-sc' in td['class']:
								if td.text.strip() != 'vs':
									homescore = td.text.strip().split('-')[0]
									awayscore = td.text.strip().split('-')[1]
						except KeyError:
							pass
						except TypeError:
							pass

					###opl_db.Game(gamecode = gamecode, gameday = gd, gametime = gametime, hometeam = hometeam, awayteam = awayteam, homescore = int(homescore), awayscore = int(awayscore)).put()
				print "    ",gamecode
				print "    ",gametime
				print "    ",hometeam
				print "    ",awayteam
				print "    ",gamelocation
				print "    ",gamelocation_url
				print "    ",homescore
				print "    ",awayscore
				print "    GD:",gd
						

"""
def get_all_schedule_results():
	t = opl_db.GameDay.all()

	gamedays = OrderedDict()

	rowarray_list = []
	for r in t.run():
		t = OrderedDict()
		t['id'] = r.key().id()
		t['gamedate'] = r.gamedate
		games_list = []
		for g in r.gamedays:
			game = OrderedDict()
			game['gamecode'] = g.gamecode
			game['gametime'] = g.gametime
			game['hometeam'] = g.hometeam
			game['awayteam'] = g.awayteam
			game['homescore'] = g.homescore
			game['awayscore'] = g.awayscore
			game['created_date'] = g.created_date.strftime('%d-%b-%Y %H:%M:%S')
			game['last_updated_date'] = g.last_updated_date.strftime('%d-%b-%Y %H:%M:%S')
			games_list.append(game)
		t['games'] = games_list
 		t['created_date'] = r.created_date.strftime('%d-%b-%Y %H:%M:%S')
                t['last_updated_date'] = r.last_updated_date.strftime('%d-%b-%Y %H:%M:%S')
		rowarray_list.append(t)

	gamedays['gamedays'] = rowarray_list
	
	j = json.dumps(gamedays)
	return j

def delete_all_schedule_results():
	t = opl_db.GameDay.all()
	for r in t.run():
		r.delete()

	t1 = opl_db.Game.all()
	for r1 in t1.run():
		r1.delete()


class THandler(webapp2.RequestHandler):	
	def get(self):
		self.response.headers['Content-Type'] = 'text/html'
		self.response.write(t())

class ScheduleResultsHandler(webapp2.RequestHandler):
	def get(self):
		delete_all_schedule_results()
		fetch_schedule_results()
		self.response.headers['Content-Type'] = 'text/html'
		self.response.write(get_all_schedule_results())
"""

def t1():
 	doc = BeautifulSoup(urllib2.urlopen("http://www.oregonpremierleague.com/standingsandschedules/Fall2012/index_E.html", "html5lib"));

 	#doc = BeautifulSoup(urllib2.urlopen("http://www.oregonpremierleague.com/standingsandschedules/springleague/index_E.html", "html5lib"));

	# t = doc.find("table").find(id="tblListGames2").find("tbody")

	t = doc.find("table").select(".MainContent")
	doc2 = BeautifulSoup(str(t[0]),"html5lib")

	reload(sys)
	sys.setdefaultencoding('utf-8')
	
	scheds = doc2.find_all("div","tg")

	for g in ['Boys','Girls']:
		p = doc2.find_all('div',text=re.compile(g));
		for ps in p:
			gender = ps.text.strip()
			print '# ', gender
			enclosing = ps.find_previous('td')
			u = enclosing.find_all('div',text=re.compile('Under'))
			for us in u:
				agegroup = us.text.strip()
				print '    ', agegroup
				tms = us.find_next_sibling('table').find_all('div','tg')
				for tm in tms:
					url = tm.a['href']
					name = tm.a.text.strip()
					print '        ',url,'  ',name

def t2():
 	doc = BeautifulSoup(urllib2.urlopen("http://www.oregonpremierleague.com/schedules/Fall2012/47896541.html", "html5lib"));

	fullscore = False

	teamname = ''
	pts = ''
	gp = ''
	w = ''
	l = ''
	t = ''
	gf = ''
	ga = ''
	gd = ''

	if doc.find("td", text=re.compile('PTS')):
		fullscore = True

	t = doc.find("td",text=re.compile('GP'))

 	tbl = t.find_parent("tr").find_parent("table")
	trs = tbl.find_all("tr", "tms")
	for tr in trs:
		tds = tr.find_all("td")
		if(fullscore):
			teamname = tds[0].a.text.strip()
			pts = tds[1].text.strip()
			gp = tds[2].text.strip()
			w = tds[3].text.strip()
			l = tds[4].text.strip()
			t = tds[5].text.strip()
			gf = tds[6].text.strip()
			ga = tds[7].text.strip()
			gd = tds[8].text.strip()
			print teamname, "pts: " , pts, "  gp: " , gp 
		else:
			teamname = tds[0].a.text.strip()
			gp = tds[1].text.strip()
			w = tds[2].text.strip()
			l = tds[3].text.strip()
			t = tds[4].text.strip()
			print teamname, "gp: " , gp, "  w: " ,w

		 

def main():
	print " in main"
	# fetch_schedule_results()
	t2()
		
if __name__ == "__main__":
	main()
