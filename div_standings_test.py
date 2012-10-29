import urllib2
import re
import json
import string


f = urllib2.urlopen("http://www.oregonpremierleague.com/standingsandschedules/Fall2012/index_E.html")

found = False
standings = []

for line in f:
	if not found:
		try:
			if (line.lstrip().index('diiStand = {')):
				found = True
		except ValueError:
			pass	
	else:
		if re.match("^tms:", line.lstrip()):
			standings.append(line.lstrip().replace('tms','"tms"'))
		elif  re.match("^}", line.lstrip()):
			standings.append(line.lstrip())
			break
		elif  re.match("^{", line.lstrip()):
			standings.append(line.lstrip())
		else:
			standings.append(line.lstrip().replace(':', ': [', 1)+"]")
			

standings_str = string.join(standings, '')

#print standings_str

j = json.loads('{'+standings_str+'}')

print j

for tm in j['tms']:
	print tm 

#print j['tms']['51462815']['TOT_PTS']
print j['tms']

for t,v in j['tms'].iteritems():
	for l in v:
		print l['TOT_PTS']
		print l['TOT_GP']
		print l['TOT_W']
		print l['TOT_L']
		print l['TOT_T']
		print l['TOT_GD']
		print l['TOT_GF']
		print l['TOT_GA']
		print l['gp']		# games played
		print l['cb']
		print l['bp']
		print l['flt']
		print l['rank']
		print l['tghr']
		print l['tmcd']
		print l['tm']
		print l['tgnm']		# division
		print l['tg']
		print l['seed']
		print l['tgseq']
		print l['tmnm']		# team name

