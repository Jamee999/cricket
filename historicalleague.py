from customleague import teamnumber, gamenumber, league
from historical import HistoricalYearsSelect, CountrySelect, histplayers
from callcricketnew import team

def setup (x):
	t = team ()
	t.name = x
	t.active = histplayers(x, a, b)
	return t

if __name__ == '__main__':
	print ('Custom league')

	x = teamnumber ()
	t = []
	a, b = 2020, 2020
	for i in range (x):
		[a,b] = HistoricalYearsSelect(a, b)
		z = CountrySelect(a,b)
		t.append(setup(z))
		y = a

	n = gamenumber ()

	league (t, n)