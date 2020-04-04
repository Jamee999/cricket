import random, shutil, datetime, math

def listshow (x):
	a = ''
	for i in x:
		if i != x[-1]: a = a + '{}, '.format(i)
		else: a = a + '{}'.format(i)
	return a

def playerwrite (a):
	x = "[" + '"' + a.name + '", '

	for i in [a.bat, a.bowl, a.tag, a.first, a.last, a.sr, a.er, a.capt]:
		if i == a.tag:
			x = x + '"'
			x = x + a.tag
			x = x + '", '
		else: x = x + str(i) + ', '
	x = x + "]"
	return x

def scoreformat (x):
	if x[1] == 10: return str(x[0])
	else: return '{}-{}'.format(x[0],x[1])

def showteam (x):
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

	WK = ''
	capt = ''

	WK = keeper (x.xi)
	
	if x.captain in x.xi:
		capt = x.captain
	else:
		capt = x.lastcapt

	a = ''

	n = 1
	for i in x.xi:
		tag = ''
		if WK == i: tag = "†"
		if capt == i: tag = "*" + tag
		if i != x.xi[-1]: a = a + '{} {}{}, '.format(n,tag,i.name)
		else: a = a + '{} {}{}'.format(n,tag,i.name)
		n = n + 1

	return a

def environment (Year):
	with open ('eradata.txt') as f:
		for line in f:
		    line = line[:-1]
		    x = line.split(', ')
		    if int(x[0]) == Year:
		        era = x[1]

	with open ('er_data.txt') as f:
	    for line in f:
	        line = line[:-1]
	        x = line.split(', ')
	        if int(x[0]) == Year:
	            er = x[1]

	return float (era), float (er)

def pitchmake (Weather):
	PaceFactor = 1 + (0.3*random.random()) * (random.random()-random.random()) #how good the pitch is for pace. 0.75-1.25, lower is better for bowling
	SpinFactor = 1 + (0.3*random.random()) * (random.random()-random.random()) #same for spin

	Asia = ['India','Pakistan','Sri Lanka','Bangladesh','Afghanistan']

	if Weather in Asia:
	    p = (4 + random.random())/5
	    if Weather == 'Pakistan':
	        p = (1+p)/2
	    PaceFactor = PaceFactor/p
	    SpinFactor = SpinFactor*p

	print ("Pace Factor:", "{:0.2f}".format(PaceFactor), "Spin Factor:", "{:0.2f}".format(SpinFactor))

	return [PaceFactor, SpinFactor]

def conditions (Weather):
    GameOvers = 450 #maximum number of overs in the game

    Asia = ['India', 'Pakistan', 'Sri Lanka', 'Bangladesh', 'Afghanistan']

    if Weather == 'Timeless': GameOvers = random.randrange(550,1000)

    elif Weather in ['England','New Zealand','Ireland']:
        if random.random() < 0.1: GameOvers = random.randrange(50,450)
        elif random.random() < 0.25: GameOvers = random.randrange(300,450)

    elif Weather in ['Australia','India','Pakistan','Afghanistan','Zimbabwe']:
        if random.random() < 0.01: GameOvers = random.randrange(50,450)
        elif random.random() < 0.1: GameOvers = random.randrange(300,450)

    elif Weather in ['South Africa','New Zealand','Sri Lanka','Bangladesh']:
        if random.random() < 0.03: GameOvers = random.randrange(50,450)
        elif random.random() < 0.15: GameOvers = random.randrange(300,450)

    return GameOvers

def quickorder (y):
	if 'WK' in y: return 2
	elif "Open" in y: return 0
	elif y == "Spin": return 4
	elif y in ["Fast", "Med"]: return 3
	else: return 1

def excessrpo (b):
	if b.overs == 0: return 0
	elif b.runs / b.overs < 4: return 0
	else: return 4 - (b.runs/b.overs)

def openingbowlers (a):
	x = a.bowl + (a.bat)/3
	if 'WK' in a.tag: x = x + 100
	elif 'Spin' in a.tag or 'Bat' in a.tag: x = x + 50
	elif 'Part' in a.tag: x = x + 25
	return x

def oversballs (x):
	if x.balls == 0 : return str(x.overs)
	else: return '{}.{}'.format(x.overs, x.balls)

