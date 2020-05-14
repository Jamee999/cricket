import pickle, random
from historical import histplayers, HistoricalYearsSelect
from customleague import teamnumber, gamenumber, league
from callcricketnew import team, listshow
from altcricket import quickorder, quicksort, quickdesc
 
def teamname (d, t, n):
	x = input('Enter the name of a team, or "default" to fill in the teams with suggested options. ')
	if x == 'default':
		while len(t) < n:
			if d[0] not in t:
				t.append(d[0])
				d.pop(0)
	else: t.append(x)
	return t

def userselection (t, p):
	print ()
	print ('Team so far:', end = ' ')
	t.active = quicksort(t.active)
	print(listshow([(x.name, x.tag) for x in t.active]))
	print ()
	s = []
	for i in range (0, 6):
		c = [x for x in p if quickorder(x.tag) == i]
		n = 0
		if i < 3: c.sort(key = lambda x: x.bat, reverse = True)
		elif i < 5: c.sort (key = lambda x: x.bat + 2*(45-x.bowl), reverse = True)
		else: 
			c = [x for x in p]
			c.sort(key = lambda x: x.bowl, reverse = False)

		while len(c) > 0 and n < 6:
			if c[0] not in s: s.append(c[0])
			c.pop(0)
			n += 1

	s.sort(key = lambda x: quickorder(x.tag))
	print ('List of suggested players:' , end = ' ')
	print(listshow([(x.name, x.tag) for x in s]))

	b = ''
	while b not in [x.name for x in p]:
		a = input('Enter the name of your selection: ')
		a = [x for x in p if x.name == a]
		if len (a) > 0: 
			a = a[0]
			b = a.name
	a.team = t.name
	t.active.append(a)
	p.remove(a)	
	print ()
	return t, p


def selection (t, p, u):
	if u != t:
		for i in p:
			if i.name == 'DG Bradman': 
				i.team = t.name
				t.squad.remove(1)
				t.active.append(i)
				p.remove(i)
				print (t.name.ljust(25), i.name)
				return t, p

		if len(t.squad) > 0: n = random.choice(t.squad)
		else: n = 9

		if 0 <= n <= 4:
			a = [x for x in p if quickorder(x.tag) == n]
		if n > 4 or len(a) == 0:
			a = p

		if n < 3: a.sort(key = lambda x: x.bat + 5*random.random(), reverse = True)
		elif 3 <= n <= 5: a.sort(key = lambda x: x.bowl + 5*random.random(), reverse = False)
		else: a.sort(key = lambda x: x.bat + max(0, 45-x.bowl)*2 + 5*random.random(), reverse = True)

		if len(t.squad) > 0: t.squad.remove(n)
		a[0].team = t.name
		t.active.append(a[0])
		print (t.name.ljust(25), a[0].name)
		p.remove(a[0])
		return t,p
	else:
		t, p = userselection (t, p)
		return t, p






if __name__ == "__main__":
	m = HistoricalYearsSelect (2020, 2020)
	n = 257
	while n > 256 or (n > 16 and (m[0] > 1877 or m[1] < 2020)):
		n = teamnumber ()
	o = gamenumber ()
	t = []
	d = []

	with open('draftteams.txt') as f:
	    for line in f:
	    	d.append(line[:-1])

	while len(t) < n:
		t = teamname (d, t, n)
	print (t)
	t.sort (key = lambda x: random.random())

	y = 0
	while y not in t:
		y = str(input('Enter the name of the team you would like to draft, or type "go" to have the computer select all teams. '))
		if y == 'go': break

	user = ''
	t1 = []
	for i in t:
		x = team()
		x.name = i
		if y == x.name: user = x
		x.squad = [0, 0, 1, 1, 1, 9, 2, 3, 3, 5, 4]
		t1.append(x)
	t = t1

	p = histplayers('all', m[0], m[1])

	print ()
	while len(p) > 0 and len(t[0].active) < 15:
		print ()
		for i in t: 
			if len(p) == 0: break
			i, p = selection (i, p, user)
		print ()
		t.reverse()

	print ()

	print ()

	league (t, o)



