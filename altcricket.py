import random, time, copy, os, shutil, datetime, pickle
from callcricketnew import test, innings, bowling, player, team, quickorder, listshow, pitchmake, playerwrite, scoreformat

def era ():
	eradata = []
	with open ('eradata.txt') as f:
		for line in f:
		    line = line[:-1]
		    #pass #print (line)
		    x = line.split(', ')
		    x[0] = int(x[0])
		    x[1] = float(x[1])
		    #pass #print (Year, x[0])
		    eradata.append(x)
	return eradata        

def tests():
	realtests = []
	q = open('testmatchlist.txt', 'r')
	for line in q:
		#print (line[:-1])
		line = line[1:-2].split(",")
		if len (line) > 10:
			#print (line)
			line[7] = line[7]+ line[8]
			line[8] = line[9]
			line[9] = line[10]
			line.pop(10)

		#print (line)
		line[0] = int(line[0])
		for i in range (1,6):
			line[i] = str(line[i][2:-1])
		line[6] = line[6][2:-1]
		line[7] = str(line[7][2:])
		line[8] = int(line[8][1:-1])
		line[9] = int(line[9][1:])
		#print (line)
		#print ()
		realtests.append(line)
	q.close()

	realtests2 = []
	log = []
	for i in realtests:
		if i[4] in log:
			pass
		else:
			log.append(i[4])
			realtests2.append(i)

	return realtests2

def desc (y):
	x = (y.name.ljust(25)) + y.team.ljust(15)
	x = x + str("%.2f" % round(y.bat,2)).rjust(7) + str("%.2f" % round(y.bowl,2)).rjust(7)
	x = x + " " + y.tag.ljust(13) + " " + str(y.dob) + " " +str(y.first) + " " + str(y.last)
	x = x + " " + str(current - y.dob).ljust(3) #+ "   " + str(y.realfirst) + " " + str(y.reallast) + '   '
	#x = x + str("%.2f" % round(y.sr,2)) + " " + str("%.2f" % round(y.er,2)) 
	#x = x + ' ' + str(y.capt).rjust(3) 
	x = x + '       ' + str(y.games).rjust(3) 
	x = x + ' ' + str(y.runs).rjust(5) + str(y.batav).rjust(6) 
	x = x + '     ' + str(y.wickets).rjust(3) + str(y.bowlav).rjust(7)
	print (x)


def age (x):
	global current
	try:
		return current-x
	except:
		return 25

def scenario (t, m):
	allplayers = []
	if m == 'r':
		for i in t:
			years = []
			for j in i.players:
				years.append(j.first)
			min = years[0]
			years.sort(key = lambda x: random.random())
			for y in i.players:
				y.first = years[0]
				years.pop(0)
				allplayers.append(y)

	elif m == 'c':
		combos = []
		for i in t:
			for y in i.players:
				combos.append([y.first,y.team])
				allplayers.append(y)
		combos.sort(key = lambda x: random.random ())

		for x in allplayers:
			x.first = combos[0][0]
			x.team = combos[0][1]
			if random.random() < 1/200:
				x.secondteam = random.choice(t).name
			combos.pop(0)

		for x in t:
			x.players = [y for y in allplayers if y.team == x.name]

	elif m in ['h','s','t']: 
		for x in t:
			for y in x.players: allplayers.append(y)
		dob = []
		q = open('dob.txt', 'r')
		for line in q:
			line = line[1:-2].split(',')
			line[0] = line[0][1:-1]
			line[1] = int(line[1])
			line[2] = int(line[2])
			dob.append(line)
		q.close()

		if m == 's':
			for i in dob:
				i.append([x.team for x in allplayers if x.name == i[0] and x.first == i[1]][0])

			for i in allplayers:
				i.dob = [x for x in dob if i.name == x[0] and i.realfirst == x[1]][0][2]

			for i in allplayers:
				c = [x for x in dob if x[2] == i.dob]
				x = random.choice(c)
				i.team = x[3]
				#dob.remove(x)

			for x in t:
				x.players = [y for y in allplayers if y.team == x.name]			

	for i in t:
		i.inj = []
		i.players.sort(key = lambda x: x.first)
		min = i.players[0].first
		for y in i.players:

			if m not in ['h', 's', 't']: 
				y.dob = y.first - random.randrange(18,25)

				if y.first - y.dob < 23: y.dob = y.dob - random.randrange(0,3)

				if y.first == min or (y.first == 1992 and y.team == 'South Africa'): y.dob = y.dob - random.randrange(0,20)
				elif y.first < 1918: y.dob = y.dob - random.randrange(0,10)

				y.last = y.dob + random.randrange(35,45)

				if y.last - y.dob >= 40: y.last = y.last - random.randrange(0,5)

			else:
				#print (y.name)
				y.dob = [x for x in dob if y.name == x[0] and y.realfirst == x[1]][0][2]
				if y.dob == 0: print (y.name)

				n = 10 + random.randrange(0,5) + random.randrange(0,5)
				if n > 15: n = n - random.randrange(0,5)

				y.first, y.last = y.realfirst, y.reallast
				if y.reallast >= 2018: y.last = max(y.reallast, y.first+n-10)

				while y.last - y.first < n:
					if y.realfirst < min + 20:
						y.last += 1
					elif y.last - y.dob > 36:
						if random.random() < 0.8: y.first -= 1
						else: y.last += 1
					elif y.first - y.dob < 22:
						if random.random() < 0.2: y.first -= 1
						else: y.last += 1
					else:
						if random.random() < 0.5: y.first -=1
						else: y.last += 1

				if y.first <= min + 20: a, b = 0, random.randrange(0,3)
				else: a, b = random.randrange(-1,2), random.randrange(-1,2)

				y.first = y.first - a
				y.last = y.last + b

				if y.last < y.realfirst: y.last = y.realfirst


			if y.last - y.first < 10: y.last = y.first + 10

	switch = []
	if m == 't':
		q = open('switch.txt', 'r')
		for line in q:
			line = line.split(',')
			switch.append(line)
		q.close()

		for i in switch:
			for j in t:
				z = [x for x in j.players if x.name == i[0]]
				if len (z) > 0: 
					y = z[0]
					j.players.remove(y)
					y.team = i[1].strip()
			for k in t:
				if k.name == y.team:
					k.players.append(y)
					break
			if len(i) > 2:
				y.dob = y.dob + (int(i[2]) - y.first )
				if len(i) == 4: y.last = int(i[3])
				else: y.last = y.last + (int(i[2]) - y.first)

				y.first = int(i[2])

			print (i)

	for i in allplayers:
		q = [x for x in allplayers if i.name == x.name and i.realfirst == x.realfirst and i is not x]
		for j in q:
			if i.name == j.name and i is not j and i.realfirst == j.realfirst:
				allplayers.remove(i)
				allplayers.remove(j)
				for k in t:
					if i in k.players and k.name == i.team: k.players.remove(i)
					if j in k.players and k.name == j.team: k.players.remove(j)

				a = max(i.first,j.first)
				b = max(i.last,j.last)
				c = max(i.dob, j.dob)

				if random.random() < 0.5: y, z = i.team, j.team
				else: y, z = j.team, i.team

				if m == 'h': a, b = i.realfirst, i.reallast

				if y == 'Ireland' or z == 'Ireland': y, z, a = 'Ireland', 'England', 2018
				for k in t:
					if k.name == y and i not in k.players:
						i.team, i.secondteam = y, z
						i.first, i.last, i.dob = a, b, c
						k.players.append(i)
						#print ('add', i.name, k.name)
				#desc (j)
				allplayers.append(i)
				del (j)
				#print ()

	for i in t: 
		i.players = list(dict.fromkeys(i.players))
		for j in i.players:
			if random.random() < 1/1000: j.secondteam = random.choice([x.name for x in t if x is not i])

	return t, allplayers

def setup (x):
	nation = x.replace(" ",'')
	country = x

	pickle_in = open("players","rb")
	players = pickle.load(pickle_in)

	print("Working... {}".format(''.ljust(20)), end="\r")
	quicksort(players)

	for i in players:
		i.basebat = i.bat
		i.basebowl = i.bowl
		i.batform = 25
		i.captgames = []

	a = team()
	a.name = country
	a.players = [x for x in players if x.team == country]
	a.squad = [x for x in a.players if x.first == min]
	a.xi = firstxi (a)
	a.tests = []

	return a



