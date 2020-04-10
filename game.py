import random, time, copy, os, shutil, datetime
from callcricketnew import test, innings, bowling, player, team, quickorder, listshow, pitchmake
from altcricket import seri, showteam, order, quickorder

def setup(home, away):
	t = test()
	t.home = team()
	t.away = team()
	t.home.name = home
	t.away.name = away
	t.venue = t.home.name
	t.year = 2020
	t.weather = t.home.name
	t.pitch = pitchmake(t.weather)
	t.raw = [t.year, t.home.name, t.away.name, "Lord's",'', '','','','']
	t.series = seri()
	t.folder = 'scorecards'
	t.saveallcards = True
	return t

def firstxi (x):
	a, o, b, k, f, s, xi = [], [], [], [], [], [], []
	roles = {0:o, 1:b, 2:k, 3:f, 4:s} 

	if len(x.squad) == 0: pool = x.active
	else: pool = x.squad

	for i in pool:
		n = quickorder(i.tag)
		roles[n].append(i)

	k.sort(key = lambda x: x.bat + 5*random.random(), reverse = True)
	if len(k) > 0:
		xi.append(k[0])
	elif len(b) > 0:
		z = random.choice(b)
		xi.append(z)
		b.remove(z)

	o.sort(key = lambda x:  x.bat+ 5*random.random(), reverse = True)
	while len(o) > 0 and len(xi) < 3:
		xi.append(o[0])
		o.pop(0)

	f.sort(key = lambda x: x.bowl+ 5*random.random(), reverse = False)
	while len (f) > 0 and len(xi) < 5:
		xi.append(f[0])
		f.pop(0)

	c = f+s
	c.sort(key = lambda x: x.bowl+ 5*random.random(), reverse = False)
	while len (c) > 0 and len(xi) < 7:
		xi.append(c[0])
		c.pop(0)

	a = [x for x in pool if x not in xi]

	a.sort(key = lambda x:x.bat+ 5*random.random(), reverse = True)
	while len (a) > 0 and len(xi) < 10:
		xi.append(a[0])
		a.pop(0)

	while len(a) > 0 and len(xi) < 11:
		if len([x for x in xi if x.bat < 20 and quickorder(x.tag) > 1]) >= 4: a.sort(key = lambda x: x.bat/2 + max(0, 45-x.bowl)+ 5*random.random(), reverse = True)
		else: a.sort(key = lambda x: x.bat, reverse = True)
		xi.append(a[0])
		a.pop(0)

	xi = order (xi, x)
	return xi


def game(t):
	for i in [t.home, t.away]:
		if len (i.squad) > 11 or i.squad == []: i.xi = firstxi(i)
		else: i.xi = i.active
		#print (i.name, i.xi, i.squad, i.active)
		i.gamecapt = [x for x in i.xi if x.capt == max([x.capt for x in i.xi])][0]
		for j in i.xi: 
			if 'WK' in j.tag: i.wk = j
		if i.wk == '': i.wk = random.choice([x for x in i.xi if x.bowl > 50 or x in i.xi[:4] or'Bat' in x.tag])
		showteam(i)

	t.cricket()
	return t

