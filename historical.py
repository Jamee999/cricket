from callcricketnew import test, innings, bowling, player, team, quickorder, listshow, playerwrite
from game import game, setup
from altcricket import seri
import pickle, datetime, random, copy

def HistoricalYearsSelect (x,y):
	a, b = 1,1
	CurrentYear = datetime.datetime.now().year
	valid = 0
	Years = [z for  z in range (1877, CurrentYear+1) if z < 1914 or z > 1946 or (1919 < z < 1939)] #Defines acceptable years
	while a not in Years + ['all', 'random', 'same']: #loops until given acceptable answer
		if a != 1 and b != 1: print ('Invalid input.')
		a, b = 0, 0
		a = str(input("Type 'all' for all-time teams, 'random' for a random year, or input a year (or range of years): ")) #User Input
		if a == 'same': return [x,y]
		elif a == 'all': return [1877,CurrentYear]
		elif "-" in a:
			x = a.split("-")
			a = int(x[0])
			b = int(x[1])
			if a not in Years or b not in Years:
				a = 0
		else: a, b = int(a), int(a)

	return [a,b]

def CountrySelect(x,y, *Team1Name):
	x = int(x)
	y = int(y)
	z = ''
	Teams = ['England', 'Australia', 'South Africa', 'West Indies', 'New Zealand', 'India', 'Pakistan', 'Sri Lanka', 'Zimbabwe', 'Bangladesh', 'Ireland', 'Afghanistan', 'random', 'all']
	if x == 1877 and y >= 2020: pass
	else:
		if y < 2018:
		    Teams.remove('Ireland')
		    Teams.remove('Afghanistan')
		if y < 2000: #remove teams from ineligible years.
		    Teams.remove('Bangladesh')
		if y < 1992:
		    Teams.remove('Zimbabwe')
		if y < 1982:
		    Teams.remove('Sri Lanka')
		if y < 1952:
		    Teams.remove('Pakistan')
		if y < 1932:
		    Teams.remove('India')
		if y < 1930:
		    Teams.remove('New Zealand')
		if y < 1928:
		    Teams.remove('West Indies')
		if y < 1889 or (x > 1970 and y < 1992):
		    Teams.remove('South Africa')

	while z not in Teams:
		z = str( input ('Select a team. The options are ' + listshow(Teams) + ": "))
		if z == 'random':
			z = random.choice([x for x in Teams if x not in ['random','all']])
		if z not in Teams: print ('Invalid selection.')
	print (z)
	print ()
	return z

def histplayers (t, y, z):
	pickle_in = open("players","rb")
	players = pickle.load(pickle_in)

	if t == 'all': p = [x for x in players if y <= x.last and z >= x.first]
	else: p = [x for x in players if x.team == t and y <= x.last and z >= x.first]
	return p

def series (home, away, homeplayers, awayplayers):
	n = 0
	while n > 1000 or n < 1:
		n = input('Enter number of games to be played: ')
		try: n = int(n)
		except: 
			print ('Invalid input')
			n = 0

	s = seri()

	for i in range (n):
		g = setup(home = home, away = away)
		g.year = 2020
		g.home.active = homeplayers
		g.away.active = awayplayers
		s.games.append(g)

	s.home = g.home
	s.away = g.away

	c = 1
	a, b, d = 0, 0, 0
	for i in s.games:
		x = game(i)
		s.results.append(x)
		s.inns = s.inns + x.inns
		s.bowls = s.bowls + x.bowls
		i.no = c
		c += 1

		if i.win in ['Draw', 'Tie']: d += 1
		elif i.win.name == s.home.name: a+= 1
		elif i.win.name == s.away.name: b += 1

		print ('',s.home.name, a, s.away.name, b, 'Draw', d)
		print ()
	
	for i in s.results: i.gamedesc()

	print ()

	print ('',s.home.name, a, s.away.name, b, 'Draw', d)
	print ()

	s.players.sort(key = lambda x: sum([y.runs for y in s.inns if y.player == x]), reverse = True)
	for i in s.players:
		r = sum([y.runs for y in s.inns if y.player == i])
		o = sum([y.out for y in s.inns if y.player == i])
		if o == 0: a = r
		else: a = round(r/o,2)
		if (a >= 50 and o > 1) or r >= 100*len(s.results) or i in s.players[:3]:
			print (i.name, r, "runs @", a, end = ', ')
	print()
	s.players.sort(key = lambda x: sum([y.wickets for y in s.bowls if y.player == x]), reverse = True)
	for i in s.players:
		r = sum([y.runs for y in s.bowls if y.player == i])
		o = sum([y.wickets for y in s.bowls if y.player == i])
		if o == 0: a = r
		else: a = round(r/o,2)
		if (a <= 25 and o > 5) or o >= (4*len(s.results)) or i in s.players[:3]:
			print (i.name, o, "wickets @", a, end = ', ')
	s.players.sort(key = lambda x: sum(20*[y.wickets for y in s.bowls if y.player == x]) +sum([y.runs for y in s.inns if y.player == x]) + 100*len([y for y in s.results if y.win == x.team]), reverse = True)
	print ()
	print ('Man of the series: {} ({})'.format(s.players[0].name, s.players[0].team))
	print ()




if __name__ == "__main__":
	print ()
	[a,b] = HistoricalYearsSelect(2020, 2020)
	home = CountrySelect(a,b)
	[x,y] = HistoricalYearsSelect(a,b)
	away = CountrySelect(x,y,home)

	homeplayers = histplayers(home, a, b)
	awayplayers = histplayers(away, x, y)

	if home == away:
		home = '{} {}'.format(home, a)
		away = '{} {}'.format(away, x)

	series (home, away, homeplayers, awayplayers)