def quicksort (x):
	x.sort(key = lambda x: 10000*quickorder(x.tag) - x.bat - x.batform, reverse = False)
	return x

def showteam (x):
	WK = ''
	capt = ''

	WK = keeper (x.xi)
	
	if x.captain in x.xi:
		capt = x.captain
	else:
		capt = x.lastcapt

	n = 1
	for i in x.xi:
		tag = ''
		if WK == i: tag = "†"
		if capt == i: tag = "*" + tag
		if i != x.xi[-1]: print (str(n) + ' ' + tag + i.name, end = ', ')
		else: print (str(n) + ' ' + tag + i.name)
		n = n + 1

	return WK

def batscore (p, t):
	if p.games >= 5: x = (p.batform + p.bat)/2
	else: x = min(p.bat*(3/4),40)

	if quickorder(p.tag) == 2 and [x for x in t if quickorder(x.tag) == 2 and x.bat < p.bat] == []:
		x = x - 3*(x**0.5)
	elif quickorder(p.tag) > 2: x = x-15

	if quickorder(p.tag) < 2: x = x + p.games**0.5

	return x

def rolecount (t, n):
	return len([x for x in t if quickorder(x.tag) == n])

def order (t, a):
	y = []
	try:
		last = a.lastxi
		wk = a.wk
	except:
		last = []
		wk = ''

	b = [x for x in t if x not in last]
	#print (b)
	b.sort(key = lambda x: batscore(x, t), reverse = True)

	if len (b) == 0: return last

	for i in last:
		if len (y) > 3 or i not in t or 'Open' not in i.tag: break
		else: y.append(i)

	if len (y) < 3:
		o = [x for x in t if 'Open' in x.tag and 'WK' not in x.tag and x not in y]

		if len (o) < 2 or [quickorder(x.tag) for x in t].count(2) > 1:
			o = [x for x in t if 'Open' in x.tag and x not in y]
		o.sort(key = lambda x: batscore(x, t), reverse = True)

	while len (y) < 3 and len(o) > 0:
		y.append(o[0])
		o.pop(0)

	if len (y) < 2:	
		b = [x for x in t if (quickorder(x.tag) < 2 or x.bat > 20) and x not in y and x is not wk]
		b.sort(key = lambda x: x.dob - x.bat)
	while len (y) < 2 and len(b) > 0:
		y.append(b[0])
		b.pop(0)

	z = [x for x in t if x not in y]
	z.sort(key = lambda x: batscore(x, t), reverse = True)

	return y+z

def firstxi (x):
	a, o, b, k, f, s, xi = [], [], [], [], [], [], []
	roles = {0:o, 1:b, 2:k, 3:f, 4:s} 

	if len(x.squad) == 0: pool = x.active
	else: pool = x.squad

	for i in pool:
		if i.status != '': continue
		n = quickorder(i.tag)
		roles[n].append(i)

	k.sort(key = lambda x: value(x, 2) + 5*random.random(), reverse = True)
	if len(k) > 0:
		xi.append(k[0])
	elif len(b) > 0:
		z = random.choice(b)
		xi.append(z)
		b.remove(z)

	o.sort(key = lambda x:  value(x, 0)+ 5*random.random(), reverse = True)
	while len(o) > 0 and len(xi) < 3:
		xi.append(o[0])
		o.pop(0)

	f.sort(key = lambda x: value(x, 3)+ 5*random.random(), reverse = True)
	while len (f) > 0 and len(xi) < 5:
		xi.append(f[0])
		f.pop(0)

	c = f+s
	c.sort(key = lambda x: value(x, 5)+ 5*random.random(), reverse = True)
	while len (c) > 0 and len(xi) < 7:
		xi.append(c[0])
		c.pop(0)

	a = [x for x in pool if x not in xi]

	a.sort(key = lambda x: value (x,1)+ 5*random.random(), reverse = True)
	while len (a) > 0 and len(xi) < 10:
		xi.append(a[0])
		a.pop(0)

	while len(a) > 0 and len(xi) < 11:
		if len([x for x in xi if x.bat < 20 and quickorder(x.tag) > 1]) >= 4: a.sort(key = lambda x: value(x, 1), reverse = True)
		else: a.sort(key = lambda x: value(x, 5)+ 5*random.random(), reverse = True)
		xi.append(a[0])
		a.pop(0)

	xi = order (xi, x)
	return xi

def captscore (x):
	global current
	z = age(x.dob) + 10*random.random() + x.bat**0.5 + x.batform**0.5 + x.batav**0.5 + x.games**0.5 

	if current > 1945: z = z - (len(x.captgames)**2)/5

	if x.capt >= 5: z = z + 10
	elif x.capt > 0: z = z + 5

	if ('Lord ' in x.name or '.' in x.name) and current < 1945: z = z**2
	if age (x.dob) < 25 or x.games < 10: z = z/10

	if current > 1970 and x.last == current: z = 0
	return z

def captselect (a, b, *args):
	a = [x for x in a]
	a.sort(key = lambda x: captscore (x), reverse = True)
	for j in a:
		if j not in args: 
			if j != b: print ('{} ({}, {}) named as captain of {}.'.format(j.name, age(j.dob), j.tag, j.team))
			return j
	return ''

def skip (s):
	if s.games[0][2] == 'England' and s.games[0][1] != 'Australia' and s.games[0][0] < 1945: x = 1/10
	elif s.games[0][0] < 1918: x = 2/3
	elif s.games[0][0] < 1945: x = 3/4
	elif s.games[0][0] < 1970: x = 4/5
	elif s.games[0][0] < 2000: x = 9/10
	else: x = 19/20
	return x

def squad (x, s):
	global dualtours
	c = []
	if s.games[0][0] < 1915: n = random.randrange(13,16)
	else: n = random.randrange(15,18)

	t = skip(s)
	if len(x.active) > n:
		for i in x.active:
			if s.year == 1930 and i in dualtours and s.away.name == 'England' and s.home.name != 'South Africa': continue
			if random.random() < t or i == x.captain or len(x.active) <= n or i.games == 0:
				c.append(i)
		while len(c) < n and len(x.active) -len(c) > 0:
			c.append(random.choice([a for a in x.active if a not in c]))

	else: c = x.active

	x.unav = [y for y in x.active if y not in c]
	for i in x.unav: i.status = 'unav'

	z = quicksort([y for y in x.active if y not in c and y.games > 0])
	print('Unavaliable:', end = ' ')
	if len (z) <= 10:
		print(listshow([quickdesc (y, x) for y in z]))
	else:
		print(listshow([x.name for x in z]))

	q = [y for y in c if y in x.xi and y.games >= 10]
	q = []
	c = [y for y in c if y not in q]

	d = [0,0,1,1,1,1,2,3,3,3,4,2,3,4,1,3,1,5,1,5,1,5,1]

	if s.games[0][1] in ['India', 'Pakistan', 'Sri Lanka', 'Bangladesh', 'Afghanistan']: d = [4] + d

	for i in d:
		if [quickorder(x.tag) for x in q].count(i) >= d.count(i): continue
		if len(c) > 0 and len(q) < n:
			c.sort(key = lambda x: value(x, i), reverse = True)
			q.append(c[0])
			c.pop(0)

	q = quicksort (q)
	print (x.name, 'squad:')
	for i in q: longdesc (i)

	if x.captain == '' or x.captain not in q or s.games[0][0] < 1945: x.captain = captselect(q, x.captain)

	print('Not selected:', end = ' ')
	b = quicksort([y for y in x.active if y not in q and (y.bat > 40 or y.bowl < 30 or (y.bat > 30 and y.bowl < 35) or y.games > 15 or y in x.lastxi) and y in c])
	print(listshow([quickdesc (y, x) for y in b]))

	if s.year == 1930 and s.away.name == 'England': dualtours = q

	return q











