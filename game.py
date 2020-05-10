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

def value (p, t, s = False):
	x = p.bat
	if quickorder(p.tag) == 3: x = x + (60-p.bowl)*3*(t.pitch[1]/t.pitch[0])
	elif quickorder (p.tag) == 4: 
		x = x + (60-p.bowl)*3*(t.pitch[0]/t.pitch[1])
		if s == True: x = x*1.5
	return x + 10 * random.random()

def firstxi (x, t):
	if len(x.squad) == 0: pool = x.active
	else: pool = x.squad

	f = [x for x in pool if quickorder(x.tag) == 3]
	f.sort(key = lambda x: x.bowl - 5*random.random())
	y = f[:2]

	pool = [x for x in pool if x not in y]
	pool.sort(key = lambda x: value(x, t), reverse = True)
	y.append(pool[0])
	pool.pop(0)

	if len ([x for x in y if quickorder(x.tag) == 4]) == 0: pool.sort(key = lambda x: value (x, t, s = True), reverse = True)
	else: pool.sort(key = lambda x: value (x, t), reverse = True)
	y.append(pool[0])

	#print ([x.name for x in y])

	pool = [x for x in pool if x not in y]
	pool.sort(key = lambda x: x.bat + 5*random.random(), reverse = True)
	y = y + pool[:5]

	#print ([x.name for x in y])

	o = [x for x in pool if 'Open' in x.tag and x not in y]
	while len([x for x in y if 'Open' in x.tag]) < 2 and len(o) > 0:
		y.append(o[0])
		o.pop(0)

	k = [x for x in pool if 'WK' in x.tag and x not in y]
	if len([x for x in y if 'WK' in x.tag]) < 1 and len(k) > 0: y.append(k[0])

	pool = [x for x in pool if x not in y]
	while len (y) < 11:
		y.append(pool[0])
		pool.pop(0)

	y = order (y, x)
	return y


def game(t):
	for i in [t.home, t.away]:
		if len (i.active) != 11: i.xi = firstxi(i, t)
		else: i.xi = i.active
		#print (i.name, i.xi, i.squad, i.active)
		i.gamecapt = [x for x in i.xi if x.capt == max([x.capt for x in i.xi])][0]
		for j in i.xi: 
			if 'WK' in j.tag: i.wk = j
		if i.wk == '': i.wk = random.choice([x for x in i.xi if x.bowl > 50 or x in i.xi[:4] or'Bat' in x.tag])
		showteam(i)

	t.cricket()
	return t

