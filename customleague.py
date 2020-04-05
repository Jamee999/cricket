from custom import getcustom
from game import setup, game
from altcricket import seri

def league (t, n):
	log = []
	for i in t:
		log.append([i.name, 0, 0])

	s = seri()
	for i in t:
		s.players = s.players + i.active

	c = 1
	for y in range (n):
		for i in t:
			for j in t:
				if j == i: continue
				print ()
				print ()
				#print (i.name, 'vs.', j.name)
				print ()
				g = setup (i.name, j.name)
				g.home.active = i.active
				g.away.active = j.active
				x = game (g)
				s.results.append(x)
				s.inns = s.inns + x.inns
				s.bowls = s.bowls + x.bowls
				x.no = c
				c += 1

				for k in log:
					if k[0] in [g.home.name, g.away.name]: k[2] +=1
					if g.win in ['Draw','Tie']: continue
					if g.win.name == k[0]: k[1] += 1
				log.sort(key = lambda x: x[1], reverse = True)
				for k in log:
					print ('{} {} games {} wins'.format(k[0].ljust(20), k[2], str(k[1]).rjust(3)))

	print ()
	print ()
	print ()
	for i in s.results: i.gamedesc()

	print ()
	for k in log:
		print ('{} {} games {} wins'.format(k[0].ljust(20), k[2], str(k[1]).rjust(3)))
	print ()

	s.players.sort(key = lambda x: x.runs, reverse = True)
	for i in s.players:
		if i.batav > 50 or i in s.players[:10]:
			print ('{} ({}) {} runs @ {}'.format(i.name, i.team, i.runs, i.batav), end = ', ')
	print()
	print ()
	s.players.sort(key = lambda x: x.wickets, reverse = True)
	for i in s.players:
		if (i.bowlav < 25 and i.wickets > 10) or i in s.players[:10]:
			print ('{} ({}) {} wickets @ {}'.format(i.name, i.team, i.wickets, i.bowlav), end = ', ')

	s.players.sort(key = lambda x: 20*x.wickets + x.runs + 100*[a[1] for a in log if a[0] == x.team][0], reverse = True)
	print ()
	print ()
	print ('Man of the series: {} ({})'.format(s.players[0].name, s.players[0].team))
	print ()


def teamnumber ():
	n = 0
	while type(n) is not int or n < 2:
		n = input('Enter number of teams in league: ')
		try: n = int(n)
		except: pass
	return n

def gamenumber ():
	n = 0
	while type(n) is not int or n <= 0:
		n = input('How many times should teams play each other? ')
		try: n = int(n)
		except: pass
	return n

if __name__ == '__main__':
	print ('Custom league')

	x = teamnumber ()
	t = []
	for i in range (x):
		t.append(getcustom(t))

	n = gamenumber ()

	league (t, n)