def batform (p):
	global eradata
	c = [y for y in eradata if y[0] == current][0][1]
	a, b = 0, 20
	for i in range(35):
		if i < 10:
			try: 
				x = p.inns[-i].runs * (0.75 + p.inns[-i].opposition.rating/200)
				if p.inns[-i].out == 0:
					b = b -1
			except:
				x = c*(2/3)

		else:
			try:
				x = p.inns[-i].runs*0.9**(i-10) * (0.75 + p.inns[-i].opposition.rating/200)
				if p.inns[-i].out == 0:
					b = b - 0.9**(i-10)
			except:
				x = c*(2/3)*0.9**(i-10)

		a = a + x

	#print (p.name.ljust(30), round(a), round(b), a/b)
	return round((30/c)*a/b,2)

def bowlform (p):
	global eradata

	if p.games == 0:
		if quickorder(p.tag) > 2 or 'Part' in p.tag: return 20
		else: return 0

	t = [y for y in eradata if y[0] == current][0][1]
	a, b = 0, 0
	for i in range(35):
		if i < 10:
			try: 
				x = p.bowls[-i].runs / (0.75 + p.inns[-i].opposition.rating/200)
				y = p.bowls[-i].wickets
			except:
				if quickorder(p.tag) > 2:
					x, y = 1.5*t, 1
				else:
					x, y = t, 0

		else:
			try:
				x = p.bowls[-i].runs*0.9**(i-10) / (0.75 + p.inns[-i].opposition.rating/200)
				y = p.bowls[-i].wickets*0.9**(i-10)
			except:
				if quickorder(p.tag) > 2 or 'Part' in p.tag:
					x = 1.5*t*0.9**(i-10)
					y = 1*0.9**(i-10)
				else:
					x, y = t, 0

		a = a + x
		b = b + y

	if b == 0: return 0

	if a == 0:
		return b*10

	c = b/60

	d = t / (a/b)

	#print (p.name.ljust(20), round(a), round(b,1), round(c,3), round(d,3), round(c*d*100, 2))
	return round(c*d*50, 2)

def recent (p):
	global current
	x = 0
	for i in range (6):
		try:
			if p.inns[-i].runs >= 50 and p.inns[-i].test.year - 2 < current:
				x = x + p.inns[-i].runs
		except: pass

		try:
			if p.bowls[-i].wickets >= 3 and p.bowls[-i].test.year - 2 < current:
				x = x + p.bowls[-i].wickets*20
		except: pass

	#print (p.name, x)
	return x

def value (p, n, s = False):
	global current, PaceFactor, SpinFactor
	#p = candidate player, n = role
	x = recent (p)/10

	if quickorder(p.tag) > 2: y = min (50, p.bowl)
	elif 'Part' in p.tag: y = min(60, p.bowl)
	else: y = p.bowl

	if n < 3: x = x + p.bat + p.batform
	else: x = x + (p.bat + p.batform)/2 + 2*p.bowlform + 2*max(0,(60-y))

	c = 0
	for a in range (20):
		b =  25*a
		if x > b: c = c + x-b
		else:
			break

	x = x + c

	y, t = 0, 250

	if age(p.dob) < 25: y = y - (25-age(p.dob))
	if current < 1945: t = 500

	while y <= p.games and (quickorder(p.tag) == n or n == 9) and p.games < 5:
		t = t * random.random()
		y = y+1
		if y > p.games: x = x + t

	if quickorder(p.tag) == n or (n==0 and 'Open' in p.tag) or n == 1 or (n == 5 and quickorder(p.tag) in [3,4]): x = x+100
	elif n == 2: x = x-500

	if current < 1945: x = x * (0.5 + random.random())

	if quickorder(p.tag) == 3  and (n == 3 or n == 5): x = x * (SpinFactor/PaceFactor)**2
	elif quickorder(p.tag) == 4 and (n == 4 or n == 5): x = x * (PaceFactor/SpinFactor)**2

	if s == True and quickorder(p.tag) == 4: x = x*1.25/(SpinFactor**2)

	if age(p.dob) > 35 and current > 1945: 
		y = (age(p.dob)-35)
		if quickorder(p.tag) in ['Spin','OpenSpin']: y = y/2
	elif age(p.dob) < 25: y = (25-age(p.dob))
	else: y = 0
	x = x*0.98**y

	#print (p.name.ljust(20), round(x), n)

	return x

def reinforce (a, x, y, z): #x is type, y is number, z is year
	global current
	if z > current: return a

	d = y - len([q for q in a.squad if q.status == '' and quickorder(q.tag) in x])
	e = [b for b in a.active if b not in a.squad and b.status == '']

	if 9 in x: x = 9
	elif x == [1]: 
		d = y - len([q for q in a.squad if q.status == '' and (quickorder(q.tag) < 2 or q.bat > 25)])
	elif x == [0]:
		d = y - len([q for q in a.squad if q.status == '' and 'Open' in q.tag])
	elif 3 in x and 4 in x: x = 5

	if type (x) == list and len(x) == 1: x = x[0]

	while d > 0 and current >= z and len(e) > 0:
		e.sort(key = lambda p: value (p,x) * random.random(), reverse = True)
		a.squad.append(e[0])
		print (e[0].name, 'added to', a.name, 'squad.')
		longdesc (e[0])
		print ()
		e.pop(0)
		d -= 1

	return a

def replace (p, a):
	c = [x for x in a.squad if x.status == '' and x not in a.xi]
	#if p in a.squad and p not in a.inj: c.append(p)
	if len (c) == 0: return a
	if quickorder(p.tag) == 0 and ['Open' in x.tag for x in a.xi].count(True) > 2:
		c.sort(key = lambda x: value (x,1), reverse = True)
	elif quickorder(p.tag) == 2 and [quickorder(x.tag) for x in a.xi].count(2) > 1:
		c.sort(key = lambda x: value (x,1), reverse = True)
	elif quickorder(p.tag) == 4 and [quickorder(x.tag) for x in a.xi].count(4) > 1:
		c.sort(key = lambda x: value (x,5), reverse = True)
	elif quickorder(p.tag) == 3 and [quickorder(x.tag) for x in a.xi].count(4) == 0:
		c.sort(key = lambda x: value (x,5), reverse = True)
	else:
		c.sort (key = lambda x: value(x, quickorder(p.tag)), reverse = True)

	if p not in a.inj and quickorder(p.tag) == 2 and quickorder(c[0].tag) != 2 and p in a.squad and [quickorder(x.tag) for x in a.xi].count(2) == 1: return a
	else:
		a.xi.remove(p)
		a.xi.append(c[0])
	#print (p.name, "replaced by", c[0].name)
	return a

def injury (a):
	h = []
	for i in a.inj:
		if random.random() < 2/3: h.append(i)

	for i in h:
		a.inj.remove(i)
		i.status = ''
		if i.games >= 10 and i not in a.unav:
			a.xi.sort(key = lambda x: value(x,1) + value (x,quickorder(x.tag)), reverse = False)
			for b in a.xi:
				if value(b,quickorder(b.tag))*1.1 < value(i,quickorder(b.tag)) and i not in a.xi:
					a.xi.remove(b)
					a.xi.append(i)
	for i in a.squad:
		if i not in a.inj:
			if random.random() < 0.02:
				a.inj.append(i)
				continue
			if random.random() < 0.01*(age(i.dob)-30):
				a.inj.append(i)
				continue
			if random.random() < 1/8 and i.tag in ['Fast', 'OpenFast']:
				a.inj.append(i)
				continue
		if i.status == 'strike': i.status = ''

	for i in a.inj:
		i.status = 'inj'
		if i in a.xi:
			a = replace (i, a) 
		if i in a.squad and random.random() < 1/20 and len(a.squad) > 11:
			a.squad.remove(i)
			a.unav.append(i)
			i.status = 'unav'
			if len(a.squad) < 20 or (i in a.lastxi or i.games >=10 or i.bat > 30 or i.bowl < 35):
				print (i.name, 'ruled out from series due to injury.')

	return a