class teaminnings:
	def __init__(self, t):
		self.test = t
		self.team = t.tobat
		self.bowlteam = [x for x in [t.home, t.away] if x is not self.team][0]
		self.innings = []
		self.order = []
		self.active = True
		self.onstrike = self.team.xi[0]
		self.batsmen = [self.team.xi[0],self.team.xi[1]]
		self.bowlers = [x for x in self.bowlteam.xi]
		self.bowlers.sort(key = lambda x: openingbowlers (x))
		self.bowler = self.bowlers[0]
		self.otherbowler = self.bowlers[1]
		self.fatigue = []
		self.extras = [0,0,0,0,0]

	def inningsheader (self):
		if len(self.test.teaminnings) > 2: self.number = '2nd'
		else: self.number = '1st'

		y = (' {} - {} innings'.format(self.team.name, self.number))

		if len(self.test.teaminnings) == 3 and self.test.teaminnings[1].team == self.team: y = y + ' (following on)'
		if len(self.test.teaminnings) == 4: y = y + ' (Target: {} in {} overs)'.format(self.target()+self.runs, self.test.remaining() + self.overs)
		self.test.score (y)

	def run (self):
		self.active = True
		for i in self.team.xi:
			x = innings (i, self.test)
			self.innings.append(x)
			i.innings = x
			x.opposition = self.bowlteam
		for i in self.bowlteam.xi:
			i.bowling = bowling (i, self.test)
			i.bowling.opposition = self.team

		while self.wickets < 10 and self.active == True:
			self.test.raincheck()
			self.over()

		self.allout()

	def runsadd (self, n):
		self.runs = self.runs + n
		self.onstrike.innings.runs = self.onstrike.innings.runs + n
		self.bowler.bowling.runs = self.bowler.bowling.runs + n
		if n == 4:
			self.onstrike.innings.fours +=1
		elif n == 6:
			self.onstrike.innings.sixes +=1

		self.milestone(n)
		self.partnership(n)
		self.swap(n)

	def pitchfactor (self):
		if 'Spin' in self.bowler.tag: return self.test.pitch[1]
		else: return self.test.pitch[0]

	def bowlchange (self):
		if 'Fast' in self.bowler.tag:
			x =  self.fatigue.count(self.bowler)*3 + self.bowler.bowling.spell - 7*self.bowler.bowling.wickets + excessrpo(self.bowler.bowling)
		else:
			x = self.fatigue.count(self.bowler) + self.bowler.bowling.spell - 7*self.bowler.bowling.wickets + excessrpo(self.bowler.bowling)
		if 'Part' in self.bowler.tag: x = x+2
		elif 'Bat' in self.bowler.tag or 'WK' in self.bowler.tag: x = x+3
		if 'Fast' in self.bowler.tag: x = 1.5*x
		if x < 1: x = 1
		x = x**2

		if self.overs < 2: x = 0
		elif self.overs % 80 < 2: x = 100

		if random.random() < x/100: 
			self.bowler.bowling.spell = 0
			return self.bowlchoice()
		else: return self.bowler

	def bowlchoice (self):
		a = self.bowler
		n = 10
		c = [x for x in self.bowlteam.xi 
		if x is not self.bowler and x is not self.otherbowler and x is not self.bowlteam.wk]
		c.sort(key = lambda x: self.bowlvalue(x), reverse = False)
		return c[0]

	def bowlvalue (self, p):
		o = self.overs % 80
		t = quickorder(p.tag)

		x = p.bowl + excessrpo(p.bowling) - 7*p.bowling.wickets

		if 'Fast' in p.tag:
			x = x + self.fatigue.count(p)**2
		else:
			x = x + 0.5*self.fatigue.count(p)**2 

		if 'Part' in p.tag: x = x + 50
		if 'Bat' in p.tag: x = x + 100
		if 'WK' in p.tag: x = x + 100
		if o < 15 and 'Spin' in p.tag: x = x + 50
		elif o < 25 and 'Spin' in p.tag: x = x + 25
		if self.overs < 50 and t < 3: x = x + 50
		if self.partnership(0) > 150 and t < 3: x + x - 20
		if t == 4: x = x * self.det() * self.test.pitch[1]
		else: x = x * self.test.pitch[0]
		if self.wickets > 7 and t > 2: x = x + 50

		x = x - 50*random.random()

		return x

	def det (self):
		if 'Spin' in self.bowler.tag: daydict = dict({1:1.3, 2:1.2, 3:1.1, 4:0.9, 5:0.7})
		else: daydict = dict({1:1.1, 2:1.05, 3:1, 4:0.95, 5:0.9})

		if self.day() > 5: x = daydict[5]
		else: x = daydict[self.day()]

		if ('Fast' in self.bowler.tag or 'Med' in self.bowler.tag) and self.overs%80 < 10: x = x * 0.9

		return x

	def aggfactor (self):
		x = 1
		if len(self.test.teaminnings) < 4:
			if self.runs > 400: x =  x + (self.runs-400)/1000
			if self.wickets > 1 and self.runs/self.wickets < 15: x = x - 0.2

		elif len(self.test.teaminnings) == 4 and self.test.remaining() > 0:
			y = self.target() - self.runs
			r = y / self.test.remaining()
			z = 10 - self.wickets

			if 6 > r > 3 and z > 4 and self.test.remaining() < 50:
				x = x + (r-3)/10
			if r > 4 and z <= 4:
				x = x - 0.2


		if self.onstrike.innings.runs > 150: x = x + (self.onstrike.innings.runs-150)/1000

		return x

	def wicketrate (self):
		y = 1
		if 'WK' not in self.bowlteam.wk.tag: y = 0.8

		y = y * (self.test.rpo/self.test.base) * (1/6)
		y = y * self.aggfactor() * max (1, self.aggfactor()**2)
		y = y / (self.onstrike.bat/30)**0.8
		y = y / (self.bowler.bowl/30)**0.5
		y = y / self.det()**0.5
		y = y / self.onstrike.innings.form()**0.5
		y = y / self.pitchfactor()**0.5
		y = y * self.bowler.er**0.5
		y = y * self.onstrike.sr**0.5
		return y

	def rate (self):
		y = self.test.rpo/6
		y = y * self.aggfactor()
		y = y * (self.onstrike.bat/30)**0.2
		y = y * (self.bowler.bowl/30)**0.5
		y = y * self.det()**0.5
		y = y * self.onstrike.innings.form()**0.5
		y = y * self.pitchfactor()**0.5
		y = y * self.bowler.er**0.5
		y = y * self.onstrike.sr**0.5
		#print (self.onstrike.name, self.onstrike.bat, self.bowler.name, self.bowler.bowl, y)
		return y

	def howout (self):
		def catcher (x):
			y = [y for y in x.xi if y is not self.bowler and y is not self.bowlteam.wk] + [y for y in x.xi[:6] if y is not self.bowler and y is not self.bowlteam.wk]
			return random.choice(y).name

		x = random.random()
		if x < 0.2143: return 'b. {}'.format(self.bowler.name)
		elif x < 0.3573: return 'lbw. b. {}'.format(self.bowler.name)
		elif x < 0.52: return 'c. †{} b. {}'.format(self.bowlteam.wk.name, self.bowler.name)
		elif x < 0.9065: 
			y = catcher(self.bowlteam)
			if y == self.bowler:
				return 'c. & b. {}'.format(self.bowler.name)
			else:
				return 'c. {} b. {}'.format(y, self.bowler.name)
		elif x < 0.9568:
			if random.random() > 0.9 and ('Med' in self.bowler.tag or 'Spin' in self.bowler.tag):
				return 'st. †{} b. {}'.format(self.bowlteam.wk.name, self.bowler.name)
			else:
				return 'c. †{} b. {}'.format(self.bowlteam.wk.name, self.bowler.name)
		elif x < 0.9983: return 'run out ({})'.format(random.choice(self.bowlteam.xi).name)
		elif x < 0.9999: return 'hit wicket b. {}'.format(self.bowler.name)
		else: return 'obstructed the field b. {}'.format(self.bowler.name)

	def wicket (self):
		self.wickets += 1
		self.onstrike.innings.out = True
		self.onstrike.innings.dismissal = self.howout()

		if 'run out' not in self.onstrike.innings.dismissal:
			self.bowler.bowling.wickets += 1

		if self.partnership(0) >= 0:
			if self.wickets != 10: x = ' - new batsman {}'.format(self.team.xi[self.wickets+1].name)
			else: x = ''
			self.test.logger('{} {} {} ({}b) {}x4 {}x6 - partnership {} {}'.format(self.onstrike.name, self.onstrike.innings.dismissal, self.onstrike.innings.runs, self.onstrike.innings.balls, self.onstrike.innings.fours, self.onstrike.innings.sixes, self.partnership(0), x))
		if self.bowler.bowling.wickets >= 5:
			self.test.logger('{} {}'.format(self.bowler.name, self.bowler.bowling.bowlformat()))

		self.onstrike.innings.FOW = [self.onstrike, self.runs,self.wickets]
		if self.wickets < 10:
			self.batsmen.remove(self.onstrike)
			self.batsmen.append(self.team.xi[self.wickets+1])
			self.onstrike = self.batsmen[-1]
			self.declaration()

	def extracheck (self):
		e = random.random()
		if e < 0.268: 
			extra = 'b'
			e = random.random()
			if e < 0.2:
				self.runs += 4
				self.extras[0] += 4
				self.partnership(4)
				return
			elif e < 0.4:
				self.runs +=1
				self.extras[0] += 1
				self.swap(1)
				self.partnership(1)
				return

		elif e < 0.632: 
			e = random.random()
			extra = 'lb'
			if e < 1/7:
				self.runs += 4
				self.extras[1] +=4
				self.partnership(4)
				return
			elif e < (1/7 + 1/50):
				self.runs += 2
				self.extras[1] += 2
				self.partnership(2)
				return
			elif e < 193/350:
				self.runs += 1
				self.extras[1] +=1
				self.swap(1)
				self.partnership(1)
				return

		elif e < 0.697: 
			extra = 'w'
			if random.random() < 0.1:
				self.runs +=4
				self.extras[2] += 4
				self.bowler.bowling.runs += 4
				self.partnership(4)
				return
			elif random.random() < 0.7:
				self.runs +=1
				self.extras[2] += 1
				self.bowler.bowling.runs += 4
				self.partnership(4)
				return

		elif e < 0.9979: 
			extra = 'nb'
			self.runs +=1
			self.extras[3] +=1
			self.balls -= 1
			self.bowler.bowling.runs += 1
			self.partnership(1)

		else: 
			if random.random() < 1/5:
				e = 'pen'
				self.runs += 5
				self.extras[4] += 5
				self.balls -= 1
				self.partnership(5)
				return

	def ball (self):
		a = self.onstrike
		b = self.bowler
		extra = ''

		z = self.rate()
		y = self.wicketrate()

		#print (a.name, b.name, round (self.onstrike.bat), round (self.bowler.bowl), round(z,3), round(y, 3), self.aggfactor())

		four = 0.06*z
		six = 0.003*z
		x = random.random()			

		self.balls += 1 
		self.onstrike.innings.balls += 1

		self.bowler.overcount()
		self.bowler.bowling.balls += 1

		if random.random() < 0.027:
			self.extracheck()

		if x < y: i = self.wicket()
		elif x < 3*y: 
			self.onstrike.innings.chances += 1
			self.bowler.bowling.chances += 1

		elif x > 1 - six: self.runsadd(6)
		elif x > 1 - six - four: self.runsadd(4)
		elif x > 1 - six - four - z:
			c = random.random()
			if c < 0.4: self.runsadd(1)
			elif c < 0.49: self.runsadd(2)
			elif c < 0.512: self.runsadd(3)

	def over (self):
		x = self.runs
		y = self.bowlchange()
		if y != self.bowler:
			self.bowler.bowling.spell == 0
		self.bowler = y

		self.fatigue.append(self.bowler)
		if len(self.fatigue) > 25: self.fatigue.pop(0)
		if self.bowler.bowling not in self.order: self.order.append(self.bowler.bowling)
		self.day()
		while self.balls < 6 and self.wickets < 10 and self.active == True:
			if self.test.remaining() <= 0: 
				self.active = False
				self.result()
				break
			self.ball()
			self.result()
			

		self.day()

		if self.runs - x == 0 and self.balls == 6: 
			self.bowler.bowling.maidens += 1
			self.bowler.maidens += 1

		if self.balls == 6: 
			self.overs, self.balls = self.overs+1, 0
			self.bowler.bowling.overs +=1
			self.bowler.bowling.spell += 1
			self.bowler.bowling.balls = 0

		self.declaration()
		if self.wickets < 10 and self.active == True: 
			self.swap(1)
			self.bowler, self.otherbowler = self.otherbowler, self.bowler

	def day (self):
		y = round(1+(self.test.overcount())//90)
		z = self.test.overcount() % 90
		a = '{} {}* ({}b), {} {}* ({}b)'.format(self.batsmen[0].name, self.batsmen[0].innings.runs, self.batsmen[0].innings.balls, self.batsmen[1].name, self.batsmen[1].innings.runs, self.batsmen[1].innings.balls)

		if self.test.gameovers <= 450:
			y = min(5,y)

		if (z == 30 or z == 60) and self.balls == 0 and self.overs > 0:
			if z == 30:
				self.test.logger('Lunch: ' + a)
			elif z == 60:
				self.test.logger('Tea: ' + a)

		x = 'Day {}'.format(y)
		if y > self.test.daytracker:
			if y > 1:
				self.test.logger('Close of play: ' + a) 
			self.test.logger(x)
			self.test.daytracker = y
		return y

	def swap (self, n):
		if n % 2 == 1:
			if self.batsmen[0] == self.onstrike: self.onstrike =self. batsmen[1]
			else: self.onstrike = self.batsmen[0]

	def lead (self):
		a = sum([x.runs for x in self.test.teaminnings if x.team == self.team])
		b = sum([x.runs for x in self.test.teaminnings if x.team != self.team])
		return a-b

	def milestone (self, n):
		x = self.onstrike.innings.runs-n
		if x % 50 > 10 and self.onstrike.innings.runs % 50 <= n:
			self.test.logger('{} {}* ({}b) {}x4 {}x6'.format(self.onstrike.name, self.onstrike.innings.runs, self.onstrike.innings.balls, self.onstrike.innings.fours, self.onstrike.innings.sixes))

	def partnership (self, n):
		try: a = max([x.FOW[1] for x in self.innings if x.FOW is not ''])
		except: a = 0
		y = self.runs-a
		if y % 50 < n and y >= 50:
			z = 50*round(y/50)
			x = '{} partnership between {} and {}.'.format(z,self.batsmen[0].name,self.batsmen[1].name)
			self.test.logger(x)
		return y

	def declaration (self):
		if self.test.weather == 'Timeless' or len(self.test.teaminnings) == 4 or self.wickets == 10: return False
		if self.batsmen[0].runs % 100 > 89 or self.batsmen[1].runs % 100 > 89: return False
		if len(self.test.teaminnings) == 1 and (self.runs > 500 or self.overs > 150) and random.random() < self.runs/50000: 
			self.declare = True
		if len(self.test.teaminnings) == 2 and self.runs > 500 and self.lead() > -50 and random.random() < 0.01: 
			self.declare = True
		if len(self.test.teaminnings) == 2 and (self.runs/self.test.teaminnings[0].runs > 2) and self.overs > 100 and random.random() < 0.01:
			self.declare = True
		if len(self.test.teaminnings) == 3 and self.lead() > (self.test.remaining()*self.test.rpo + 50) and self.test.remaining() > 35:
			self.declare = True
			

		if self.declare == True:
			self.test.logger('{} declared with a lead of {}.'.format(self.team.gamecapt.name, self.lead()))
			self.active = False
			#self.allout()
		else:
			return False

	def allout (self):
		if self.balls == 6:
			self.balls = 0
			self.overs += 1
		if self.bowler.bowling.balls == 6:
			self.bowler.bowling.balls = 0
			self.bowler.bowling.overs += 1
		self.bowler.overcount()

		if len(self.test.teaminnings) < 4 or self.test.win != '':
			q,w = '',''
			if self.batsmen[0].innings.out == False: q = "*"
			if self.batsmen[1].innings.out == False: w = "*"
			self.test.logger('End of innings - {} {}{} ({}b), {} {}{} ({}b).'.format(self.batsmen[0].name, self.batsmen[0].innings.runs, q, self.batsmen[0].innings.balls, self.batsmen[1].name, self.batsmen[1].innings.runs, w, self.batsmen[1].innings.balls))

		self.test.tobat = self.followon()
		self.test.logprint()
		self.inningsheader()

		for a in self.test.players:
			a.stats(self.test)

		for a in self.innings:
			a.stats()
			if a.out == False: 
				a.dismissal = 'not out'
				FOW = ''
			else:
				if a.FOW[2] == 10:
					FOW = '{}ao'.format(a.FOW[1])
				else:
					FOW = '{}-{}'.format(a.FOW[1],a.FOW[2])

			tag = ''
			if a.player == self.team.gamecapt: tag = tag + '*'
			if a.player == self.team.wk: tag = tag + "†"

			if len(tag) > 1:
				name = a.name.ljust(19)
			else:
				name = a.name.ljust(20)

			if self.test.fullcard == True:
				 a.scorecard = '{}{} {} {} {} FOW: {}      {}'.format(tag.rjust(1),name, a.dismissal.rjust(50), str(a.runs).rjust(3), '({})'.format(a.balls).rjust(5),FOW.rjust(5),a.player.batdesc(self.test.year))
			else:
				a.scorecard = '{}{} {} {} {} FOW: {}'.format(tag.rjust(1),name, a.dismissal.rjust(50), str(a.runs).rjust(3), '({})'.format(a.balls).rjust(5),FOW.rjust(5))
			
			if a.balls > 0:
				self.test.score (a.scorecard)

		if sum(self.extras) > 0:
			a = ''
			if self.extras[0] >0: a = a + '{}b, '.format(self.extras[0])
			if self.extras[1] >0: a = a + '{}lb, '.format(self.extras[1])
			if self.extras[2] >0: a = a + '{}w, '.format(self.extras[2])
			if self.extras[3] >0: a = a + '{}nb, '.format(self.extras[3])
			if self.extras[4] >0: a = a + '{}pen, '.format(self.extras[4])

			a = a[:-2]
			self.test.score('{} - extras {}'.format(a, str(sum(self.extras)).rjust(3)).rjust(76))
		else:
			self.test.score('extras 0'.rjust(76))

		if self.wickets == 10:
			y = '(all out - {} overs) {}'.format(oversballs (self), self.runs)
		elif self.declare == True:
			y = '({} wickets declared - {} overs) {}'.format(self.wickets, oversballs (self), self.runs)
		else:
			y = '({} wickets - {} overs) {}'.format(self.wickets, oversballs (self), self.runs)


		self.test.score (y.rjust(76))

		b = [x.name for x in self.innings if x.balls == 0]
		if len (b) > 0:
			self.test.score(' Did not bat: {}'.format(listshow(b)))

		self.test.score( '{}{}{}{}{}'.format(''.ljust(21),'O'.center(6), 'M'.center(7), 'R'.center(5), 'W'.center(5)))
		for i in self.bowlers:
			i.bowling.stats()
			if i.bowling.overs == 0 and i.bowling.balls == 0:
				continue
			if self.test.fullcard == True:
				y = ' {} {} - {} - {} - {} {} {} {}'.format(i.name.ljust(20), oversballs(i.bowling).center(4), str(i.bowling.maidens).rjust(2), str(i.bowling.runs).rjust(3), str(i.bowling.wickets).rjust(2),i.bowling.player.tag.center(20), ''.ljust(34),i.bowldesc(self.test.year))
			else:
				y = ' {} {} - {} - {} - {} {}'.format(i.name.ljust(20), oversballs(i.bowling).center(4), str(i.bowling.maidens).rjust(2), str(i.bowling.runs).rjust(3), str(i.bowling.wickets).rjust(2),i.bowling.player.tag.center(20))
			self.test.score (y)

	def followon (self):
		if len(self.test.teaminnings) != 2:
			return self.bowlteam
		elif self.test.teaminnings[0].runs - 200 > self.runs and self.wickets == 10:
			self.test.logger('{} chose to enforce the follow-on.'.format(self.bowlteam.gamecapt.name))
			return self.team
		else:
			return self.bowlteam

	def target (self):
		a = sum([x.runs for x in self.test.teaminnings if x.team == self.team])
		b = sum([x.runs for x in self.test.teaminnings if x.team != self.team])
		return b-a+1

	def margin (self):
		a = sum([x.runs for x in self.test.teaminnings if x.team == self.team])
		b = sum([x.runs for x in self.test.teaminnings if x.team == self.bowlteam])

		if b > a and len(self.test.teaminnings) == 3:
			if b-a != 1: return 'an innings and {} runs'.format(b-a)
			else: return 'an innings and 1 runs'
		elif b > a and len(self.test.teaminnings) == 4:
			if b-a != 1: return '{} runs'.format(b-a)
			else: return '1 runs'
		elif len(self.test.teaminnings) == 4 and a > b:
			if self.wickets != 9: return '{} wickets'.format(10-self.wickets)
			else: return '1 wicket'
		else: return ''

	def endofgame (self):
		self.test.blank()
		self.result()
		a, b = [], []
		if self.test.win == '':
			return

		if self.test.win in ['Draw', 'Tie']:
			for i in self.test.teaminnings:
				x = [i.runs, i.wickets]
				if i.team == self.test.teaminnings[0].team: a.append(scoreformat(x))
				else: b.append(scoreformat(x)) 
			
			if self.test.win == 'Draw':
				x = ' {} ({}) drew with {} ({}).'.format(self.test.teaminnings[0].team.name, listshow(a), [x for x in [self.test.home, self.test.away] if x is not self.test.teaminnings[0].team][0].name, listshow(b))
			else:
				x = ' {} ({}) tied with {} ({}).'.format(self.test.teaminnings[0].team.name, listshow(a), [x for x in [self.test.home, self.test.away] if x is not self.test.teaminnings[0].team][0].name, listshow(b))
		
		else: 
			for i in self.test.teaminnings:
				x = [i.runs, i.wickets]
				if i.team == self.test.win: a.append(scoreformat(x))
				else: b.append(scoreformat(x))
			x = ' {} ({}) beat {} ({}) by {}.'.format(self.test.win.name, listshow(a), [x for x in [self.test.home, self.test.away] if x is not self.test.win][0].name, listshow(b), self.test.margin)
		self.test.score(x)

		self.test.motmpick()
		self.test.score(' Man of the Match: {} ({})'.format(self.test.motm.name, self.test.motm.team))
		if self.test.lostovers > 0:
			self.test.score(' {} overs lost to bad weather.'.format(self.test.lostovers))
		self.test.score(' Pace Factor: {}, Spin Factor: {}'.format(round(self.test.pitch[0],2), round(self.test.pitch[1]),2))
		#self.test.logger('End of game:'+x)
		self.test.logprint()

		#####ONLY SAVE SCORECARDS FROM THIS POINT ON ######

		if len(test.teaminnings) == 4:
			if self.test.win == self.test.teaminnings[1].team == self.test.teaminnings[2].team: self.test.cardsave()

		if any((x.runs >= 700 or (x.runs <=50 and x.wickets ==10)) for x in self.test.teaminnings): self.test.cardsave()
		if any((x.runs >= 250 or (x.runs>=200 and (x.runs/x.balls > 1 or self.test.year < 1900))) for x in self.test.inns): self.test.cardsave()
		if any(x.wickets > 8 and x.runs < 1000 for x in self.test.bowls):self.test.cardsave() 
		if any(x.wickets == 8 and x.runs < 50 for x in self.test.bowls):self.test.cardsave() 
		if any(x.wickets >=6 and x.runs <=10 for x in self.test.bowls): self.test.cardsave()

	def finish (self):
		if self.balls == 6:
			self.overs += 1
			self.balls = 0
		self.active = False

		self.test.margin = self.margin()

	def result (self):
		a = sum([x.runs for x in self.test.teaminnings if x.team == self.team])
		b = sum([x.runs for x in self.test.teaminnings if x.team == self.bowlteam])

		#print (a, b, self.test.remaining())

		if self.test.remaining() <= 0:
			self.test.win, self.test.margin = 'Draw', 'Draw'
			self.finish()
			return

		if len (self.test.teaminnings) == 4:
			if a > b: 
				self.test.win = self.team
				self.finish()
				return
			if self.wickets == 10:
				if b > a:
					self.test.win = self.bowlteam
					self.finish()
					return
				elif a == b:
					self.test.win, self.test.margin = 'Tie', 'Tie'
					self.finish()
					return

		elif len(self.test.teaminnings) == 3:
			if b > a and self.wickets == 10:
				self.test.win = self.bowlteam
				self.finish()
				return

		if b > a and self.wickets < 10: return

	test = ''
	team = ''
	bowlteam = ''
	number = ''
	active = ''
	declare = False

	runs = 0
	wickets = 0
	overs = 0
	balls = 0
	extras = []

	onstrike = ''
	batsmen = ''
	bowler = ''
	innings = ''
	order = ''
	fatigue = ''

class test:
	def __init__(self):
		self.raw = []
		self.card = []
		self.log = []
		self.inns, self.bowls = [], []
		self.teaminnings = []
		self.players = []
		self.log = []

	def cricket (self):
		t = datetime.datetime.now()
		self.card = []
		self.playerlog()
		self.header()
		self.base, self.rpo = environment (self.year)
		self.gameovers = conditions (self.weather)
		self.pregamestats()
		self.toss()
		for i in range (4):
			if self.win != '':
				continue
			x = teaminnings (self) 
			self.teaminnings.append(x) 
			self.blank()
			x.run()
		self.teaminnings[-1].endofgame()
		self.stats()
		for i in self.players:
			i.stats(self)
		print ()
		for i in self.log:
			print (i)
		#for i in self.card:
			#print (i)
		#print(datetime.datetime.now()-t)
		if self.win == '': int ('s')

	def decision (self):
		if random.random() < 0.8:
			self.score ('{} has elected to bat first.'.format(self.toss.gamecapt.name))
			self.choice = True
		else:
			self.score ('{} has elected to field first.'.format(self.toss.gamecapt.name))
			self.choice = False

	def toss (self):
		self.toss = random.choice([self.home, self.away])
		x = '{} has won the toss.'.format(self.toss.name)
		self.score(x)
		self.decision()
		if self.choice == True: self.tobat = self.toss
		else: self.tobat = [y for y in [self.home, self.away] if y is not self.toss][0]

	def overcount (self):
		return sum([x.overs for x in self.teaminnings]) + sum([x.balls > 0 for x in self.teaminnings if x is not self.teaminnings[-1]]) + self.lostovers

	def raincheck (self):
		if self.gameovers >= 450: return
		elif self.lostovers == 450-self.gameovers: return
		elif random.random() < (450-self.gameovers)/4500:
			x = random.randrange(0,10) + round(random.random()*(450-self.gameovers))
			x = min (x, self.remaining())
			if x > 0:
				self.logger('{} overs lost due to bad weather.'.format(x))

				n = 90
				while n < self.overcount() + self.lostovers:
					if self.overcount() < n < self.overcount() + x: self.teaminnings[-1].day()
					n = n + 90

				self.lostovers = self.lostovers + x
				#self.logger(str(self.overcount()))
			#if self.overcount() >= self.gameovers: self.teaminnings[-1].active = False
				
	def remaining (self):
		if self.gameovers <= 450: return 450 - self.overcount()
		else: return max(0, self.gameovers - self.overcount())

	def playerlog (self):
		self.players = [*self.home.xi, *self.away.xi]

	def time (self):
		x = (self.overcount() % 90)
		if self.overcount() > 450 and self.gameovers == 450:
			x = (self.overcount() - 360) + 15
		if 30 < x <= 60: x = x + 10
		elif 60 < x <= 90: x = x + 15

		y = round(x // 15)
		z = round(4*(x % 15))

		if x == 0 and self.teaminnings[-1].balls == 0 and self.overcount() <= self.gameovers or (self.overcount() == self.gameovers == 450):
			y, z = 7, random.randrange(0,5)

		#print (self.overcount() , round(x), 11+y, z)
		return '{}:{}'.format(11+y,str(z).zfill(2))

	def logger (self, x):
		t = self.time()
		y = self.teaminnings[-1]
		x = [x, t]
		x.append('{} {}-{} ({}.{} overs)'.format(y.team.name, y.runs, y.wickets, y.overs, y.balls))
		n = self.teaminnings[-1].lead()
		if len(self.teaminnings) == 1: x.append('')
		elif len(self.teaminnings) in [2,3]:
			if n > 0: x.append(' lead by {}'.format(n))
			elif n == 0: x.append(' scores level')
			else: x.append(' trail by {}'.format(-n))
		else: x.append(' target {}'.format(self.teaminnings[3].target()+self.teaminnings[3].runs))


		l = [a[0] for a in self.log]
		if x[0] not in l:
			self.log.append(x)

	def logprint (self):
		for i in self.card:
			print (i)
		self.card = []

		y = ['Lunch:', 'Tea:', 'End of innings']
		with open (self.scorecard, 'a') as f:
			for i in self.log:
				b = i[1]
				z = '{} {} {}'.format(b,str(i[2] + i[3]).ljust(45), i[0])
				if 'Day ' in i[0]:
					f.write('\n')
					print ()
					f.write(str(i[0]))
					print (i[0])
				elif 'Close of play' in i[0]:
					b = '18:00'
					f.write(z)
					print (z)
				else:
					f.write(z)
					print (z)
				f.write('\n')

				if any(x in i[0] for x in y):
					f.write('\n')
					print ()
		self.log = []

	def header (self):
		with open (self.scorecard, 'w') as f:
			pass
		x = '{} vs. {}'.format(self.home.name, self.away.name)
		self.score(x)

	def blank (self):
		with open (self.scorecard, 'a') as f:
			f.write('\n')
		self.card.append('')

	def cardkeep (self, x, end = '\n'):
		with open (self.scorecard, 'a') as f:
			f.write(x)
			f.write(end)

	def score (self, x, end = '\n'):
		self.card.append(x)
		self.cardkeep(x, end)

	def cardsave (self):
		try:
			f = open('{}/scorecard{}.txt'.format(self.folder, self.no))
		except:
			f = open('scorecard.txt','r')
			c = []
			for line in f: c.append(line)
			f.close()

			y = '{}, {} v. {} at {}, {} {}\n'.format(self.raw[4],self.raw[1],self.raw[2],self.raw[3],self.raw[7],self.raw[8])
			#c.insert(0,y)
			if len (self.series.results) > 0: d = ['Series:\n']
			else: d = []
			for t in self.series.results:
				if t.win in ['Draw', 'Tie']: z = t.win
				else: z = t.win.name + ' won by ' + t.margin
				d.append('Test # {}, {}, {}, {}\n'.format(t.no, t.venue, t.dates, z))

			if len([y for y in self.players if y.games == 1]) > 0:
				d.append('\nDebut: ')
				for i in [y for y in self.players if y.games == 1]:
					d[-1] = d[-1] + i.name + ', '
				d[-1] = d[-1][:-2]
				d.append('\n')

			e1 = '{}: {}'.format(self.home.name, showteam(self.home))
			e2 = '{}: {}'.format(self.away.name, showteam(self.away))

			c = [y] + d + ['\n'] + [e1] + ['\n'] + [e2] + ['\n'] + ['\n'] + c[1:]
			with open('scorecard.txt','w') as f:
				for i in c: f.write(str(i))
			shutil.copy('scorecard.txt','{}/scorecard{}.txt'.format(self.folder, self.no))
		finally:
			f.close()

	def gamedesc (self):
		if self.win == 'Draw': y = 'Draw'
		elif self.win == 'Tie': y = 'Tie'
		else: y = '{} won by {}'.format(self.win.name, self.margin)
		#print ((self.home.name, 'v.', self.away.name).ljust(35), 'at', self.venue.ljust(15), "| Test #", str(self.no).ljust(4),'|', self.dates, '|', y, '| MOTM:', self.motm.name)
		print ('{} v. {} at {} Test #{} {} {} MOTM: {}'.format(self.home.name.center(15), self.away.name.center(15), self.venue.center(20),str(self.no).ljust(4), self.dates.center(30), y.center(50), self.motm.name))

	def pregamestats (self):
		self.home.tests.append(self)
		self.away.tests.append(self)
		for i in self.players:
			if self.series != '' and i not in self.series.players: self.series.players.append(i)
			i.games = i.games+1
			i.end = self.year
			i.motmscore = 0
			if i in [self.home.gamecapt, self.away.gamecapt]: i.captgames = i.captgames + 1

	def motmscore (self, p):
		x = 0
		a = [x for x in self.bowls if x.player == p]
		b = [x for x in self.inns if x.player == p]
		x = x + sum([i.wickets for i in a])*self.base + sum([i.overs for i in a])*self.rpo*0.5 - sum([i.runs for i in a])

		x = x + sum([i.runs for i in b])
		if len(self.teaminnings) > 2:
			x = x + 0.5*sum([x.runs for x in self.teaminnings[2].innings if x.player == p])
			if len(self.teaminnings) == 4:
				x = x + sum([x.runs for x in self.teaminnings[3].innings if x.player == p])

		if self.win in ['Draw','Tie']: pass
		elif p in self.win.xi: x += 100

		return x

	def motmpick(self):
		self.players.sort(key = lambda x: self.motmscore(x), reverse = True)
		self.motm = self.players[0]
		self.motm.motm += 1

	def stats (self):
		m = self.margin.split(" ")
		if self.win == 'Tie':
			self.cardsave ()
		elif self.win == 'Draw' and len(self.teaminnings) == 4:
			if self.teaminnings[3].wickets == 9 or self.teaminnings[3].runs >= 300: self.cardsave()
			if self.gameovers > 450: self.cardsave()

		elif 'runs' in self.margin and 'innings' not in self.margin:
			if int(m[0]) < 6: self.cardsave ()
		elif 'wickets' in self.margin:
			if int(m[0]) == 1: self.cardsave()
			if self.teaminnings[3].runs >= 300: self.cardsave()

	year = 0
	daytracker = 0
	series = ''
	home = ''
	away = ''
	venue = ''
	no = 0
	dates = ''

	win = ''
	margin = ''
	motm = ''

	scorelog = ''
	inns = ''
	bowls = ''
	weather = ''
	pitch = ''

	raw = ''
	scorecard = 'scorecard.txt'
	card = []
	fullcard = False
	log = []
	teaminnings = []
	players = ''
	tobat = ''
	folder = ''
	lostovers = 0

class innings:
	def __init__(self, p, t):
		self.name = p.name
		self.player = p
		self.test = t
		self.year = t.year
		p.inns.append(self)

	def form (self):
		if self.test.overcount() % 90 < 6: return 0.9
		else: return 0.9 + min(0.1, self.balls/500) + min(0.1, self.runs/250) - min (0, (200-self.balls)/2000)

	def stats (self):
		if 100 > self.runs >= 50: self.player.fifties +=1
		elif self.runs >= 100: self.player.centuries +=1
		if self.runs >= 200: self.player.doubles +=1
		if self.runs > self.player.HS or (self.runs == self.player.HS and self.player.HSNO == ' ' and self.out == False):
			self.player.HS = self.runs
			if self.out == False: self.player.HSNO = '*'
			else: self.player.HSNO = ' '
		self.test.inns.append(self)

	name = ''
	player = ''
	runs = 0
	balls = 0
	chances = 0
	fours = 0
	sixes = 0
	out = False
	dismissal = ''
	FOW = ''
	scorecard = ''

	year = 0
	test = ''
	opposition = ''

class bowling:
	def __init__(self, p, t):
		self.name = p.name
		self.player = p
		self.test = t
		self.year = t.year
		p.bowls.append(self)

	def bowlformat (self):
		a = str(self.overs).rjust(2)
		b = str(self.maidens).rjust(2)
		c = str(self.runs).rjust(3)
		d = str(self.wickets).rjust(2)

		return '{} - {} - {} - {}'.format(a,b,c,d)

	def stats (self):
		if self.wickets >=5: self.player.fives += 1
		if self.wickets > self.player.BBW or (self.wickets == self.player.BBW and self.runs < self.player.BBR):
			self.player.BBW = self.wickets
			self.player.BBR = self.runs
		if any((self.player == y.player and self.wickets + y.wickets >= 10 and self is not y) for y in self.test.bowls): self.player.tens +=1
		self.test.bowls.append(self)

	name = ''
	player = ''
	opposition = ''
	overs = 0
	balls = 0
	maidens = 0
	runs = 0
	wickets = 0
	chances = 0
	spell = 0
	year = 0
	test = ''

class team:
	def __init__(self):
		self.players, self.active, self.squad, self.xi, self.lastxi, self.tests = [], [], [], [], [], []

	name = ''
	players = []
	active = []
	squad = []
	unav = ''
	captain = ''
	xi = []
	lastxi = []
	lastcapt = ''
	gamecapt = ''
	wk = ''
	inj = ''
	tests = []
	rating = 0

class player:
	def overcount (self):
		self.overs = self.ballsbowled//6
		self.ballsbowled = self.ballsbowled%6

	def stats (self, test):
		self.inns = list(dict.fromkeys(self.inns))
		self.bowls = list(dict.fromkeys(self.bowls))

		self.runs = sum([x.runs for x in self.inns])
		self.outs = sum([x.out for x in self.inns])
		self.balls = sum([x.balls for x in self.inns])
		if self.outs > 0: self.batav = round(self.runs/self.outs, 2)
		else: self.batav = self.runs
		if self.balls > 0: self.batsr = round(100*self.runs/self.balls,1)

		self.ballsbowled = 6*sum([x.overs for x in self.bowls]) + sum([x.balls for x in self.bowls])
		self.wickets = sum([x.wickets for x in self.bowls])
		self.bowlruns = sum([x.runs for x in self.bowls])
		self.maidens = sum([x.maidens for x in self.bowls])

		if self.wickets > 0:
			self.bowlav = round(self.bowlruns/self.wickets, 2)
			self.bowlsr = round(self.ballsbowled/self.wickets, 1)
		if self.ballsbowled > 0:
			self.bowler = round(self.bowlruns/(self.ballsbowled/6), 2)

	def batdesc (self, current):
		if self.end+1 < current: y = '{}-{}'.format(self.debut, self.end)
		else: y = '{}-    '.format(self.debut)
		return ('Age{} {} {} Tests {} runs @{} SR{}{}x200 {}x100 {}x50 HS {}{} Rating{}'.format(str(current-self.dob).rjust(3), y, str(self.games).rjust(3), str(self.runs).rjust(5), "{:0.2f}".format(self.batav).rjust(6), "{:0.1f}".format(self.batsr).rjust(5), str(self.doubles).rjust(2), str(self.centuries).rjust(2), str(self.fifties).rjust(2), str(self.HS).rjust(3),self.HSNO, "{:0.2f}".format(self.batform).rjust(6)))

	def bowldesc (self, current):
		if self.BBR == float('inf'): BB = '-'.center(6)
		else: BB = str(self.BBW).rjust(2) + '-' + str(self.BBR).ljust(3)

		if self.end == 9999: y = '         '
		elif self.end+1 < current: y = '{}-{}'.format(self.debut, self.end)
		else: y = '{}-    '.format(self.debut)
		return ('Age{} {} {} Tests {} wickets @{} {}x5w {}x10w BB{} SR{} ER {} Rating {}'.format(str(current-self.dob).rjust(3), y, str(self.games).rjust(3), str(self.wickets).rjust(3), "{:0.2f}".format(self.bowlav).rjust(6), str(self.fives).rjust(2), str(self.tens).rjust(2), BB, "{:0.1f}".format(self.bowlsr).rjust(5), "{:0.2f}".format(self.bowler).rjust(4), "{:0.2f}".format(self.bowlform).rjust(6)))

	name = ''
	team = ''
	secondteam = ''
	basebat = 0
	basebowl = 500
	bat = 0
	bowl = 500
	batform = 0
	bowlform = 0
	tag = ''
	dob = 0
	first = 0
	last = 0
	age = 0
	debut = ''.center(4)
	end = 9999
	realfirst = 0
	reallast = 0
	sr = 0
	er = 0
	capt = 0

	inns = []
	bowls = []
	games = 0
	captgames = 0
	motm = 0

	runs = 0
	balls = 0
	outs = 0
	batav = 0
	batsr = 0
	fifties = 0
	centuries = 0
	doubles = 0
	HS = 0
	HSNO = ' '

	ballsbowled = 0
	overs = 0
	maidens = 0
	bowlruns = 0
	wickets = 0
	bowlav = float('inf')
	bowler = float('inf')
	bowlsr = float('inf')
	fives = 0
	tens = 0
	BBR = float('inf')
	BBW = 0

	innings = ''
	bowling = ''
	motmscore = 0

if __name__ == "__main__":
	pass