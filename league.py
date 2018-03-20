import random, time, os, pexpect, shutil

print ('')
print ('')

y = 0
Number = 0
Games = 0

while y < 1877 or y > 2018:
    y = input('What year should teams be selected from? ')
    if y == 'all':
        y = 2019
        break
    try:
        y = int(y)
    except:
        print ('Invalid input.')

Teams = ['England', 'Australia', 'South Africa', 'West Indies', 'New Zealand', 'India', 'Pakistan', 'Sri Lanka', 'Zimbabwe', 'Bangladesh']
if y < 2000: #remove teams from ineligible years.
    Teams.remove('Bangladesh')
if y < 1992:
    Teams.remove('Zimbabwe')
if y < 1982:
    Teams.remove('Sri Lanka')
if y < 1952:
    Teams.remove('Pakistan')
if y < 1932:
    Teams.remove('India')
if y < 1930:
    Teams.remove('New Zealand')
if y < 1928:
    Teams.remove('West Indies')
if y < 1889 or (y > 1970 and y < 1992):
    Teams.remove('South Africa')

print (Teams)
delete = ''
while delete != 'go':
    delete = input('Enter the name of a team you want to remove from the league, or type "go" to confirm teams. ')
    if delete in Teams:
        Teams.remove(delete)

Teams.sort(key = lambda x: random.random())

while Games < 1 or Games > 20:
    Games = input('How many times should the teams play each other? ')
    try:
        Games = int(Games)
    except:
        print ('Invalid input.')
        Games = 0

folder = str(input('Input the name of the folder to save scorecards to. '))

try:
    os.mkdir(folder)
except:
    y = y

if y == 2019:
    y = 'all'

print ('')

def game (x,y,z,n):
    cricket = pexpect.spawn('python3 cricket.py')
    time.sleep (0.1)
    cricket.expect("Type 'h' for historical teams, 'c' for custom teams, or 'r' to recreate a real test match. ")
    cricket.sendline ('h')
    time.sleep (0.2)
    cricket.expect("Type 'all' for all-time teams")
    cricket.sendline (n)
    time.sleep (0.1)
    cricket.expect("Select a team")
    cricket.sendline (y)
    time.sleep (0.1)
    cricket.expect("Type 'h' for historical teams, 'c' for custom teams, or 'r' to recreate a real test match. ")
    cricket.sendline ('h' )
    time.sleep (0.2)
    cricket.expect("Type 'all' for all-time teams")
    cricket.sendline (n)
    time.sleep (0.1)
    cricket.expect("Select a team")
    cricket.sendline (z)
    time.sleep (0.1)
    cricket.expect_exact('Enter "slow" to watch the game in over-by-over mode, or anything else to proceed with quicksim.')
    cricket.sendline (' ' )
    time.sleep (0.7)
    cricket.expect('Man of the Match:')
    shutil.copy('scorecard.txt','{}/scorecard{}.txt'.format(folder, x))
    print ('Game {} simulated.'.format(x))

y = str(y)
n = 1
for a in range (Games):
    for i in range (len(Teams)-1):
        for j in range (0, len(Teams)-i-1):
            game (n, Teams[i], Teams[i+j+1], y)
            f=open('{}/scorecard{}.txt'.format(folder, n),'r')
            result = f.readlines()[-3]
            f.close()
            e=open('{}/results.txt'.format(folder),'a')
            e.write('{} v. {} - '.format(Teams[i], Teams[i+j+1]))
            e.write(result)
            e.close()
            print('{} v. {}'.format(Teams[i], Teams[i+j+1]))
            print (result)
            n = n + 1

TotalGames = n
#Team, Games, Wins, Losses, Draws, Innings Wins
Table = []
Results = []

g = open('{}/results.txt'.format(folder),'r')
for line in g:
    Results.append(line)
g.close()

for i in range(len(Teams)):
    Table.append([Teams[i],0,0,0,0,0])
    for j in range(len(Results)):
        if Teams[i] in Results[j]:
            Table[i][1] = Table[i][1] + 1
            if Results[j].count(Teams[i][0]) == 2:
                Table[i][2] = Table[i][2] + 1
                if 'innings' in Results[j]:
                    Table[i][5] = Table[i][5] + 1
            elif 'Drawn' in Results[j] or 'tied' in Results[j]:
                Table[i][4] = Table[i][4] + 1
            else:
                Table[i][3] = Table[i][3] + 1