def drop (p, t): #player, team
	global current
	if len(t.squad) <= 11: return False
	if len (t.tests) > 0 and t.tests[-1].win == t and recent (p) > 0: return False
	elif p not in t.xi or (p in [t.captain, t.lastcapt] and current > 1945): return False
	elif p.status == 'unav': return True
	elif p.batform > 40 or p.bowlform > 40 or (p.batform > 30 and p.bowlform > 30) or p.games <= 3 or recent (p) > 100: return False

	y = quickorder(p.tag)

	if y == 2 and len([x for x in t.squad if quickorder(x.tag) == 2 and x not in t.xi]) == 0 and [quickorder(x.tag) for x in t.xi].count(2) == 1: return False

	return True

def keeper (t):
	x = ''
	for i in t:
		if 'WK' in i.tag: x = i
	if x == '':
		for i in t:
			if i.tag in ['Bat', 'OpenBat']: x = i
	if x == '':
		for i in t:
			if quickorder(i.tag) == 1: x = i
	if x == '':
		for i in t: x = [y for y in t if t.bowl == max([z.bowl for z in t])][0]

	return x

def addplayer (a, e, n):
	if len(e) == 0:
		d = [quickorder(x.tag) for x in a.squad if x.status == '']
		return a, d, e
	e.sort(key = lambda x: value (x,n) * random.random(), reverse = True)
	a.squad.append(e[0])
	print (e[0].name, 'added to', a.name, 'squad.')
	longdesc (e[0])
	e.pop(0)
	d = [quickorder(x.tag) for x in a.squad if x.status == '']
	return a, d, e

def resign (c, t): #captain, team
	global current
	if len (t.tests) < 6 or current < 1945 or len(c.captgames) < 5 or c.captgames[-1].loss != t: return t

	a = [x for x in c.captgames if x.win == t]
	b = [x for x in c.captgames if x.loss == t]

	x = len(b) - len (a)

	c.captgames.reverse()

	for i in c.captgames:
		if i.loss == t:
			x = x + 0.5
		if 'innings' in i.margin:
			x = x + 1
		else: break

	c.captgames.reverse()

	if x <= 5: return t

	if random.random() < ((x-5)**2)/100:
		#print (len(c.captgames), len(a), len(b), x)
		print ('{} resigns as captain of {} ({} Tests led, {} wins, {} losses)'.format(c.name, t.name, len(c.captgames), len(a), len(b)))
		while t.captain == c: 
			t.captain = captselect(t.xi, t.captain, *[c])
		if random.random() < 1/3 and c in t.squad: 
			t.squad.remove(c)
			t.unav.append(c)
		print ()

	return t

def strike (a, b):
	if b == False:
		a.squad.sort(key = lambda x: random.random())
		for i in a.squad:
			#if len(a.squad) - len ([x for x in a.active if x.status != '']) <= 11: continue
			if random.random() < 0.5+(i.games/200) or (i in a.xi and random.random() < 0.98): 
				i.status = 'strike'
				if i in a.xi: a.xi.remove(i)

	else:
		for i in a.xi:
			i.status = 'strike'
			a.xi.remove(i)
	print ('{} players go on strike!'.format(a.name))
	print ()

	while len ([x for x in a.squad if x.status == '']) < 11:
		random.choice([x for x in a.squad if x.status == 'strike']).status = ''

	return a

def select (a, s): #team
	global PaceFactor, SpinFactor
	print ()
	print (a.name)
	
	if len(s.results) > 1: a = resign (a.captain, a)

	a = injury (a)

	if random.random() < 1/1000 and len(a.squad) >= 22: a = strike (a, False)
	elif len(s.results) > 0 and a.name =='Australia' and s.results[-1].no == 17: a = strike (a, True)
	elif a.name == 'West Indies' and s.away.name == 'Bangladesh' and s.year == 2009 and len(s.results) == 0: a = strike (a, True)

	if len([x for x in a.inj if x in a.squad]) > 0:
		print ("Injured:", end = " ")
		if len(a.squad) >= 20:
			inj = quicksort([x for x in a.inj if x in a.squad and (x in a.lastxi or x.games >=10 or x.bat > 30 or x.bowl < 35)])
		else: inj = quicksort([x for x in a.inj if x in a.squad])
		print(listshow([quickdesc (x, a) for x in inj]))
		print ()

	b = [x for x in a.xi if x not in a.squad or x.status != '']
	n = 0
	while len (b) > 0:
		if n > 10:
			for i in b:
				a.xi.remove(i)
			break
		for i in b:
			replace (i, a)
		b = [x for x in a.xi if x not in a.squad or x.status != '']
		n += 1

	if a == s.away:
		a = reinforce (a, [3], 2, 1960) #add fast bowlers
		a = reinforce (a, [2], 1, 1960) #add keeper
		a = reinforce (a, [4], 1, 1960) #add spinner
		if s.home in ['India',"Pakistan",'Sri Lanka',"Bangladesh","Afghanistan"]:
			a = reinforce (a, [4], 2, 1980)
		#a = reinforce (a, [0], 2, 1990) #add openers
		a = reinforce (a, [3], 3, 1990) #add more fast bowlers
		a = reinforce (a, [1], 7, 1960)
		a = reinforce (a, [3,4], 4, 1960)
		a = reinforce (a, [0,1,2,3,4,5,9], 11, 1960)

		d = [quickorder(x.tag) for x in a.squad if x.status != '']
		e = [x for x in a.active if x not in a.squad if x.status != '']
		
		z = [x for x in a.squad if x not in a.xi and x.status == '']
		while len(a.xi) < 11 and len (z) > 0:
			z.sort(key = lambda x: value (x,9), reverse = True)
			a.xi.append(z[0])
			z.pop(0)

	c = [x for x in a.squad if x not in a.xi and x.status == '']

	for i in a.xi:			
		if drop (i, a) == True:
			if quickorder(i.tag) == 2 and len([x for x in c if quickorder(x.tag) == 2]) == 0 and len([x for x in a.xi if quickorder(x.tag)]) < 2: continue
			a = replace (i, a)

	if len(a.xi) < 8: a.xi = firstxi (a)

	c = [x for x in a.squad if x not in a.xi and x.status == '']
	while len (a.xi) < 11:
		if len (c) == 0: c = c + a.inj
		c.sort(key = lambda x: value(x,9), reverse = True)
		a.xi.append(c[0])
		c.pop(0)

	b = [x for x in a.xi if quickorder(x.tag) > 2]
	d = [x for x in a.squad if quickorder(x.tag) > 2 and x not in a.xi and x not in a.xi and x.status == '']
	d.sort(key = lambda x: value (x,5))
	e = [x for x in a.xi if quickorder(x.tag) < 2]
	e.sort(key = lambda x: value (x, 1))
	while len(b) < 4 and len(d) > 0 and len (e) > 0:
		a.xi.remove(e[0])
		a.xi.append(d[0])
		e.pop(0)
		d.pop(0)
		b = [x for x in a.xi if quickorder(x.tag) > 2]

	y = [x for x in a.xi if x.bat < 25 and quickorder(x.tag) > 2]
	y.sort(key = lambda x: value (x, 5), reverse = True)
	z = [x for x in a.squad if x not in a.xi and x.bat > 25 and x.status == '']
	z.sort(key = lambda x: value (x, 1), reverse = True)
	while len (y) > 4 and len (z) > 0:
		a.xi.remove(y[-1])
		a.xi.append(z[0])
		y.pop()
		z = [x for x in a.squad if x not in a.xi and x.bat > 25 and x.status == '']

	o = [x for x in a.xi if 'Open' in x.tag]
	p = [x for x in a.squad if 'Open' in x.tag and x not in a.xi and x not in a.xi and x.status == '']
	p.sort(key = lambda x: value (x, 0), reverse = True)
	f = [x for x in a.xi if quickorder(x.tag) <= 2 and x not in o]
	f.sort(key = lambda x: value (x, 0))
	if len(o) < 2 and len (p) > 0 and len(f) > 0:
		a.xi.remove(f[0])
		a.xi.append(p[0])
		f.pop(0)
		p.pop(0)
		o = [x for x in a.xi if 'Open' in x.tag == 0]
		
	o = [x for x in a.xi if quickorder (x.tag) == 2]
	p = [x for x in a.squad if quickorder(x.tag) == 2 and x not in a.xi and x not in a.xi and x.status == '']
	l = [x for x in a.squad if quickorder(x.tag) < 3 and x not in a.xi and x not in a.xi and x.status == '']
	f = [x for x in a.xi if quickorder(x.tag) != 2 and x not in o]
	f.sort(key = lambda x: value (x, 1))

	if len(o) < 1 and len (p) > 0:
		p.sort(key = lambda x: value (x, 2), reverse = True)
		a.xi.remove(f[0])
		a.xi.append(p[0])
	elif len(o) < 1 and len (l) > 0:
		a.xi.remove(f[0])
		a.xi.append(random.choice(l))

	o = [x for x in a.xi if quickorder (x.tag) == 2]
	l = [x for x in a.squad if x not in a.xi and x not in a.xi and x.status == '']
	l.sort(key = lambda x: value (x, 1), reverse = True)
	o.sort(key = lambda x: value (x, 2), reverse = True)
	if len(o) > 1 and len (l) > 0 and random.random() < 0.75:
		a = replace(o[-1], a)

	o = [x for x in a.xi if quickorder (x.tag) == 4]
	p = [x for x in a.squad if quickorder(x.tag) > 2 and x not in a.xi and x not in a.xi and x.status == '']
	r = [x for x in a.xi if quickorder(x.tag) == 3]
	p.sort(key = lambda x: value (x, 3), reverse = True)
	if len(o) > 1 and len (p) > 0 and current > 1960:
		o.sort(key = lambda x: value (x, 5))
		a = replace(o[0], a)
	if len(o) == 0 and len (p) > 0 and len (r) > 2:
		r.sort(key = lambda x: value (x,5, s = True))
		a = replace(r[0], a)

	o = [x for x in a.xi if quickorder (x.tag) == 3]
	p = [x for x in a.squad if quickorder(x.tag) == 3 and x not in a.xi and x not in a.xi and x.status == '']
	p.sort(key = lambda x: value (x, 3), reverse = True)
	while len(o) < 2 and len (p) > 0:
		y = [x for x in a.xi if quickorder(x.tag) < 3]
		z = [x for x in a.xi if quickorder(x.tag) == 4]
		if len (y) > 7:
			y.sort(key = lambda x: value (x,2))
			a.xi.remove(y[0])
			a.xi.append(p[0])
			p.pop(0)
		elif len (z) > 1:
			z.sort(key = lambda x: value (x, 4))
			a.xi.remove(z[0])
			a.xi.append(p[0])
			p.pop(0)
		o = [x for x in a.xi if quickorder (x.tag) == 3]

	if set([x.name for x in a.lastxi]) != set([x.name for x in a.xi]):
		last = quicksort([x for x in a.lastxi])
		now = quicksort([x for x in a.xi])
		a.xi = order (a.xi, a)
		if len ([x for x in last if x not in now]) > 0:
			for j in range (len ([x for x in last if x not in now])):
				y = [x for x in last if x not in now][j]
				z = [x for x in now if x not in last][j]
				print (quickdesc (y, a), 'replaced by', quickdesc (z,a))
			print ()
	else: a.xi = a.lastxi

	for i in a.xi:
		if i.status == 'inj': print (i.name, 'playing while injured.')

	a.lastxi = [x for x in a.xi]

	if a.captain not in a.xi and a.captain.status == '' and a.captain not in a.unav: a.captain = captselect (a.xi, a.captain)

	return a


