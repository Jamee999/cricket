import pickle
from callcricketnew import player

def run():
	countries = ['England','Australia','South Africa','West Indies','New Zealand','India', 'Pakistan','Sri Lanka','Zimbabwe','Bangladesh','Afghanistan','Ireland']

	players = []
	for i in countries:
		j = ''.join(i.split()).lower()
		with open('{}data.txt'.format(j)) as f:
			for line in f:
				x = line[1:-2]
				x = x.split(',')
				p = player()
				p.name = x[0][1:-1]
				p.bat = float(x[1])
				p.bowl = float(x[2])
				p.tag = x[3][2:-1]
				p.first = int(x[4])
				p.last = int(x[5])
				p.sr = float(x[6])
				p.er = float(x[7])
				p.capt = int (x[8])
				p.team = i
				players.append(p)

	pickle_out = open("players","wb")
	pickle.dump(players, pickle_out)
	pickle_out.close()

	print ('Player data converted and saved.')

if __name__ == "__main__":
	run ()