Table.sort(key=lambda x: x[2]*3.01 + x[4] + x[5], reverse = True)

print('Team            Games  Wins Losses Draws Innings Wins')
e = open('{}/table.txt'.format(folder),'a')
e.write('Team            Games  Wins  Losses  Draws  Innings Wins')
e.write('\n')
for i in range(len(Table)):
    print('{} {}     {}     {}     {}     {}'.format(Table[i][0].ljust(16),Table[i][1],Table[i][2],Table[i][3],Table[i][4],Table[i][5]))
    e.write('{} {}     {}    {}     {}      {}'.format(Table[i][0].ljust(16),str(Table[i][1]).ljust(2),str(Table[i][2]).ljust(2),str(Table[i][3]).ljust(2),str(Table[i][4]).ljust(2),str(Table[i][5]).ljust(2)))
    e.write('\n')
e.close()

print('')
print ('Final:')
game (n, Table[0][0], Table[1][0], y)
f=open('{}/scorecard{}.txt'.format(folder, n),'r')
result = f.readlines()[-3]
f.close()
e=open('{}/results.txt'.format(folder),'a')
e.write('{} v. {} - '.format(Table[0][0], Table[1][0]))
e.write(result)
e.close()
print('{} v. {}'.format(Table[0][0], Table[1][0]))
print (result)

for j in range (1, n):
    scorecard = []
    f = open('{}/scorecard{}.txt'.format(folder,j),'r')
    for line in f:
        scorecard.append(line)
    f.close()

    def batcard (x, y):
        for i in range (x, y):
            n = scorecard[i].rfind('(')
            balls = int(scorecard[i][n+1:-2])
            runs = int(scorecard[i][n-4:n-1])
            if '*+' in scorecard[i]:
                nameandout = scorecard[i][2:n-5].split('  ')
            else:
                nameandout = scorecard[i][1:n-5].split('  ')
            if nameandout[-1] == '':
                nameandout.pop()
            name = nameandout[0]
            dismissal = nameandout[-1]
            dismissal = dismissal.strip()
            if dismissal == 'not out' or dismissal == '':
                outs = 0
            else:
                outs = 1
            g.write('{}, {}, {}, {}'.format(name, outs, runs, balls))
            g.write('\n')

    def breakfind(x, y):
        for i in range (x, y):
            if scorecard[i] == '\n':
                return i
                break

    def bowlcard (x, y):
        for i in range (x, y):
            scorecard[i] = scorecard[i].split('- ')
            scorecard[i][0] = scorecard[i][0].split('  ')
            name = scorecard[i][0][0]
            name = name.strip()
            overs = int(scorecard[i][0][-1])
            maidens = int(scorecard[i][1])
            runs = int(scorecard[i][2])
            wickets = int(scorecard[i][3][:-1])
            g.write('{}, {}, {}, {}, {}'.format(name, overs, maidens, runs, wickets))
            g.write('\n')


    g = open('{}/rawstats.txt'.format(folder),'a')
                    
    batcard (5, 16)
    a = breakfind (19, 30)
    bowlcard (19, a)

    batcard (a+2, a+13)
    b = breakfind (a+16, a+27)
    bowlcard (a+16, b)

    try:
        batcard (b+2, b+13)
        c = breakfind (b+16, b+27)
        bowlcard (b+16, c)
    except:
        continue

    try:
        batcard (c+2, c+13)
        d = breakfind (c+16, c+27)
        bowlcard (c+16, d)
    except:
        continue
                    
    g.close()

f = open('{}/rawstats.txt'.format(folder),'r')
stats = []
for line in f:
    line = line.split(',')
    line[1] = int(line[1])
    line[2] = int(line[2])
    line[3] = int(line[3])
    try:
        line[4] = int(line[4])
    except:
        line = line
    stats.append(line)

batnames = []
bowlnames = []
batstats = []
bowlstats = []