def milestonegame (a):
	for x in [10, 25, 50, 75, 100, 125, 150, 175, 200]:
		y = []
		for i in a:
			if i.games +1 == x: y.append(i.name)
		
		if len(y) > 0:
			print ('{}th Test:'.format(x), end = ' ')
			print(listshow (y))

def namedesc (x):
	print (x.name.ljust(20), x.team.ljust(13), x.tag.ljust(13), end = ' ')

def agedesc (x):
	namedesc (x)
	print (x.age, end = ' ')

def quickdesc (y, t):
	global current
	if y.status == 'inj': a = ', injured'
	elif y.status == 'unav': a = ', unavaliable'
	elif y.status != '': a = ', {}'.format(y.status)
	elif y not in t.active: a = ', retired'
	else: a = ''

	if y.games == 0: x = '{} ({}, {}, {} Tests{})'.format(y.name, y.tag, age(y.dob), y.games, a)
	elif y.wickets == 0: x = '{} ({}, {}, {} Tests, {} runs @ {}{})'.format(y.name, y.tag, age(y.dob), y.games, y.runs, y.batav, a)
	else: x = '{} ({}, {}, {} Tests, {} runs @ {}, {} wickets @ {}{})'.format(y.name, y.tag, age(y.dob), y.games, y.runs, y.batav, y.wickets, y.bowlav, a) 
	return x

def longdesc (x):
	global current
	print (x.name.ljust(20), end = ' ')
	print (x.team.ljust(13), end = ' ')
	print (x.tag.ljust(13), end = ' ')
	print(x.batdesc(current), end = ' ')
	print ('     ', end = '')
	print(x.shortbowldesc())

def testsetup (s,g):
	global folder
	t = test()
	t.raw = g
	t.year = g[0]
	t.series = s
	t.home = [x for x in s.teams if x.name == g[1]][0]
	t.away = [x for x in s.teams if x.name == g[2]][0]
	t.venue = g[3]
	t.no = int(g[4].replace('Test # ',''))
	t.dates = str(g[7]) + " " + str(g[8])
	t.scorelog, t.inns, t.bowls, t.teaminnings = [], [], [], []
	t.fullcard = True
	t.folder = folder
	return t

def weathercheck (s, g):
	Weather = ''

	if g[0] == 1912 and g[3] not in ['Melbourne','Sydney','Adelaide']: Weather = 'England'
	elif g[0] < 1945: 
		if g[1] == 'Australia': Weather = 'Timeless'
		elif g == s.games[-1] and g[1] != 'England':
			a = len([x for x in s.results if x.win == s.home])
			b = len([x for x in s.results if x.win == s.away])
			if -1 <= (a-b) <= 1: Weather = 'Timeless'

	if Weather == '': Weather = g[1]

	return Weather

def modcheck (t, s):
	for i in t.xi:
		i.mod = 1
		if i.status == 'inj':
			i.mod = 0.8
		if t == s.away:
			i.mod = i.mod*0.95 

	return t


def game (s, g):
	global pause, PaceFactor, SpinFactor, inns, bowls
	import callcricketnew as cricket

	t = testsetup (s, g)

	t.weather = weathercheck (s, g)
	t.pitch = pitchmake (t.weather)

	for i in [t.away, t.home]:
		i = select (i, s)

		if i.captain in i.xi: x = i.captain
		elif i.lastcapt in i.xi: x = i.lastcapt
		else:
			i.lastcapt = captselect(i.xi, i.captain)
			x = i.lastcapt

		i.gamecapt = x
		i.wk = showteam(i)
		i = modcheck (i, s)

	allplayers = [*t.home.xi, *t.away.xi]
	print ()

	h = [x for x in t.home.xi + t.away.xi if x.games == 0]
	#h = quicksort(h)
	#h.sort(key = lambda x: x.team)
	k = [x.name for x in h]

	if g == s.games[0]:
		print ()
		for i in s.home.xi: longdesc(i)
		print('Not selected:', end = ' ')
		b = quicksort([y for y in s.home.active if y not in s.home.xi and (((y.bat > 40 or y.bowl < 30 or y.games > 15 or (y.bat > 30 and y.bowl < 35)) and y.end > current-3) or y in s.home.lastxi) and y.status == ''])
		print(listshow([quickdesc (x, s.home) for x in b]))
		print ()

	if len (h) > 0:
		print ('Debut:', end = ' ')
		print(listshow(k))
		for i in h: i.debut = g[0]

	milestonegame (allplayers)

	t.cricket()

	for i in t.inns:
		if i not in inns: inns.append(i)
	for i in t.bowls:
		if i not in bowls: bowls.append(i)

	for i in allplayers:
		i.batform = batform (i)
		i.bowlform = bowlform (i)

	PaceFactor,SpinFactor = 1,1

	return s, t

