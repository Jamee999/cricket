import random, time, copy, os, shutil, datetime
from callcricketnew import test, innings, bowling, player, team, quickorder, listshow, playerwrite
from game import game, setup
from historical import series


def possible():
	a, c = [], []
	with open ('customteams.txt') as g:
		for line in g: a.append(line[:-1])
	n = 0
	for i in a:
		if i == '': c.append(a[n+1])
		n +=1
	return c, a

def find (t, a):
	p = []
	read = False
	for i in a:
		if read == True and i != '': p.append(i)
		if i == t: read = True
		if i == '': read = False
	return p

def playermake (x, t):
	p = player ()
	x = x[2:-3].split(',')
	p.name = x[0][:-1]
	p.team = t.name
	p.bat = float(x[1])
	p.bowl = float(x[2])
	p.tag = x[3][2:-1]
	p.first = int(x[4])
	p.last = int(x[5])
	p.sr = float(x[6])
	p.er = float(x[7])
	p.capt = int(x[8])
	#longdesc (p)
	return p

def load (t, *q):
	c, a = possible()
	t.name = False

	for i in q:
		if i in c:
			c.remove(q)

	while t.name not in c:
		t.name = input('Select a team from: {} -- '.format(listshow(c)))
	p = find (t.name, a)
	for i in p:
		t.active.append(playermake(i,t))

	return t

def getplayers():
	import pickle
	pickle_in = open("players","rb")
	players = pickle.load(pickle_in)
	return players

def make (x):
	p = getplayers()
	while len(x.active) < 11 or add == True:
		n = input("Please enter a player's name. ")
		e = [x for x in p if n == x.name]
		f = [x.name for x in p if n in x.name]
		if len(e) > 1:
			print (e)
		elif len(e) == 1: 
			e[0].team = x.name
			x.active.append(e[0])
			print ('Success - player in database added to team.')
		elif len(e) == 0 and len(f) > 0: 
			print ('Did you mean one of these players?', end= ' ')
			print (listshow(f))
		else: print ('Player not found, please try again.')

		if len(x.active) >= 11:
			add = input("Type 'y' to keep adding players, or any other button to end. ")
			if add == 'y':
				add = True

	with open ('customteams.txt', 'a') as g:
		g.write('\n')
		g.write(str(x.name))
		g.write('\n')
		for i in x.active:
			g.write(playerwrite(i))
			g.write('\n')
	return x

def getcustom (*q):
	o = ''
	while o not in ['l', 'n']: o = input("Type 'l' to load an existing custom team, or 'n' to create a new one. ")
	if o == 'l': 
		x = team()
		t = load (x, q)
	if o == 'n': 
		x = input('Type name of team: ')
		a = team()
		a.name = x
		t = make (a)

	print ()

	return t

		
if __name__ == "__main__":
	q = []
	for i in range(2):
		q.append(getcustom())

	series (q[0].name, q[1].name, q[0].active, q[1].active)