for i in range (len(stats)):
    if len(stats[i]) == 4:
        if stats[i][0] not in batnames:
            batnames.append(stats[i][0])
    else:
        if stats[i][0] not in bowlnames:
            bowlnames.append(stats[i][0])

for j in range (len(batnames)):
    batstats.append([batnames[j],0,0,0])
    for i in range (len(stats)):
        if len(stats[i]) == 4 and stats[i][0] == batstats[j][0]:
            batstats[j][1] = batstats[j][1] + stats[i][1]
            batstats[j][2] = batstats[j][2] + stats[i][2]
            batstats[j][3] = batstats[j][3] + stats[i][3]
    if batstats[j][1] == 0:
        batstats[j][1] = 1


for j in range (len(bowlnames)):
    bowlstats.append([bowlnames[j],0,0,0,0])
    for i in range (len(stats)):
        if len(stats[i]) == 5 and stats[i][0] == bowlstats[j][0]:
            bowlstats[j][1] = bowlstats[j][1] + stats[i][1]
            bowlstats[j][2] = bowlstats[j][2] + stats[i][2]
            bowlstats[j][3] = bowlstats[j][3] + stats[i][3]
            bowlstats[j][4] = bowlstats[j][4] + stats[i][4]

batstats.sort(key=lambda x: x[2], reverse = True)
bowlstats.sort(key=lambda x: x[4], reverse = True)

runssum = 0
wicketssum = 0

g = open('{}/stats.txt'.format(folder),'a')
for i in range (len(batnames)):
    g.write('{} - {} runs @ {}'.format(batstats[i][0], batstats[i][2], (round(batstats[i][2]/batstats[i][1],2))))
    g.write('\n')
    runssum = runssum + batstats[i][2]
    wicketssum = wicketssum + batstats[i][1]
g.close()
print ('')
h = open('{}/stats.txt'.format(folder),'a')

for i in range (len(bowlnames)):
    if bowlstats[i][4] > 0:
        h.write('{} - {} wickets @ {} (ER: {}, SR: {})'.format(bowlstats[i][0], bowlstats[i][4], round((bowlstats[i][3]/bowlstats[i][4]),2), round((bowlstats[i][3]/bowlstats[i][1]),2),round((6*bowlstats[i][1]/bowlstats[i][4]),2)))
        h.write('\n')
h.close()            

for i in range (10):
    print ('{} - {} runs @ {}'.format(batstats[i][0], batstats[i][2], (round(batstats[i][2]/batstats[i][1],2))))
print ('')
for i in range (10):
    print ('{} - {} wickets @ {}'.format(bowlstats[i][0], bowlstats[i][4], round(bowlstats[i][3]/bowlstats[i][4],2)))

print ('')

for i in range (len(batnames)):
    for j in range (len(bowlnames)):
        if bowlstats[j][4] > 0 and batstats[i][1] > 0:
            if batstats[i][0] == bowlstats[j][0]:
                if batstats[i][2]/batstats[i][1] > 35 and batstats[i][1] > 3 and bowlstats[j][3]/bowlstats[j][4] < 35 and bowlstats[j][4] > 8:
                    print ('{} - {} runs @ {}, {} wickets @ {}'.format(batstats[i][0], batstats[i][2], (round(batstats[i][2]/batstats[i][1],2)), bowlstats[j][4], round(bowlstats[j][3]/bowlstats[j][4],2)))

innings = [x for x in stats if len(x) == 4]
bowling = [x for x in stats if len(x) == 5]

innings.sort(key = lambda x: x[2], reverse = True)

print ('')

if innings[0][1] == 1:
    print ('Top score: {} - {}'.format(innings[0][0], innings[0][2]))
else:
    print ('Top score: {} - {}*'.format(innings[0][0], innings[0][2]))

print ('')

bowling.sort(key = lambda x: x[3])
bowling.sort(key = lambda x: x[4], reverse = True)

print ('Best bowling: {} {} - {} - {} - {}'.format(bowling[0][0], bowling[0][1], bowling[0][2], bowling[0][3], bowling[0][4]))

print ('')

print ('Overall: {} runs, {} wickets @ {}.'.format(runssum, wicketssum, (runssum/wicketssum)))

print ('')
print ('')