def trophy (s):
	global trophies
	for i in trophies:
		if sorted([s.home.name,s.away.name]) == sorted([i[1],i[2]]):
			if len(s.results) >= 2:
				x = len([x for x in s.results if x.win == s.home])
				y = len([x for x in s.results if x.win == s.away])
				if x > y or (x == y and i[3] == s.home.name):
					print (i[0], 'held by', s.home.name)
					i[3] = s.home.name
				elif y > x or (x == y and i[3] == s.away.name):
					print (i[0], 'held by', s.away.name)
					i[3] = s.away.name
				break
			elif len(s.games) >= 2:
				if i[3] == '': print (i[0])
				else: print (i[0], 'held by', i[3])


class seri:
	home = ''
	away = ''
	third = ''
	year = ''
	games = []
	results = []
	inns = []
	bowls = []
	players = []
	teams = []

	def __init__(self):
		games, results, inns, bowls, players, teams = [], [], [], [], [], []


def playerwins (s, p):
	x = 0
	for i in s.results:
		if i.win in ['Draw', 'Tie']: continue
		if p in i.players and i.win.name == p.team: x += 1

	return x

def playseries (s):
	global pause, trophies
	print ()
	print ()
	print ()

	s.teams = []
	s.teams.append(s.home)
	s.teams.append(s.away)
	if s.third == '': 
		print (s.away.name, 'tour of', s.home.name)
		trophy (s)
	else:
		print ('1912 Triangular Tournament in England')
		s.teams.append(s.third)
		

	for i in s.games:
		for j in s.games:
			if i[4] == j[4] and i is not j: s.games.remove(j)

	for i in s.games: print (i)
	print ()
	s.home.squad = [x for x in s.home.active]
	s.away.squad = squad(s.away, s)
	if s.third != '': 
		print ()
		s.third.squad = squad(s.third, s)
	s.results, s.inns, s.bowls = [], [], []

	print ()
	for i in s.teams:
		if i.captain == '' or i.captain not in i.squad: i.captain = captselect (i.squad, 'asdasfasfa')
		print (i.name, "Captain", i.captain.name)
		if s.year < 1945: i.xi = firstxi(i)
		i = injury(injury(i))
		print ()

	print ()
	for i in s.games:
		print ()
		print (i)
		s, x = game(s,i)
		s.results.append(x)
		s.inns = s.inns + x.inns
		s.bowls = s.bowls + x.bowls
		a = len([x for x in s.results if x.win == s.home])
		b = len([x for x in s.results if x.win == s.away])
		c = len([x for x in s.results if x.win == s.third])
		d = len(s.results) - a - b - c
		if s.third == '': print (s.home.name, a, s.away.name, b, 'Draw', d)
		else: print (s.home.name, a, s.away.name, b, s.third.name, c, 'Draw', d)
		print ()
	
	for i in s.results: i.gamedesc()

	print ()
	s.players.sort(key = lambda x: sum([y.runs for y in s.inns if y.player == x]), reverse = True)
	x = []
	for i in s.players:
		r = sum([y.runs for y in s.inns if y.player == i])
		o = sum([y.out for y in s.inns if y.player == i])
		if o == 0: a = r
		else: a = round(r/o,2)
		if (a >= 50 and o > 1) or r >= (80*len(s.results)) or i in s.players[:3]:
			x.append('{} {} runs @ {}'.format(i.name, r, a))
	print (listshow(x))

	s.players.sort(key = lambda x: sum([y.wickets for y in s.bowls if y.player == x]), reverse = True)
	x = []
	for i in s.players:
		r = sum([y.runs for y in s.bowls if y.player == i])
		o = sum([y.wickets for y in s.bowls if y.player == i])
		if o == 0: a = r
		else: a = round(r/o,2)
		if (a <= 25 and o > 5) or o >= (4*len(s.results)) or i in s.players[:3]:
			x.append('{} {} wickets @ {}'.format(i.name, o, a))
	print (listshow(x))
	
	s.players.sort(key = lambda x: sum(20*[y.wickets for y in s.bowls if y.player == x]) +sum([y.runs for y in s.inns if y.player == x]) + 100*playerwins(s, x) + 50*len([y for y in s.results if y.motm == x]) , reverse = True)
	print ()
	print ('Man of the series: {} ({})'.format(s.players[0].name, s.players[0].team))
	print ()
	trophy (s)
	print ()

	if pause == 'p': input()

	for i in s.teams: 
		i = resign (i.captain, i)
		i.unav = []
		for j in i.active:
			if j.status == 'unav': j.status = ''

	return s











def switchcheck (p, t, y, a):
	global teams
	if p.secondteam == '' or random.random() < 1/2 or p.games == 0 or p.secondteam not in [x.name for x in a] or p.end >= y-2: pass
	else:
		print (p.name, "switches from", p.team, 'to', p.secondteam)
		t.players.remove(p)
		if p in t.squad: t.squad.remove(p)
		if p in t.xi: t.xi.remove(p)
		if p in t.active: t.active.remove(p)

		p.team = p.secondteam
		p.secondteam = ''
		for i in teams:
			if i.name == p.team: i.players.append(p)
		longdesc (p)
		
	return p, t

def seasonmaker (i, x):
	carryover = ['Jan','Feb','Mar','Apr']
	fails = [[1888,'South Africa'],[1929,'New Zealand'],[1981,'Sri Lanka'] ]
	if len(i) > 10: return False
	elif (i[0] == 1877 == x): return True
	elif [x,i[1]] in fails or [x,i[2]] in fails: return False
	elif i[1] == 'West Indies':
		if i[0] == x: return True
		else: return False
	elif i[0] == x: return True
	elif i[0] == x+1 and any(y in i[7] for y in carryover) == True and 'Dec' not in i[7]: return True
	else: return False

def namepick (y):
		z = [x for x in y.players if x.games > 15]
		p = []
		if len(z) < 20: return ''
		z.sort(key = lambda x: x.runs, reverse = True)
		p = p + z[:5]
		z.sort
		z.sort(key = lambda x: x.wickets, reverse = True)
		p = p + z[:5]
		z.sort(key = lambda x: x.games, reverse = True)
		p = p + z[:5]
		return random.choice(p)

def trophymaker (x, t):
	global trophies
	if random.random() > 0.5: return trophies
	else:
		a = random.choice(t)
		b = random.choice(t)

		if a == b or a.tests == [] or b.tests == []: return trophies
		else:
			for i in trophies:
				if (i[1] == a.name and i[2] == b.name) or (i[1] == b.name and i[2] == a.name): return trophies
			y = random.choice([a,b])

			if random.random() < 1/2:
				p = namepick(y)
				if p == '' or p.games < 5 or p in y.active:  return trophies
				longdesc (p)
				z = p.name.replace(p.name.split(' ')[0],'')
			else:
				v = [x for x in [a,b] if x is not y][0]
				c = namepick (y)
				d = namepick (v)
				if c == '' or d == '' or c.games < 15 or d.games < 15 or c in y.active or d in v.active: return trophies
				longdesc (c)
				longdesc (d)
				z0 = c.name.replace(c.name.split(' ')[0],'').strip()
				z1 = d.name.replace(d.name.split(' ')[0],'').strip()
				if any([z0 in x[0] for x in trophies]) or any([z1 in x[0] for x in trophies]):
					print (trophies)
					return trophies
				z = str(z0 + '-' + z1)

			n = random.choice(['Trophy','Trophy','Trophy','Trophy','Championship','Series','Shield','Cup'])
			z = z.strip()
			if any([z in x[0] for x in trophies]):
				print (trophies)
				return trophies

			t = z + ' ' + n
			trophies.append([t.strip(),a.name,b.name,''])

			print (t, 'created between', a.name, 'and', b.name)
			print ()

			return trophies

def rateget (i, x): #team, year
	a = [y for y in i.tests if y.year == x]

	points = len([y for y in i.tests if y.win == i and y.year == x]) + (len([y for y in i.tests if y.win == 'Draw' and y.year == x])/2)
	games = len([y for y in i.tests if y.year == x])
	return points, games

