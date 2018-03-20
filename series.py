import pexpect, time, shutil, os

print ('')
print ('')
print ('Team Selection - historical teams only.')

a = input("Type 'all' for all-time teams, 'random' for a random year, or input a year (or range of years): ")
b = input('Enter the name of the first team in the series: ')
a1 = input("Type 'all' for all-time teams, 'random' for a random year, or input a year (or range of years): ")
c = input('Enter the name of the second team in the series: ')
length = 1 + int(input('How many Test matches should be in the series? '))
folder = str(input('Input the name of the folder to save scorecards to. '))

try:
    os.mkdir(folder)
except:
    folder = folder

print ('')

def game (x, t, t1, y, z):
    cricket = pexpect.spawn('python3 cricket.py')
    time.sleep (0.1)
    cricket.expect_exact("Type 'h' for historical teams, 'c' for custom teams, or 'r' to recreate a real test match. ")
    cricket.sendline ('h')
    time.sleep (0.1)
    cricket.expect_exact("Type 'all' for all-time teams, 'random' for a random year, or input a year (or range of years):")
    cricket.sendline (t)
    time.sleep (0.1)
    cricket.expect("Select a team. The options are: ")
    cricket.sendline (y)
    time.sleep (0.1)
    cricket.expect_exact("Type 'h' for historical teams, 'c' for custom teams, or 'r' to recreate a real test match. ")
    cricket.sendline ('h' )
    time.sleep (0.1)
    cricket.expect_exact("Type 'all' for all-time teams, 'random' for a random year, or input a year (or range of years):")
    cricket.sendline (t1)
    time.sleep (0.1)
    cricket.expect("Select a team. The options are: ")
    cricket.sendline (z)
    time.sleep (0.1)
    cricket.expect_exact('Enter "slow" to watch the game in over-by-over mode, or anything else to proceed with quicksim.')
    cricket.sendline (' ' )
    time.sleep (0.5)
    cricket.expect('Man of the Match:')
    shutil.copy('scorecard.txt','{}/scorecard{}.txt'.format(folder, x))
    print ('Game {} simulated.'.format(x))

for i in range (1, length):
    try:
        game (i, a, a1, b, c,)
        f=open('{}/scorecard{}.txt'.format(folder, i),'r')
        result = f.readlines()[-3]
        f.close()
        e=open('{}/results.txt'.format(folder),'a')
        e.write(result)
        e.close()
        print (result)
    except:
        print ('Invalid inputs! ')
        break

bwins = 0
cwins = 0
results = []
q = open('{}/results.txt'.format(folder),'r+')
q.write('\n')
for line in q:
    results.append(line)
for i in range (len(results)):
    if '{} wins'.format(b) in results[i]:
        bwins = bwins + 1
    elif '{} wins'.format(c) in results[i]:
        cwins = cwins + 1
if bwins > cwins:
    print ('{} wins the series, {} games to {}'.format(b, bwins, cwins))
    q.write('{} wins the series, {} games to {}'.format(b, bwins, cwins))
elif cwins > bwins:
    print ('{} wins the series, {} games to {}'.format(c, cwins, bwins))
    q.write('{} wins the series, {} games to {}'.format(c, cwins, bwins))
else:
    print ('Series drawn, {} wins each.'.format(bwins))
    q.write('Series drawn, {} wins each.'.format(bwins))
q.close()
    

        


for j in range (1, length):
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

for i in range (8):
    print ('{} - {} runs @ {}'.format(batstats[i][0], batstats[i][2], (round(batstats[i][2]/batstats[i][1],2))))
print ('')
for i in range (8):
    print ('{} - {} wickets @ {}'.format(bowlstats[i][0], bowlstats[i][4], round(bowlstats[i][3]/bowlstats[i][4],2)))

for i in range (len(batnames)):
    for j in range (len(bowlnames)):
        if bowlstats[j][4] > 0 and batstats[i][1] > 0:
            if batstats[i][0] == bowlstats[j][0]:
                if batstats[i][2]/batstats[i][1] > 35 and bowlstats[i][1] > 3 and bowlstats[j][3]/bowlstats[j][4] < 35 and bowlstats[j][4] > 8:
                    print ('{} - {} runs @ {}, {} wickets @ {}'.format(batstats[i][0], batstats[i][2], (round(batstats[i][2]/batstats[i][1],2)), bowlstats[i][4], round(bowlstats[i][3]/bowlstats[i][4],2)))

innings = [x for x in stats if len(x) == 4]
bowling = [x for x in stats if len(x) == 5]

innings.sort(key = lambda x: x[2], reverse = True)

print ('')

if innings[0][1] == 1:
    print ('Top score: {} - {}'.format(innings[0][0], innings[0][2]))
else:
    print ('Top score: {} - {}*'.format(innings[0][0], innings[0][2]))


bowling.sort(key = lambda x: x[3])
bowling.sort(key = lambda x: x[4], reverse = True)

print ('Best bowling: {} {} - {} - {} - {}'.format(bowling[0][0], bowling[0][1], bowling[0][2], bowling[0][3], bowling[0][4]))

print ('')

print ('Overall: {} runs, {} wickets @ {}.'.format(runssum, wicketssum, (runssum/wicketssum)))

print ('')
print ('')
