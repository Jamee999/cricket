from customleague import teamnumber, gamenumber, league
from historical import HistoricalYearsSelect, CountrySelect, histplayers
from callcricketnew import team

def setup (x):
	t = team ()
	t.active = histplayers(x, a, b)
	if x == 'all': 
		x = 'World'
		for i in t.active: i.team = x
	t.name = x
	return t

if __name__ == '__main__':
	print ('Historical league')

	x = teamnumber ()
	t = []
	a, b = 2020, 2020
	for i in range (x):
		[a,b] = HistoricalYearsSelect(a, b)
		z = CountrySelect(a,b)
		c = setup(z)

		for j in t:
			if c.name == j.name:
				c.name = '{} {}'.format(c.name, a)
				for k in c.active:
					k.team = c.name

		t.append(c)
		y = a

	n = gamenumber ()

	league (t, n)