def harmmean (x, y):
	a = 2*x*y
	b = x+y
	return a/b

def seasonstats (p, t):
	print ()
	print ()
	print ()
	a = []
	for i in p:
		y = sum([x.runs for x in i.inns if x.test.year == t])
		z = sum([x.out for x in i.inns if x.test.year == t])
		av = round(y/(max(1,z)),2)
		if y > 0: a.append([i, y, av])

	if len(a) >=5:
		n = min (10, len(a))

		print ('Season stats')
		a.sort(key = lambda x: x[1], reverse = True)

		print ('Most runs in', str(t))
		for i in a[:n]:
			print (i[0].name.ljust(20), i[0].team.ljust(13), str(i[1]).rjust(4), "runs @", str(i[2]).rjust(5))
		print ()

		a = []
		for i in p:
			y = sum([x.wickets for x in i.bowls if x.test.year == t])
			z = sum([x.runs for x in i.bowls if x.test.year == t])
			if y > 0: a.append([i, y, round(z/y,2)])

		a.sort(key = lambda x: x[1], reverse = True)

		print ('Most wickets in', str(t))
		for i in a[:n]: print (i[0].name.ljust(20), i[0].team.ljust(13), str(i[1]).rjust(4), "wickets @", str(i[2]).rjust(5))
		print ()


	b = [x for x in inns if x.test.year == t]
	b.sort(key = lambda x: x.runs, reverse = True)
	if len(b) > 50:
		print ('Top innings in', str(t))
		c = [x for x in b if x.runs >= 200 or x in b[:5]]
		c.sort(key = lambda x: x.test.no)
		for i in c:
			if i.out == 1: x = ' '
			else: x = "*"
			print ('{} {} {}'.format(i.name.ljust(20), i.player.team.ljust(12), i.desc() ), end = ' ')
			i.test.gamedesc()
		print ()

	b = [x for x in bowls if x.test.year == t]
	b.sort(key = lambda x: x.wickets - x.runs/20, reverse = True)
	if len(b) > 50:
		print ('Best bowling in', str(t))
		c = [x for x in b if x.wickets >=7 or x in b[:5]]
		c.sort(key = lambda x: x.test.no)
		for i in c:
			print (i.name.ljust(20), i.player.team.ljust(12), i.bowlformat(), end = ' ') 
			i.test.gamedesc()

def rating (x, t, p):
	for i in t:
		points, games = rateget (i, x)
		for j in range (100):
			a = rateget (i, x-j)
			points = points + a[0]*0.8**j
			games = games + a[1]*0.8**j

		if games > 0: i.rating = round(100*points/games,2)
		else: i.rating = -1
		#print (i.name, i.rating, points, games)
	t.sort(key = lambda x: x.rating, reverse = True)

	if len([x for x in t if x.rating >= 0]) > 1:
		print ()
		print ('End of year ratings')
		print ('Teams')
		for i in t:
			if i.rating >= 0: print (i.name.ljust(20), i.rating)

	print ()

	c = [y for y in p if y.first <= x and y.last >=x and y.games >=1 and y.end >= x-2]
	xi = []

	if len (c) >= 25:
		print ('Batsmen')
		c.sort(key = lambda x: x.batform, reverse = True)
		for i in c[:10]:
			namedesc (i)
			print (i.batdesc(x))
		print ()
		a = [x for x in c if 'Open' in x.tag]
		xi = a[:2]

		a = [x for x in c if 'WK' in x.tag]
		if len(a) == 0: pass
		elif a[0] not in xi: xi.append(a[0])

		n = 0
		while len(xi) < 6:
			if c[n] not in xi: xi.append(c[n])
			n = n + 1

		print ('Bowlers')
		c.sort(key = lambda x: x.bowlform, reverse = True)
		for i in c[:10]:
			namedesc (i)
			print (i.bowldesc(x))
		print()

		a = [x for x in c if quickorder(x.tag) == 4]
		if len(a) > 0:
			if a[0] not in xi: xi.append(a[0])

		a = [x for x in c if quickorder(x.tag) == 3]
		if len(a) > 1:
			if a[0] not in xi: xi.append(a[0])
			if a[1] not in xi: xi.append(a[1])

		x = False
		n = 0
		while x == False:
			if c[n] not in xi: 
				xi.append(c[n])
				x = True
			n = n+1

		print ("All-rounders")
		c.sort(key = lambda x: (harmmean(x.batform, x.bowlform)), reverse = True)
		for i in c[:10]:
			print ("{:0.2f}".format(float(harmmean(i.batform, i.bowlform))).rjust(6), end = '    ')
			longdesc (i)

		n = 0
		while len(xi) < 11:
			if c[n] not in xi: xi.append(c[n])
			n = n + 1

		print ()
		print ('World XI:', end = ' ')
		xi = order (xi, '')
		print(listshow (["{} ({})".format(x.name,x.team) for x in xi]))

	return t

def worldseries (t):
	for i in t:
		if i.name == 'South Africa': x = 3
		if i.name in ['Australia','West Indies']: x = 1
		else: x = 1/3

		y = []
		for j in i.players:
			if random.random() < 0.02*x*(min(j.games,45)) and j.first <= 1977 and j.last >= 1977:
				#j.first = 1977 + random.randrange(1, 3)
				y.append(j)
				if j in i.active: i.active.remove(j)

		y.sort(key = lambda x: x.games, reverse = True)
		if len(y) > 0:
			print (i.name, 'players signed by World Series Cricket:')
			for k in y: 
				k.status = 'WSC'
				print(quickdesc (k,i))
			if team.captain in y: team.captain = captselect(team.active, team.captain, team.captain)
		print ()

	return t

def rebels (t, x):
	team = ''
	while team == '':
		for i in t:
			if i.name == 'South Africa': continue
			if i.name == 'England' and random.random() < 1/3: team = i
			elif random.random() < 0.05: team = i
			if team != i: break

	y = []
	for j in team.players:
		if random.random () < 0.15 and j.first <=x and j.last >= x:
			#j.first = x+2
			j.status = 'banned'
			y.append (j)
			if j in team.active: team.active.remove(j) 

	y.sort(key = lambda x: x.games, reverse = True)
	if len(y) > 0:
		print (team.name, 'players signed for rebel tour of South Africa:')
		for k in y: print(quickdesc (k, team))
		if team.captain in y: team.captain = captselect(team.active, team.captain, team.captain)
	print ()

	return t


def retire (t, tag, x):
	print ()
	tick = 0
	for i in t:
		for j in i.players:
			if j.last != x: continue
			elif j.games == 0 and j.age < 50:
				if tag != t: continue
				else:
					j.last = j.last+1
			elif tag == t or (tag.name == j.team and random.random() < 0.2 and j.games > 0 and x < 2019 and j.end >= x-1):
				if tag == t: pass
				else:
					if tag.name == j.team and j not in tag.squad: continue
				j.bat = j.basebat
				j.bowl = j.basebowl
				if j in i.active:
					if tick == 0: print ('Retirement:')
					tick = 1
					i.active.remove(j)
					longdesc (j)
				if j in i.xi: i.xi.remove(j)
				if j in i.inj: i.inj.remove(j)
				if j == i.captain and x > 1945: i.captain = captselect(i.active, i.captain)

	return t

def fillsquad (t, x):
	while len (t.active) < 11:
		a = [y for y in t.players if y.first == x+1]
		if len(a) > 0: 
			z = random.choice(a)
			z.first -= 1
			t.active.append(z)
		else: x +=1 


	return t

