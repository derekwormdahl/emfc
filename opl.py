#from bs4 import BeautifulSoup
from bs4 import *
import urllib2
from decimal import *
from datetime import datetime
from bs4 import NavigableString
import collections

def convert(data):
    if isinstance(data, unicode):
        return str(data)
    elif isinstance(data, collections.Mapping):
        return dict(map(convert, data.iteritems()))
    elif isinstance(data, collections.Iterable):
        return type(data)(map(convert, data))
    else:
        return data
 

doc = BeautifulSoup(urllib2.urlopen("http://www.oregonpremierleague.com/schedules/Fall2012/47896539.20129.html","html5lib"));

t = doc.find("table").find(id="tblListGames2").find("tbody")


print "*********************************************************"
#print t.tr.next_sibling.next_sibling.next_sibling.next_sibling


if 'RowHeader' in t.tr.td['class']:
	print t.tr.td.text.strip()

for sib in t.tr.next_siblings:
	if not isinstance(sib, NavigableString):
		if(sib.select(".RowHeader")):
			gamedate = sib.td.text.strip()
			print gamedate

		gametime = ''
		team1 = ''
		team2 = ''
		gamelocation = ''
		gamelocation_url = ''
		homescore = ''
		awayscore = ''
		
		t = convert(sib.get("class",''))
		if isinstance(t,list):
			if(t.index('sch-main-gm') > 0):
				for td in sib.find_all('td'):
					try:
						# print "Class:",td
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
							team1 = td.text.strip()
					except KeyError:
						pass
					except TypeError:
						pass
					try:
						if 'schedtm2' in td['class']:
							team2 = td.text.strip()
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
			print "    ",gamecode
			print "    ",gametime
			print "    ",team1
			print "    ",team2
			print "    ",gamelocation
			print "    ",gamelocation_url
			print "    ",homescore
			print "    ",awayscore
					
			print "****** Game Day: *****",sib.td.text.strip()
		#else:
		# print "************ ",sib
		#for tt in t:
		#	print tt
		"""
		t1 = convert(sib.attrs)
		if t1.has_key('class'):
			print t1['class']
			"""
		#print 'class' in sib.attrMap
		#if((sib.get("class")).contains("sch-main-gm")):
		#	print "    game"#,g.td.span.text
	#print "Sib: ",sib," Type: ",type(sib)



"""
gamedays = doc.findAll('td', {'class':'RowHeader'})
for gameday in gamedays:
	print gameday.string


print doc2.tr.next_sibling