def season (x, t):
	global realtests, trophies
	print ()
	print ()
	print ()
	print ('Year:',x)
	trophies = trophymaker(x, t)
	serieslist = []
	series = []
	games = []
	activeteams = []
	for i in realtests:
		if 'ICC World XI' in i: continue
		if i[0] == x and len(i) == 10:
			#games.append(i)
			if [i[1],i[2]] not in serieslist: serieslist.append([i[1],i[2]])
			for j in [i[1],i[2]]:
				if j not in [x.name for x in activeteams]: activeteams.append([x for x in t if x.name == j][0])

	print ('New players:')
	for i in t:
		i.active = []
		i.unav = []
		for j in i.players:
			if j.first <= x and j.last >= x: 
				if j.status not in ['WSC', 'banned'] or random.random() < 1/4: 
					j.status = ''
					i.active.append(j)
		for j in i.active:
			j.age = age(j.dob)
			if j.age > 35: n = j.age-35
			elif j.age < 25: n = 25-j.age
			else: n = 0

			n = 5*n
			j.bat = max( 1, j.basebat * (100-n)/100 )
			j.bowl = j.basebowl * (100+n)/100

			if j.bowl == 0: j.bowl = 40

			j, i = switchcheck(j, i, x, activeteams)

			if j.first == x:
				namedesc (j)
				print (age(j.dob))

	if x == 1977: t = worldseries (t)
	if 1970 < x <= 1990 and random.random() < 0.1: t = rebels (t, x)

	for i in activeteams:
		if len(i.active) < 11: fillsquad (i, x)

		if i.xi == []: i.xi = firstxi (i)
		if (i.captain == '' or i.captain not in i.active or random.random() < 0.1) and x > 1945:
			try: i.captain = captselect (i.xi, i.captain)
			except: i.captain = captselect(i.active, i.captain)

	print ()

	d = []

	if x == 1912: 
		n = seri()
		n.home = [x for x in t if x.name == 'England'][0]
		n.away = [x for x in t if x.name == 'Australia'][0]
		n.third = [x for x in t if x.name == 'South Africa'][0]
		n.year = x
		n.games = []
		for j in realtests:
			if j[2] != 'England' and seasonmaker(j, x) == True:
				j.append('1912 Triangular Tournament')
				n.games.append(j)
		series.append(n)

	for i in serieslist:
		if i[0] == 1912 == x:
			continue
		n = seri()
		n.year = x
		n.home = [x for x in t if x.name == i[0]][0]
		n.away = [x for x in t if x.name == i[1]][0]
		n.games = []
		#print (n.home.name, n.away.name, x)
		for j in realtests:
			if j[1] == n.home.name and j[2] == n.away.name and seasonmaker (j, x) == True:
				j.append(str(n.home.name + ' vs. ' + n.away.name + ' ' + str(x)))
				n.games.append(j)
		series.append(n)

	for i in series:
		if len (i.games) > 0:
			i = playseries (i)
			t = retire (t, i.home, x)
			t = retire (t, i.away, x)
			if i.third != '': t = retire (t, i.third, x)

	seasonstats (allplayers, x)
	t = rating (x, t, allplayers)
	t = retire (t, t, x)

	return t

def startup():
	global current, eradata, PaceFactor, SpinFactor, inns, bowls, folder, pause, dualtours
	current = 1877
	PaceFactor,SpinFactor = 1, 1
	folder = 'altcricket'

	if not os.path.exists(folder): os.makedirs(folder)
	fileList = os.listdir(folder)
	for fileName in fileList: os.remove("{}/{}".format(folder,fileName))

	print ()
	countries = ['England','Australia','South Africa','West Indies','New Zealand','India',
				'Pakistan','Sri Lanka','Zimbabwe','Bangladesh','Afghanistan','Ireland']
	teams = []
	years = []
	realtests = []
	inns = []
	bowls = []
	allplayers = []
	dualtours = []

	eradata = era()

	print ('Modes:')
	print ('historical - player countries and time periods are unchanged')
	print ('text - as historical, except players listed in "switch.txt" will have their countries switched.')
	print ('random - player time periods are randomized, but countries are unchanged')
	print ('shuffle - player countries are randomized, but time periods are unchanged')
	print ('chaos - player countries and time periods are both randomized')
	print ()
	mode = ''
	while mode not in ['r','c','h','s', 't']: mode = input("Input: 'h' for historical, 't' for text, 'r' for random, 's' for shuffle, 'c' for chaos: ")

	pause = input('Type "p" for pause mode. ')

	for i in countries: x = teams.append(setup (i))

	teams, allplayers = scenario (teams, mode)

	realtests = tests()

	trophies = [ ['The Ashes','England','Australia',''],
	['Wisden Trophy','England','West Indies',''],
	['Trans-Tasman Trophy','Australia', 'New Zealand',''],
	['Gandhi-Mandela Trophy','India','South Africa','']
	]

	return teams,realtests, allplayers, trophies

def summary (teams, allplayers, inns, bowls):
	global current
	print ()
	teams.sort(key = lambda x: len([y for y in x.tests if y.win == x.name]), reverse = True)
	for i in teams:
		wins = len([x for x in i.tests if x.win == i])
		draws = len([x for x in i.tests if x.win in ["Draw",'Tie']])
		losses = len([x for x in i.tests if x.loss == i])
		if losses > 0: x = losses
		else: x = 1
		if len(i.tests) > 0: print (i.name.ljust(13), len(i.tests), 'Tests', wins, 'Wins', losses, 'Losses', draws, 'Draws', round(wins/x,2), 'W/L')

	for i in allplayers:
		if i.bowlav == "-": i.bowlav = float("inf")
		i.bat = i.basebat
		i.bowl = i.basebowl

	print ()
	print ('Runs')
	allplayers.sort(key = lambda x: x.runs, reverse = True)
	[(print (x.name.ljust(20), end = ' '), print (x.batdesc(current))) for x in allplayers[:30]]
	print()
	print ('Batting average')
	allplayers.sort(key = lambda x: x.batav, reverse = True)
	[(print (x.name.ljust(20), end = ' '), print (x.batdesc(current))) for x in [x for x in allplayers if x.games >= 20][:30]]
	print()
	print ('Wickets')
	allplayers.sort(key = lambda x: x.wickets, reverse = True)
	[(print (x.name.ljust(20), end = ' '), print (x.bowldesc(current))) for x in allplayers[:30]]
	print()
	print ('Bowling average')
	allplayers.sort(key = lambda x: x.bowlav, reverse = False)
	[(print (x.name.ljust(20), end = ' '), print (x.bowldesc(current))) for x in [x for x in allplayers if x.wickets >= 100][:30]]
	print()
	print ('Tests')
	allplayers.sort(key = lambda x: x.games, reverse = True)
	[longdesc(x) for x in allplayers[:30]]
	print()
	print ('All rounders')
	allplayers.sort(key = lambda x: x.batav, reverse = True)
	[longdesc(x) for x in allplayers if x.runs > 1000 and x.batav>25 and x.wickets > 100 and x.bowlav < 35]
	print ()


	inns.sort(key = lambda x: x.test.no)
	bowls.sort(key = lambda x: x.test.no)

	max = 99
	for i in inns:
		if i.runs >= 300 or i.runs > max or (i.runs >= 200 and i.runs/(i.balls+0.001) >= 1):
			if i.out == 1: x = ' '
			else: x = "*"
			if i.runs > max:
				max = i.runs
			print ('{} {} {}'.format(i.name.ljust(20), i.player.team.ljust(12), i.desc() ), end = ' ')
			i.test.gamedesc()

	print ()
	max = 4,0

	for i in bowls:
		if i.wickets >= 9 or i.wickets > max[0] or (i.wickets == max[0] and i.runs < max[1]) or (i.wickets == 8 and i.runs <=50) or (i.wickets >= 5 and i.runs/i.wickets <= 1):
			print (i.name.ljust(20), i.player.team.ljust(13), i.bowlformat(), end = ' ') 
			i.test.gamedesc()
			if i.wickets > max[0] or (i.wickets == max[0] and i.runs < max[1]): max = [i.wickets,i.runs]

	print ()

	allplayers.sort(key = lambda x: x.dob)
	for i in allplayers:
		if i.games == 0: longdesc (i)

	print ('All players: ', sum([x.runs for x in inns]), 'runs @',sum([x.runs for x in inns])/sum([x.out for x in inns]))
	print ()


if __name__ == "__main__":
	x = datetime.datetime.now()
	teams, realtests, allplayers, trophies = startup()

	for i in range (1877, 2021):
		current = i
		teams = season (i, teams)
		if pause == 'p': input()

	summary (teams, allplayers, inns, bowls)
	print ()
	print(datetime.datetime.now()-x)






