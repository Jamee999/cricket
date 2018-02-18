import random, time
import datetime


BatAbi = 1 #batsman's ability
BowlAbi = 1 #bowler's ability
BaseRPO = 3
BaseWkRt = ((1757-215)/92749)
Base4Rt = (5495/92749)
Base6Rt = (380/92749)
BaseScrRt = ((47446 - (5495*4) - (380*6)) / 92749)

x = 0

GameOvers = 450 #maximum number of overs in the game

#DataLength = len(Lines)

PercFilter = 100

def YearsInput (x):
    global FirstYear, LastYear, PercFilter, Teams
    Teams = ['England', 'Australia', 'South Africa', 'West Indies', 'New Zealand', 'India', 'Pakistan', 'Sri Lanka', 'Zimbabwe', 'Bangladesh']
    Range = input ('Input a year - or a range of years - for players to be selected from (or select "all"): ')
    if Range == 'random':
        FirstYear = random.choice(range(1877,2018))
        LastYear = FirstYear
        print (FirstYear)
    else:
        if Range == 'same':
            return 'same'
        #FirstYear = 1875
        #LastYear = 2018
        else:
            Range = ''.join(Range.split())
            try:
                if Range == 'all':
                    PercFilter = input ('What percentage of avaliable players should be selected from? ')
                    PercFilter = int(PercFilter)
                    if PercFilter > 100:
                        PercFilter = 100
                    if PercFilter < 5:
                        PercFilter = 5
                    FirstYear = 1877
                    LastYear = 2018
                elif '-' in Range:
                    Range = Range.split('-')
                    Range [0] = int (Range[0])
                    Range [1] = int (Range[1])
                    if Range[0] < Range[1] and Range[0] > 1876 and Range[1] < 2019:
                        FirstYear = int(Range[0])
                        LastYear = int(Range[1])
                    else:
                        print ('Invalid input. ')
                        YearsInput (x)
                else:
                    Range = int(Range)
                    if Range > 1876 and Range < 2019:
                        if Range > 1939 and Range < 1946:
                            FirstYear = 1938
                            LastYear = 1947
                        else:
                            FirstYear = int(Range)
                            LastYear = int(Range)
                    else:
                        print ('Invalid input. ')
                        YearsInput (x)
            except:
                print ('Invalid input. ')
                YearsInput (x)

        if FirstYear < 1877:
            FirstYear = 1877
        if LastYear > 2018:
            LastYear = 2018


print ('Team One')
n = YearsInput (x)
if n == 'same':
    print ('Invalid input. ')
    YearsInput (x)

if LastYear < 1929 and FirstYear > 1913:
    FirstYear = 1913
    LastYear = 1920

if LastYear < 1947 and FirstYear > 1939:
    FirstYear = 1937
    LastYear = 1948

#for i in range(0,DataLength):
#    if Lines[i] == '':
#        Teams.append(Lines[i+1])

def TeamInput (x):
    global Teams
    if LastYear < 2000:
        Teams.remove('Bangladesh')
    if LastYear < 1992:
        Teams.remove('Zimbabwe')
    if LastYear < 1982:
        Teams.remove('Sri Lanka')
    if LastYear < 1952:
        Teams.remove('Pakistan')
    if LastYear < 1932:
        Teams.remove('India')
    if LastYear < 1930:
        Teams.remove('New Zealand')
    if LastYear < 1928:
        Teams.remove('West Indies')
    if LastYear < 1889 or (FirstYear > 1970 and LastYear < 1992):
        Teams.remove('South Africa')
    Valid = 0
    while Valid == 0:
        y = input (str('Select a team to play. The options are: ' + str(Teams) + ' or "random" or "custom". '))
        if y == 'random' or y == 'Random':
            y = random.choice(Teams)
            print (y)
            return y
        elif y == 'custom':
            return 'all'
        elif y in Teams:
            return y
            Valid = 1
        else:
            print ('Not a valid team.')
            print ('')
            TeamInput (x)

Team1Name = TeamInput(x)

PlayersTemp = []
country =  ''.join(Team1Name.split()).lower()
with open(str(str(country) + 'data.txt')) as f:
    for line in f:
        PlayersTemp.append(line[0:-1])

Players = []

if Team1Name == 'all':
    n = 0
    Team1Name = input ("Please enter your custom team's name. ")
    while n < 11:
        PlayerName = input ('Please enter the name of your first player. ')
        for i in range (0, len(PlayersTemp)):
            if PlayerName in PlayersTemp[i]:
                PlayersTemp[i] = PlayersTemp[i][1:-1]
                PlayersTemp[i] = PlayersTemp[i].split(', ')
                PlayersTemp[i][0] = PlayersTemp[i][0][1:-1]
                PlayersTemp[i][1] = float(PlayersTemp[i][1])
                PlayersTemp[i][2] = float(PlayersTemp[i][2])
                PlayersTemp[i][3] = PlayersTemp[i][3][1:-1]
                PlayersTemp[i][4] = int(PlayersTemp[i][4])
                PlayersTemp[i][5] = int(PlayersTemp[i][5])
                PlayersTemp[i][6] = float(PlayersTemp[i][6])
                PlayersTemp[i][7] = float(PlayersTemp[i][7])
                Players.append(PlayersTemp[i])
                n = n+1
                print ('Player in database - added to team.')
            else:
                continue
else:
    for i in range (0, len(PlayersTemp)-1):
        Placeholder = []
        PlayersTemp[i] = PlayersTemp[i][1:-1]
        #print (PlayersTemp[i])
        PlayersTemp[i] = PlayersTemp[i].split(', ')
        #print (PlayersTemp[i])
        PlayersTemp[i][0] = PlayersTemp[i][0][1:-1]
        PlayersTemp[i][1] = float(PlayersTemp[i][1])
        PlayersTemp[i][2] = float(PlayersTemp[i][2])
        PlayersTemp[i][3] = PlayersTemp[i][3][1:-1]
        PlayersTemp[i][4] = int(PlayersTemp[i][4])
        PlayersTemp[i][5] = int(PlayersTemp[i][5])
        PlayersTemp[i][6] = float(PlayersTemp[i][6])
        PlayersTemp[i][7] = float(PlayersTemp[i][7])
        if PlayersTemp[i][5] >= (FirstYear) and PlayersTemp[i][4] <= LastYear and random.random() < (PercFilter/100):
            Players.append(PlayersTemp[i])

def Select (Players):
    global BowlCount, SpinCount
    import random
    from operator import itemgetter
    #print (Players)
    SelectedTeam = []

    OpenCount = 0
    WKCount = 0
    BowlCount = 0
    SpinCount = 0

    Players.sort(key = lambda x: x[1] + 5*(random.random()-random.random()), reverse=True)
    for i in range (0, 3):
        SelectedTeam.append(Players[i])
    Players.pop(0)
    Players.pop(0)
    Players.pop(0)

    Players.sort(key = lambda x: x[2] + 3*(random.random()-random.random()))
    for i in range (0,2):
        SelectedTeam.append(Players[i])
    if Players[0][1] > 25 and Players[1][1] > 25:
        SelectedTeam.append(Players[2])
        Players.pop(0)
    Players.pop(0)
    Players.pop(0)

    for i in range (0, (len(SelectedTeam))):
        if 'WK' in SelectedTeam[i][3]:
            WKCount = WKCount + 1
        if 'Open' in SelectedTeam[i][3]:
            OpenCount = OpenCount+1
            
    if OpenCount + WKCount > 0:
        Players.sort(key = lambda x: x[1] + 5*(random.random()-random.random()), reverse=True)
        for i in range (0, (OpenCount+WKCount)):
            SelectedTeam.append(Players[i])
        for i in range (0, (OpenCount+WKCount)):
            Players.pop(0)

    OpenCount = 0
    WKCount = 0

    for i in range (0, (len(SelectedTeam))):
        if 'WK' in SelectedTeam[i][3]:
            WKCount = WKCount + 1
        if 'Open' in SelectedTeam[i][3]:
            OpenCount = OpenCount+1

    if OpenCount < 2:
        import copy
        Openers = copy.deepcopy(Players)
        for i in range (0, (len(Openers))):
            if 'Open' not in Openers[i][3]:
                Openers[i][1] = Openers[i][1] - 10
        Openers.sort(key = lambda x: x[1] + 5*(random.random()-random.random()), reverse=True)            
        for i in range (0, 2-OpenCount):
            if 'Open' not in Openers[i][3]:
                Openers[i][1] = Openers[i][1] + 10
                Openers[i][3] = Openers[i][3] + 'FillIn'
            SelectedTeam.append(Openers[i])
            for j in range(0, (len(Players)-1)):
                if Players[j][0] == Openers[i][0]:
                    Players.remove(Players[j])
            if 'Bat' not in Openers[i][3] and 'WK' not in Openers[i][3] and 'Part' not in Openers[i][3]:
                BowlCount = BowlCount+1

    WKCount = 0

    for i in range (0, (len(SelectedTeam))):
        if 'WK' in SelectedTeam[i][3]:
            WKCount = WKCount + 1
            WKName = SelectedTeam[i][0]

    if WKCount == 0:
        Keepers = [x for x in Players if 'WK' in x[3]]
        #print (Keepers)
        if len(Keepers) > 0:
            Keepers.sort(key = lambda x: x[1] + 5*(random.random()-random.random()), reverse = True)
            SelectedTeam.append(Keepers[0])
            WKName = Keepers[0][0]
            Players.remove(Keepers[0])
        else:
            Players.sort(key = lambda x: x[1] + 15*(random.random() - random.random()), reverse = True)
            Players[0][3] = Players[0][3] + 'FakeWK'
            SelectedTeam.append(Players[0])
            WKName = Players[0][0]
            Players.remove(Players[0])

    PaceCount = 0

    for i in range (0, len(SelectedTeam)):
        if 'Bat' not in SelectedTeam[i][3] and 'WK' not in SelectedTeam[i][3] and 'Part' not in SelectedTeam[i][3] and SelectedTeam[i][1] < 40:
            BowlCount = BowlCount+1
        if 'Spin' in SelectedTeam[i][3] and 'Part' not in SelectedTeam[i][3]:
            SpinCount = SpinCount + 1
        if ('Fast' in SelectedTeam[i][3] or 'Med' in SelectedTeam[i][3]) and 'Part' not in SelectedTeam[i][3]:
            PaceCount = PaceCount + 1

    def Value (x):
        global BowlCount, SpinCount
        if 'Bat' in x[3] or 'WK' in x[3]:
            return x[1] + 5*(random.random()-random.random())
        elif 'Part' in x[3]:
            if PaceCount < 2 and 'Spin' not in x[3]:
                return (x[1] + (max(0, (50-x[2]))))  + 5*(random.random()-random.random())
            else:
                return (x[1] + (max(0, (50-x[2]))))  + 5*(random.random()-random.random())
        
        else:
            if 'Spin' in x[3] and 'Part' not in x[3]:
                if SpinCount > 0:
                    return (x[1] + (max(0, 48-x[2]) * (100/BowlCount**3)) - (SpinCount+1)**2  + 5*(random.random()-random.random()))
                else:
                    return (x[1] + (max(0, 48-x[2]) * (125/BowlCount**3)) + 5*(random.random()-random.random()))
            else:
                if PaceCount <2:
                    return (x[1] + (max(0, 55-x[2]) * (100/BowlCount**3))  + 5*(random.random()-random.random()))
                else:
                    return (x[1] + (max(0, 48-x[2]) * (100/BowlCount**3))  + 5*(random.random()-random.random()))

    #print (Players)
    n = len(SelectedTeam)
    for i in range (n, 11):
        Players.sort(key = lambda x: Value (x), reverse = True)
        SelectedTeam.append(Players[0])
        Players.pop(0)  
        if 'Bat' not in SelectedTeam[i][3] and 'WK' not in SelectedTeam[i][3] and 'Part' not in SelectedTeam[i][3]:
            BowlCount = BowlCount+1
        if 'Spin' in SelectedTeam[i][3] and 'Part' not in SelectedTeam[i][3]:
            SpinCount = SpinCount + 1
        if 'Fast' in SelectedTeam[i][3] or 'Med' in SelectedTeam[i][3]:
            PaceCount = PaceCount + 1

    def Order (y):
        Lineup = []
        #print (y)
        #print (' ')
        q = y
        for i in q:
            if 'Open' in i[3]:
                i.append(1)
            if 'WK' in i[3]:
                try:
                    i[8] = i[8] - 0.5
                except:
                    i.append(0)
            if 'FillIn' in i[3]:
                i.append(0.7)
            if  'Open' not in i[3] and 'WK' not in i[3] and 'FillIn' not in i[3]:
                i.append(0)

        q = sorted(q, key = itemgetter(8,1), reverse = True)
        Lineup.append(q[0])
        Lineup.append(q[1])
        t = 0
        if q[2][1] > (q[3][1] - 15):
            Lineup.append(q[2])
            t = 1
        q.pop(0)
        q.pop(0)
        if t == 1:
            q.pop(0)

        def Position (x):
            Av = x[1] + 3*(random.random()-random.random())
            if 'Bat' in x[3] or 'Part' in x[3]:
                Av = Av + 10
            return Av
        
        q = sorted (q, key = lambda x: Position (x), reverse = True)
        #print (q)
        for i in range(0,9-t):
            Lineup.append(q[i])
        for j in range (0,11):
            Lineup[j].pop()
            #print (Lineup[j])
        return (Lineup)                  

    #print (SelectedTeam)
    SelectedTeam = Order (SelectedTeam)

    #CapEx = []
    #for i in range(0,10):
    #    d = Players.index(SelectedTeam[i][0])
    #    CapEx.append(Players[d][16])
    #print (CapEx)
        
    def Output (x):
        file = open ('tempteams.txt','w')
        for a in range(0,8):
            for b in range (0,10):
                file.write(str(x[b][a]))
                file.write(', ')
            file.write(str(x[10][a]))
            file.write('\n')
            for i in range (0,11):
                if 'WK' in x[i][3]:
                    WKName = x[i][0]
        Captain = x[2]
        file.write(str(Captain[0]))
        file.write('\n')
        file.write(str((WKName)))
        file.write('\n')
        

    Output (SelectedTeam)




Select (Players)

Lines = []
with open('tempteams.txt') as f:
    for line in f:
        Lines.append(line)
#print (Lines)
Team1 = Lines[0]
Team1 = Team1.replace('\n','')
Team1 = Team1.split(', ')
print ('')
for w in range (0,11):
    Team1[w] = Team1[w].lstrip()
    print (Team1[w])
    time.sleep(0.5)
Team1BatAvs = Lines[1]
Team1BatAvs = Team1BatAvs.replace('\n','')
Team1BatAvs = Team1BatAvs.split(',')
for d in range(0,11):
    Team1BatAvs[d] = float(Team1BatAvs[d])
Team1BowlAvs = Lines[2]
Team1BowlAvs = Team1BowlAvs.replace('\n','')
Team1BowlAvs = Team1BowlAvs.split(',')
for d in range(0,11):
    Team1BowlAvs[d] = float(Team1BowlAvs[d])

Team1Captain = Lines[8]
Team1Captain = Team1Captain.replace('\n','')
Team1WK = Lines[9]
Team1WK = Team1WK.replace('\n','')

Team1Roles = Lines[3]
Team1Roles = Team1Roles.replace('\n','')
Team1Roles = Team1Roles.split(',')
for w in range (0,10):
    Team1Roles[w] = Team1Roles[w].lstrip()

Team1ERs = Lines[7]
Team1ERs = Team1ERs.replace('\n','')
Team1ERs = Team1ERs.split(',')
for d in range(0,11):
    Team1ERs[d] = float(Team1ERs[d])
    if Team1ERs[d] == 0:
        Team1ERs[d] = 3.5

#print (Team1)
#print (Team1BatAvs)
#print (Team1BowlAvs)
#print (Team1Roles)
#print (Team1Captain)
#print (Team1WK)
#print (Team1ERs)

#Teams.remove(Team1Name)

if FirstYear != LastYear:
    Team1Years = (str(FirstYear)) + ' - ' + str(LastYear)
else:
    Team1Years = (str(LastYear))

print ('')

print ('Team Two')
print ('')


Team2Years = YearsInput (x)

if LastYear < 1929 and FirstYear > 1913:
    FirstYear = 1913
    LastYear = 1920

if LastYear < 1947 and FirstYear > 1939:
    FirstYear = 1938
    LastYear = 1948
    
if Team1Years == str(Team2Years):
    Teams.delete(Team1Name)
Team2Name = TeamInput(x)


PlayersTemp = []
country =  ''.join(Team2Name.split()).lower()
with open(str(str(country) + 'data.txt')) as f:
    for line in f:
        PlayersTemp.append(line[0:-1])

Players = []

if Team2Name == 'all':
    n = 0
    Team2Name = input ("Please enter your custom team's name. ")
    while n < 11:
        PlayerName = input ('Please enter the name of your first player. ')
        for i in range (0, len(PlayersTemp)):
            if PlayerName in PlayersTemp[i]:
                PlayersTemp[i] = PlayersTemp[i][1:-1]
                PlayersTemp[i] = PlayersTemp[i].split(', ')
                PlayersTemp[i][0] = PlayersTemp[i][0][1:-1]
                PlayersTemp[i][1] = float(PlayersTemp[i][1])
                PlayersTemp[i][2] = float(PlayersTemp[i][2])
                PlayersTemp[i][3] = PlayersTemp[i][3][1:-1]
                PlayersTemp[i][4] = int(PlayersTemp[i][4])
                PlayersTemp[i][5] = int(PlayersTemp[i][5])
                PlayersTemp[i][6] = float(PlayersTemp[i][6])
                PlayersTemp[i][7] = float(PlayersTemp[i][7])
                Players.append(PlayersTemp[i])
                n = n+1
                print ('Player in database - added to team.')
            else:
                continue
else:
    for i in range (0, len(PlayersTemp)-1):
        Placeholder = []
        PlayersTemp[i] = PlayersTemp[i][1:-1]
        #print (PlayersTemp[i])
        PlayersTemp[i] = PlayersTemp[i].split(', ')
        #print (PlayersTemp[i])
        PlayersTemp[i][0] = PlayersTemp[i][0][1:-1]
        PlayersTemp[i][1] = float(PlayersTemp[i][1])
        PlayersTemp[i][2] = float(PlayersTemp[i][2])
        PlayersTemp[i][3] = PlayersTemp[i][3][1:-1]
        PlayersTemp[i][4] = int(PlayersTemp[i][4])
        PlayersTemp[i][5] = int(PlayersTemp[i][5])
        PlayersTemp[i][6] = float(PlayersTemp[i][6])
        PlayersTemp[i][7] = float(PlayersTemp[i][7])
        if PlayersTemp[i][5] >= (FirstYear) and PlayersTemp[i][4] <= LastYear and random.random() < (PercFilter/100):
            Players.append(PlayersTemp[i])

#print (Players)
Select (Players)

Lines = []
with open('tempteams.txt') as f:
    for line in f:
        Lines.append(line)
#print (Lines)
Team2 = Lines[0]
Team2 = Team2.replace('\n','')
Team2 = Team2.split(', ')
print ('')
for w in range (0,11):
    Team2[w] = Team2[w].lstrip()
    print (Team2[w])
    time.sleep(0.5)
Team2BatAvs = Lines[1]
Team2BatAvs = Team2BatAvs.replace('\n','')
Team2BatAvs = Team2BatAvs.split(',')
for d in range(0,11):
    Team2BatAvs[d] = float(Team2BatAvs[d])
Team2BowlAvs = Lines[2]
Team2BowlAvs = Team2BowlAvs.replace('\n','')
Team2BowlAvs = Team2BowlAvs.split(',')
for d in range(0,11):
    Team2BowlAvs[d] = float(Team2BowlAvs[d])

Team2Captain = Lines[8]
Team2Captain = Team2Captain.replace('\n','')
Team2WK = Lines[9]
Team2WK = Team2WK.replace('\n','')

Team2Roles = Lines[3]
Team2Roles = Team2Roles.replace('\n','')
Team2Roles = Team2Roles.split(',')
for w in range (0,10):
    Team2Roles[w] = Team2Roles[w].lstrip()

Team2ERs = Lines[7]
Team2ERs = Team2ERs.replace('\n','')
Team2ERs = Team2ERs.split(',')
for d in range(0,11):
    Team2ERs[d] = float(Team2ERs[d])
    if Team2ERs[d] == 0:
        Team2ERs[d] = 3.5

#print (Team2)
#print (Team2BatAvs)
#print (Team2BowlAvs)
#print (Team2Roles)
#print (Team2Captain)
#print (Team2WK)

Team1BatAbi = []
Team1BowlAbi = []
for i in range(0,11):
    Team1BatAbi.append((Team1BatAvs[i]/30))
    Team1BowlAbi.append((Team1BowlAvs[i]/30))

Team2BowlAbi = []
Team2BatAbi = []
for i in range(0,11):
    Team2BatAbi.append((Team2BatAvs[i]/30))
    Team2BowlAbi.append(Team2BowlAvs[i]/30)
    
if FirstYear != LastYear:
    Team2Years = (str(FirstYear)) + ' - ' + str(LastYear)
else:
    Team2Years = (str(LastYear))

if Team1Name == Team2Name:
    Team1Name = str(str(Team1Name) + ' ' + str(Team1Years))
    Team2Name = str(str(Team2Name) + ' ' + str(Team2Years))




print (' ')
delay = input ('Enter "slow" to watch the game in over-by-over mode, or anything else to proceed with quicksim. ')
if delay == 'slow':
    delay = 1
else:
    delay = 0





Header = open('scorecard.txt','w')

if Team1Name == Team2Name:
    Team1Name = str(str(Team1Name) + ' ' + str(Team1Years))
    Team2Name = str(str(Team2Name) + ' ' + str(Team2Years))
    Header.write(str(str(Team1Name) + ' vs. ' + str(Team2Name))) 
else:  
    Header.write(str(str(Team1Name) + ' (' + str(Team1Years) + ') vs. ' + str(Team2Name) + ' (' + str(Team2Years) + ')'))
Header.write('\n')
Header.close()

print (' ')
print (str(str(Team1Name) + ' vs. ' + str(Team2Name)))

MOM = [ ]
for i in range (0,11):
    MOMTemp = [Team1[i],0]
    MOMTemp2 = [Team2[i],0]
    MOM.append(MOMTemp)
    MOM.append(MOMTemp2)

#print (MOM)


def MakeCard (x):
    x = 0
    global Team1
    card =[
    ['name','runs','balls faced','out?','dismissal','fours','sixes'],
    [],
    [],
    [],
    [],
    [],
    [],
    [],
    [],
    [],
    [],
    []
        ]
    k = 0
    for i in Team1:
        card[(k + 1)].extend([i,0,0,0,'',0,0])
        k = k +  1
    return (card)

def MakeBowlCard (x):
    x = 0
    global Team2
    card =[
    ['name','overs','maidens','runs','wickets'],
    [],
    [],
    [],
    [],
    [],
    [],
    [],
    [],
    [],
    [],
    [],
    ['placeholder',0,0,0,0]
        ]
    k = 0
    for i in Team2:
        card[(k + 1)].extend(['',0,0,0,0])
        k = k +  1
    return (card)    

def RunStats (x):
    global card
    global Bat1
    global Bowl1
    for i in range (0,12):
        if card[i][0] == Bat1:
            card[i][1] = card[i][1] + x
            break

def BallStats (x):
    global card
    global Bat1
    global Bowl1
    for i in range (0,12):
        if card[i][0] == Bat1:
            card[i][2] = card[i][2] + x
            break

def OverStats (x):
    global BowlCard
    global Bowl1
    for i in range (0,12):
        if BowlCard[i][0] == x:
            BowlCard[i][1] = BowlCard[i][1] + 1
            break
        if BowlCard[i][0] == '':
            BowlCard[i][0] = x
            BowlCard[i][1] = 1
            break
        
def MaidenStats (x):
    global BowlCard
    for i in range (0,12):
        if BowlCard[i][0] == x:
            BowlCard[i][2] = BowlCard[i][2] + 1
            break

def BowlRunsStats (x):
    global BowlCard
    global Bowl1
    for i in range (0, 12):
        if BowlCard [i][0] == Bowl1:
            BowlCard[i][3] = (BowlCard[i][3] + x)
            break

def BowlWicketStats (x):
    global BowlCard
    for i in range (0,12):
        if BowlCard[i][0] == x:
            BowlCard[i][4] = (BowlCard[i][4] + 1)
            break

x = 0

def coin (x,y):
    rand = random.random()
    if rand > 0.5:
        return x
    else:
        return y

def toss (x):
    global Team1Name 
    global Team2Name
    global Team1
    global Team2
    global Team2Captain
    global Team1Captain
    global Team1WK
    global Team2WK
    global Team1BatAbi
    global Team2BatAbi
    global Team1BatAvs
    global Team2BatAvs
    global Team1BowlAbi, Team1BowlAvs, Team2BowlAbi, Team2BowlAvs, Team1Roles, Team2Roles, Results, Team1ERs, Team2ERs

    x = x
    outcome = coin (Team1Name, Team2Name)
    Results = open('scorecard.txt', 'a')
    print (str(outcome + ' has won the toss.'))
    Results.write((str(outcome + ' has won the toss.')))
    Results.write('\n')
    rand = random.random()
    if outcome == Team1Name and rand > 0.2:
        print( str(Team1Captain + ' has elected to bat first.'))
        Results.write(str(Team1Captain + ' has elected to bat first.'))
    elif outcome == Team1Name and rand < 0.2:
        print( str(Team1Captain + ' has elected to field first.'))
        Results.write(str(Team1Captain + ' has elected to bat first.'))
        Team1Name, Team2Name = Team2Name, Team1Name
        Team1, Team2 = Team2, Team1
        Team1Captain, Team2Captain = Team2Captain, Team1Captain
        Team1WK, Team2WK = Team2WK, Team1WK
        Team1BatAbi, Team2BatAbi = Team2BatAbi, Team1BatAbi
        Team1BatAvs, Team2BatAvs = Team2BatAvs, Team1BatAvs
        Team1BowlAvs, Team2BowlAvs = Team2BowlAvs, Team1BowlAvs
        Team1Roles, Team2Roles = Team2Roles, Team1Roles
        Team1ERs, Team2ERs = Team2ERs, Team1ERs
    elif outcome == Team2Name and rand > 0.2:
        print( str(Team2Captain + ' has elected to bat first.'))
        Results.write(str(Team2Captain + ' has elected to bat first.'))
        Team1Name, Team2Name = Team2Name, Team1Name
        Team1, Team2 = Team2, Team1
        Team1Captain, Team2Captain = Team2Captain, Team1Captain
        Team1WK, Team2WK = Team2WK, Team1WK
        Team1BatAbi, Team2BatAbi = Team2BatAbi, Team1BatAbi
        Team1BatAvs, Team2BatAvs = Team2BatAvs, Team1BatAvs
        Team1BowlAbi, Team2BowlAbi = Team2BowlAbi, Team1BowlAbi
        Team1BowlAvs, Team2BowlAvs = Team2BowlAvs, Team1BowlAvs
        Team1Roles, Team2Roles = Team2Roles, Team1Roles
        Team1ERs, Team2ERs = Team2ERs, Team1ERs
    else:
        print( str(Team2Captain + ' has elected to field first.'))
        Results.write(( str(Team2Captain + ' has elected to field first.')))
    Results.write('\n')
    Results.write('\n')
    print ('')
    Results.close()

x = 0
toss (x)

Bat1 = Team1[0]
Bat2 = Team1[1]

Bowl1 = Team2[9]
Bowl2 = Team2[10]

BatTeam = Team1Name
BowlTeam = Team2Name

Score = 0
Wickets = 0
TotalOvers = 0

GameScores = []
FallOfWicket = [0]

Innings = 0


def ball (x):
    rand = random.random()
    global RunsOver
    global WicketsOver
    global Bat1
    global Bowl1
    global card
    global BowlCard
    global Team1, Team2
    global Team1BatAbi, Team2BowlAbi, Team2ERs
    global BaseWkRt
    global Base6Rt
    global Base4Rt
    global BaseScrRt
    global TotalOvers, OverCount
    global Team1Roles, Team2Roles
    global det, AggFactor

    for i in range (0, 11):
        if Bowl1 == Team2[i]:
            Bowl1Role = Team2Roles[i]
            break
    det = 1
    Day = -(-(TotalOvers+OverCount)//90)
    if 'Spin' in Bowl1Role:
        if Day == 1:
            det = 1.5
        elif Day == 2:
            det = 1.4
        elif Day == 3:
            det = 1.1
        elif Day == 4:
            det = 0.7
        else:
            det = 0.5
    else:
        if Day == 1:
            det = 1.2
        if Day == 2:
            det = 1.1
        if Day == 3:
            det = 1
        if Day == 4:
            det = 0.9
        if Day == 5:
            det = 0.8


    if ('Fast' in Bowl1Role or 'Med' in Bowl1Role) and (OverCount % 80) < 10:
        det = det * 0.9

    Position = Team1.index(Bat1)
    if (Bat1 == Team1[0] or Bat1 == Team1[1]) and 'FillIn' in Bat1:
        BatAbi = Team1BatAbi[Position] - (1/3)
    else:
        BatAbi = Team1BatAbi[Position]

    Form = 0.75 + min(0.15, (card[Position+1][2]/300)) + min(0.15,(card[Position+1][1]/100)) + min(0, ((200-card[Position+1][2])/1000))
    if ((TotalOvers+OverCount) % 90) < 6:
        Form = min(Form, 0.8)
    
    #print (Form, det, AggFactor)

    BowlPosition = Team2.index(Bowl1)
    BowlER = Team2ERs[BowlPosition] * 2
    BowlAbi = Team2BowlAbi[BowlPosition] / BowlER
    
    AdjustedWkRt = BaseWkRt * (1/(BatAbi**0.8)) * (1/(BowlAbi)) * (1/(det**0.5)) * (1/Form**0.5) *AggFactor * (min(1, AggFactor))
    Adjusted6Rt = Base6Rt * (BatAbi**0.2) * BowlER * (det**0.5) * (Form**0.5) * AggFactor
    Adjusted4Rt = Base4Rt * (BatAbi**0.2) * BowlER * (det**0.5) * (Form**0.5) * AggFactor
    AdjustedScrRt = BaseScrRt * (BatAbi**0.2) * BowlER * (det**0.5) * (Form**0.5) * AggFactor
    
    BallStats(1)
    if rand < AdjustedWkRt:
        WicketsOver = WicketsOver + 1
        BowlWicketStats (Bowl1)
        return 'WICKET!!!'
    
    elif rand < (AdjustedWkRt + Adjusted6Rt):
        RunsOver = RunsOver + 6
        RunStats (6)
        return '6 runs!!'
    
    elif rand < (AdjustedWkRt + Adjusted6Rt + Adjusted4Rt):
        RunsOver = RunsOver + 4
        RunStats (4)
        return '4 runs!'
    
    elif rand < (AdjustedWkRt + Adjusted6Rt + Adjusted4Rt + AdjustedScrRt):
        a = random.random()
        if a > 0.25:
            RunsOver = RunsOver + 1
            RunStats (1)
            return '1 run.'
        elif a > 0.05:
            RunsOver = RunsOver + 2
            RunStats (2)
            return '2 runs.'
        else:
            RunsOver = RunsOver + 3
            RunStats (3)
            return '3 runs.'
    elif rand < (AdjustedWkRt + Adjusted6Rt + Adjusted4Rt + AdjustedScrRt + 0.025):
        return 'Chance!'
        # RUNS PER BALL IS TOO HIGH - added in 2s and 3s, but the prob is still calculated on the basis of BaseScrRt being all singles.
        
    else:
        return 'No run.'

#  2017 only    Mat	Inns	NO	Runs	HS	Ave	BF	SR	100	50	0	4s	6s	
# 	191	47	1757	215	47446	244*	30.76	92749	51.15	92	228	173	5495	380

def ChangeBatsman (x):
    global Bat1
    global Team1
    global Wickets
    global WicketsOver
    if (Wickets+WicketsOver) == 10:
        return Bat1
    x = x
    NextBat = Team1[(Wickets+WicketsOver+1)]
    print (' ')
    print (str('New Batsman: ' + str(NextBat)))
    print (' ')
    return NextBat
    

def MakeSpellCount (x):
    global Team2
    SpellCount = [
    ['name','overs in current spell'],
    [],
    [],
    [],
    [],
    [],
    [],
    [],
    [],
    [],
    [],
    []
        ]
    k = 1
    for i in Team2:
        SpellCount[k].extend([i,0])
        k = k +  1
    return SpellCount



FatigueList = []

def second_smallest(numbers):
    a1, a2 = float('inf'), float('inf')
    for x in numbers:
        if x <= a1:
            a1, a2 = x, a1
        elif x < a2:
            a2 = x
    return a2

def BowlChoice (x):
    global Bowl1
    global Bowl2
    global Team2
    global SpellCount
    global OverCount, TotalOvers
    global Team2WK
    global GameOvers
    global Team2BowlAvs
    global FatigueList
    global BowlCard
    global Team2Roles
    global OverCount, FallOfWicket
    a = range (0,11)
    y = 10

    det = 1
    Day = -(-(TotalOvers+OverCount)//90)
    if Day == 1:
        det = 1.2
    elif Day == 2:
        det = 1.15
    elif Day == 3:
        det = 1.05
    elif Day == 4:
        det = 0.9
    else:
        det = 0.7

    if Innings > 1 and OverCount == 0:
        Bowl1 = ''
        Bowl2 = ''
    
    for i in range (0,12):
        if SpellCount[i][0] == Bowl2 and OverCount != 0:
            SpellCount[i][1] = SpellCount[i][1] + 1           

    if OverCount % 80 < 2:
        import copy
        OpenAvs = copy.deepcopy(Team2BowlAvs)
        for i in range(0,11):
            if 'Spin' in Team2Roles[i] or 'Bat' in Team2Roles[i]:
                OpenAvs[i] = OpenAvs[i] + 50

    if OverCount == 0:
        j = min(OpenAvs)
        k = OpenAvs.index(j)
        return Team2[k]
    elif OverCount == 1:
        j = second_smallest(OpenAvs)
        k = OpenAvs.index(j)
        return Team2[k]
    for i in a:
        if Team2[i] == Bowl1:
            y = i
        if BowlCard[i][0] == Bowl1:
            BowlCardNo = i
        if OverCount < 2:
            BowlCardNo = 2
            
    if BowlCard[BowlCardNo][3] != 0:
        if (BowlCard[BowlCardNo][3]/BowlCard[BowlCardNo][1]) > 4:
            ExcessRPO = BowlCard[BowlCardNo][3] - 4*BowlCard[BowlCardNo][1]
        else:
            ExcessRPO = 0
    else:
        ExcessRPO = 0

    if 'Fast' not in Team2Roles[y] and 'Part' not in Team2Roles[y] and 'Bat' not in Team2Roles[y]:    
        z = SpellCount[(y+1)][1] - BowlCard[BowlCardNo][4] + (ExcessRPO)/4
    else:
        z = SpellCount[y+1][1] - BowlCard[BowlCardNo][4] + (ExcessRPO)/4
    if 'Part' in Team2Roles[y]:
        z = z+2
    if 'Bat' in Team2Roles[y]:
        z = z+3
    z = z**2
    if OverCount % 80 < 2:
        Bowl1 = ''
        z = 100
    if 'Fast' in Team2Roles[y]:
        z = 1.5*z
    
    #print (z)
    prob = (int(z)/100)
    if random.random() < prob:
        t = 0
        q = 11
        while t == 0:
            for i in range (0,10):
                if Team2[q-1] == BowlCard[i][0]:
                    CardNo = i
                    break
                else:
                    CardNo = 12

                # print (q, CardNo)
                        
                        
                         
                if BowlCard[CardNo][1] != 0:
                    if (BowlCard[CardNo][3]/BowlCard[CardNo][1]) > 4:
                        ExcessRPO = BowlCard[CardNo][3] - 4*BowlCard[CardNo][1]
                    else:
                        ExcessRPO = 0
                else:
                    ExcessRPO = 0
                b = random.random()
                if 'Fast' in Team2Roles[q-1]:
                    d = Team2BowlAvs[(q-1)] + (FatigueList.count((Team2[(q-1)]))**2) + ExcessRPO - 2*BowlCard[CardNo][4] + 5*SpellCount[q][1]
                else:
                    d = Team2BowlAvs[(q-1)] + ((FatigueList.count((Team2[(q-1)]))**2)/5) + ExcessRPO - 2*BowlCard[CardNo][4] + 2*SpellCount[q][1]
                if 'Part' in Team2Roles[q-1]:
                    d = d+20
                if 'Bat' in Team2Roles[q-1]:
                    d = d+50
                if (OverCount % 80) < 15 and 'Spin' in Team2Roles[q-1]:
                    d = d+50
                elif (OverCount % 80) < 25 and 'Spin' in Team2Roles[q-1]:
                    d = d+25
                if Team2[q-1] == Bowl1:
                    d = 500
                if OverCount < 50 and ('Part' in Team2Roles[q-1] or 'Bat' in Team2Roles[q-1]):
                    d = d+20
                Partnership = (Score+RunsOver) - FallOfWicket[-1]
                if Partnership > 150 and ('Part' in Team2Roles[q-1] or 'Bat' in Team2Roles[q-1]):
                    d = d-20
                if 'Spin' in Team2Roles[q-1]:
                    d = d*det
                # print (d)

                if d <= 40:
                    c = 0.5 + ((40-d)/50)
                elif d <= 80:
                    c = 0.5 - ((d-40)/100)
                else:
                    c = 0.1 - ((d-80)/1500)
                # print (c, d)


                if b < c and SpellCount[q][0] != Bowl2 and SpellCount[q][0] != Team2WK:
                    t = 1
                    if SpellCount[q][0] !=Bowl1:
                        print (str('New Bowler: ') + str(SpellCount[q][0]))
                        print (' ')
                        SpellCount[(y+1)][1] = 0
                    return SpellCount[q][0]
                if q > 1:
                    q = q-1
                else:
                    q = 11
    else:
        return Bowl1



def Wicket (x,y):
    global Team1
    global Team2
    global Team2WK
    global Team2Roles
    global card, BowlCard
    name = Team1.index(x) + 1
    card[name][3] = 1
    rand = random.random()
    for i in range(0,11):
        if y == BowlCard[i][0]:
            PlayerNumber = i
            break
    if rand < 0.2143:
        card[name][4] = str('b. ' + str(y))
        LastWicket[2] = str('b. ' + str(y))
        return str('b. ' + str(y))
    elif rand < 0.3573:
        card[name][4] = str('lbw. b. ' +str(y))
        LastWicket[2] = str('lbw. b. ' +str(y))
        return str('lbw. b. ' +str(y))
    elif rand < 0.52:
        card[name][4] = str('c. ' + str(Team2WK) + ' b. ' +str(y))
        LastWicket[2] = str('c. ' + str(Team2WK) + ' b. ' +str(y))
        return str('c. ' + str(Team2WK) + ' b. ' +str(y))                
    elif rand < 0.9065:
        Fielder = random.choice(Team2)
        if Fielder != y:
            card[name][4] = str('c. ' + str(Fielder) + ' b. ' + str(y))
            LastWicket[2] = str('c. ' + str(Fielder) + ' b. ' + str(y))
            return str('c. ' + str(Fielder) + ' b. ' + str(y))
        else:
            card[name][4] = str('c. & b. ' +str(y))
            LastWicket[2] = str('c. & b. ' +str(y))
            return str('c. & b. ' +str(y))
    elif rand < 0.9568: #adjusted by +0.01
        if random.random() > 0.9 and ('Med' in Role or 'Spin' in Role):
            card[name][4] = str('st. ' + str(Team2WK) + ' b. ' +str(y))
            LastWicket[2] = str('st. ' + str(Team2WK) + ' b. ' +str(y))
            return str('st. ' + str(Team2WK) + ' b. ' +str(y))
        else:
            Fielder = random.choice(Team2)
            if Fielder != y:
                card[name][4] = str('c. ' + str(Fielder) + ' b. ' + str(y))
                LastWicket[2] = str('c. ' + str(Fielder) + ' b. ' + str(y))
                return str('c. ' + str(Fielder) + ' b. ' + str(y))
            else:
                card[name][4] = str('c. & b. ' +str(y))
                LastWicket[2] = str('c. & b. ' +str(y))
                return str('c. & b. ' +str(y))
    elif rand < 0.9919: #adjusted by +0.01
        Fielder = random.choice(Team2)
        card[name][4] = str('run out ('+str(Fielder) + ')')
        LastWicket[2] = str('run out ('+str(Fielder) + ')')
        BowlCard[(PlayerNumber)][4] = (BowlCard[(PlayerNumber)][4] - 1)
        return str('run out ('+str(Fielder) + ')')
    else:
        card[name][4] = str('hit wicket b. ' + str(y))
        LastWicket[2] = str('hit wicket b. ' + str(y))
        return str('hit wicket b. ' + str(y))        


def milestone (x):
    global RunsOver, WicketsOver, card, Bat1, FallOfWicket, Score, Wickets
    for i in range(1,12):
        if Bat1 == card[i][0]:
            PlayerNo = i
            break
    if x == '1 run.':
        j = 1
    elif x == '2 runs.':
        j = 2
    elif x == '3 runs.':
        j = 3
    elif x == '4 runs!':
        j = 4
    elif x == '6 runs!!':
        j = 6
    else:
        j = 0

    BatsmanScore = card[PlayerNo][1]
    if (BatsmanScore % 50) < j:
        print (' ')
        print (str('Milestone: ' + str(card[PlayerNo][0]) + ' ' + str(card[PlayerNo][1]) + '* (' + str(card[PlayerNo][2]) + ')'))
        print (' ')

    Partnership = (Score+RunsOver) - FallOfWicket[-1]
    if (Partnership % 50) < j:
        print (' ')
        print (str('Partnership: ' + str(Partnership) + ' (' +str(LastWicket[3]) + ' balls)'))
        if Wickets > 0:
            print ( str( 'Last Wicket: '+ str(LastWicket[0]) + '/' + str(Wickets)+' - ' + str(LastWicket[1]) + ' ' + str (LastWicket[2]) + ' '+ str(LastWicket[4])))
        print (' ')


# ['Score at Last Wicket', 'Last Man Out', 'How Last Man Out', 'Balls Since Last Wicket'

LastWicket = [0,'','',0,'']

def declare (x):
    global card, Bat1, Bat2, Innings, Score, GameScores, TotalOvers, GameOvers, OverCount
    import random
    a = 0
    b = 0
    for i in range (1, 11):
        if Bat1 == card[i][0]:
            a = card[i][1]
        if Bat2 == card[i][0]:
            b = card[i][1]
    if (a % 100 > 89) or (b % 100 > 89):
        return 'continue'
    if Innings == 0 and (Score > 500 or OverCount > 150 ) and random.random() < (Score/50000):
        print ('')
        print ('Innings declared.')
        return 'declare'
    if Innings == 1 and Score > 500 and (Score-GameScores[1] > -50) and random.random() < 0.1:
        print ('')
        print ('Innings declared.')
        return 'declare'
    if Innings == 1 and ((Score/GameScores[1]) > 2) and OverCount > 100 and random.random() < 0.02:
        print ('')
        print ('Innings declared.')
        return 'declare'
    if Innings == 2 and ((3*(GameOvers-TotalOvers-OverCount)) + 50 < (GameScores[1]+Score-GameScores[5])) and random.random() < 0.2 and FollowOn == False:
        print ('')
        print ('Innings declared.')
        return 'declare'
    
  
def over (x):
    global Bowl1
    global Bowl2
    global Bat1
    global Bat2
    global Wickets
    global RunsOver
    global WicketsOver
    global Wickets
    global Team1
    global BowlCard
    global card
    global Team2
    global Score
    global Innings
    global GameScores
    global FatigueList, LastWicket, dec, AggFactor
    global GameOvers, TotalOvers, OverCount

    c = 0
    RunsOver = 0
    WicketsOver = 0
    
    r = BowlChoice (x)
    Bowl1 = r
    BowlName = Bowl1
    o = Team2.index(Bowl1)
    print (str('Over ' + str (x) + ': '+str(Bowl1) + ' to bowl. ' +str((SpellCount[o+1][1])) + ' overs in spell so far.'))
    OverStats (Bowl1)
    FatigueList.append(Bowl1)
    if len(FatigueList) > 25:
        FatigueList.pop(0)

    AggFactor = 1
    if Innings < 3:
        if Score > 400:
            AggFactor = 1 + (Score-400)/500
        if Wickets > 1 and (Score/Wickets) < 15:
            AggFactor = 0.8
    elif Innings == 2:
        if Score + GameScores[1] - GameScores[5] > 250:
            AggFactor = 1 + (Score-250)/500
    else:
        Target = (GameScores[1]+GameScores[9]-GameScores[5]+1)
        RemainingOvers = (GameOvers-TotalOvers-OverCount)
        if RemainingOvers == 0:
            RemainingOvers = 1
        if (Target-Score)/RemainingOvers > 6 and RemainingOvers > 15:
            AggFactor = 0.7
        if Wickets > 6 and Target-Score > 50:
            AggFactor = 0.7
        if (Target-Score)/RemainingOvers < (10-Wickets) and RemainingOvers < 50:
            AggFactor = 1+(10-Wickets)/10

    while c < 6:
        dec = 0
        y = (ball (c))
        print (str('Ball ' +str(c+1)+ ': ' +str(Bowl1) + ' to ' + str (Bat1) + ': ' +str(y)))
        milestone (y)
        LastWicket[3] = LastWicket[3] + 1
        if y == 'WICKET!!!' and (Wickets+WicketsOver) <= 9:
            x = int(Wickets + 2)
            
            b = range(1,11)
            for i in b:
                if card[i][0] == Bat1:
                    z = i
            Dismissal = Wicket (Bat1, Bowl1)
            print (' ')
            print (str(card[z][0] + ' ' + str(Dismissal) + ' ' + str(card[z][1]) + ' (' + str(card[z][2]) + ')'))
            Partnership = (Score+RunsOver) - FallOfWicket[-1]
            print (str('Partnership: ' + str(Partnership) + ' (' +str(LastWicket[3]) + ' balls)'))
            print (str(str(BatTeam)+' ' +str(Score+RunsOver)+'/' + str(Wickets+WicketsOver)))
            if (Wickets+WicketsOver) > 1:
                FallOfWicket.append(Score+RunsOver)
            elif (Wickets+WicketsOver) == 1:
                FallOfWicket[0] = (Score+RunsOver)
            LastWicket[0] = (Score+RunsOver)
            LastWicket[1] = Bat1
            LastWicket[3] = 0
            for i in range (0,11):
                if card[i][0] == Bat1:
                    #print (card)
                    LastWicket[4] = card[i][1]
                    break
            if declare(x) == 'declare':
                c = 6
                dec = 1
            
            Bat1 = ChangeBatsman (x)
            
        if y == 'WICKET!!!' and (Wickets+WicketsOver) > 9:
            print ('')
            b = range(1,12)
            for i in b:
                if card[i][0] == Bat1:
                    z = i
            Dismissal = Wicket (Bat1, Bowl1)
            print (str(card[z][0]  + ' ' + str(Dismissal) + ' ' + str(card[z][1]) + ' (' + str(card[z][2]) + ')'))
            Partnership = (Score+RunsOver) - FallOfWicket[-1]
            print (str('Partnership: ' + str(Partnership) + ' (' +str(LastWicket[3]) + ' balls)'))

            FallOfWicket.append(Score+RunsOver)
            print ('')
            print ('All Out.')
            print ('')
            break
        c = c + 1
        if y == '1 run.' or y == '3 runs.':
            Bat1, Bat2 = Bat2, Bat1

        if Innings == 3 and (int(Score+RunsOver)+GameScores[5]) > ((GameScores[1] + GameScores[9])):
            c = 6
        import time
        time.sleep(delay/10)


    if RunsOver == 0:
        MaidenStats (Bowl1)
    BowlRunsStats (RunsOver)

    Score = Score + RunsOver
    Wickets = Wickets + WicketsOver

    if Wickets  != 10:
        if WicketsOver == 0:
            print (str(str(RunsOver)+ ' runs from the over. ' +str(BatTeam)+' ' +str(Score)+'/' + str(Wickets)+ ' after ' +str(x) + ' overs. (' +str(round((Score/(OverCount+1)),1)) + ' RPO)'))
        elif WicketsOver == 1:
            print (str(str(RunsOver)+ ' runs and ' +str(WicketsOver)+ ' wicket from the over. ' +str(BatTeam)+' ' +str(Score)+'/' + str(Wickets)+ ' after ' +str(OverCount) + ' overs. (' +str(round((Score/(OverCount+1)),1)) + ' RPO)'))
        else:
            print (str(str(RunsOver)+ ' runs and ' +str(WicketsOver)+ ' wickets from the over. ' +str(BatTeam)+' ' +str(Score)+'/' + str(Wickets)+ ' after ' +str(OverCount) + ' overs. (' +str(round((Score/(OverCount+1)),1)) + ' RPO)'))
    # print (FallOfWicket)

    if Wickets > 0:
        print ( str( 'Last Wicket: '+ str(LastWicket[0]) + '/' + str(Wickets)+' - ' + str(LastWicket[1]) + ' ' + str (LastWicket[2]) + ' '+ str(LastWicket[4])))

    a = range (1,12)
    for i in a:
        if BowlCard[i][0] == BowlName:
            print (str(str(BowlName) + ' ' +str(BowlCard[i][1]) + ' - ' +str(BowlCard[i][2]) + ' - ' +str(BowlCard[i][3]) + ' - ' + str(BowlCard[i][4])))
            break
        
    Bowl1, Bowl2 = Bowl2, Bowl1
    Bat1, Bat2 = Bat2, Bat1
    BowlName = Bowl1


    if (len(Bat1) > len(Bat2)):
        LongerName = len(Bat1)
    else:
       LongerName = len(Bat2)
        
    for i in a:
        if card[i][0] == Bat1 and Wickets != 10:
            NameFormat = Bat1.ljust(LongerName)
            RunsFormat = str(card[i][1]).rjust(3)
            BallsFormat = str('(' +str(card[i][2]) +')').rjust(5)
            print (str(NameFormat + ' - ' + RunsFormat + '* ' + BallsFormat))
        if card[i][0] == Bat2 and Wickets != 10:
            NameFormat = Bat2.ljust(LongerName)
            RunsFormat = str(card[i][1]).rjust(3)
            BallsFormat = str('(' +str(card[i][2]) +')').rjust(5)
            print (str(NameFormat + ' - ' + RunsFormat + '* ' + BallsFormat))
    if Innings == 1:
        print ()
        print(str(str(GameScores[0]) + ' ' + str(GameScores[1]) + '/' + str(GameScores[2]) + ' [' + str(GameScores[3]) +']' ))
        print(str(BatTeam)+' ' +str(Score)+'/' + str(Wickets)+ ' [' +str(OverCount) + ']')
        if (Score > GameScores[1]):
            print(str((BatTeam) + ' leads by ' + str((Score-GameScores[1])) + ' runs.'))
        elif (GameScores[1] > Score):
            print(str((BatTeam) + ' trails by ' + str((GameScores[1]-Score)) + ' runs.'))
        else:
            print('Scores level.')

    if Innings == 2:
        print ()
        print(str(str(GameScores[0]) + ' ' + str(GameScores[1]) + '/' + str(GameScores[2]) + ' [' + str(GameScores[3]) +']' ))
        print(str(str(GameScores[4]) + ' ' + str(GameScores[5]) + '/' + str(GameScores[6]) + ' [' + str(GameScores[7]) +']' ))
        print(str((BatTeam)+' ' +str(Score)+'/' + str(Wickets)+ ' [' +str(OverCount) + ']'))
        if FollowOn == False:
            if (Score + GameScores[1]) > GameScores[5]:
                print(str((BatTeam) + ' leads by ' + str(Score + GameScores[1] - GameScores[5]) + ' runs.'))
            elif (Score + GameScores[1]) < GameScores[5]:
                print(str((BatTeam) + ' trails by ' + str(GameScores[5] - Score - GameScores[1])  + ' runs.'))
            else:
                print('Scores level.')
        else:
            if (Score+GameScores[5]) > GameScores[1]:
                print(str((BatTeam) + ' leads by ' + str(Score + GameScores[5] - GameScores[1]) + ' runs.'))
            elif (Score+GameScores[5]) < GameScores[1]:
                print(str((BatTeam) + ' trails by ' + str(GameScores[1] - GameScores[5] - Score)  + ' runs.'))
            else:
                print('Scores level.')

    if Innings == 3:
        print ()
        print(str(str(GameScores[0]) + ' ' + str(GameScores[1]) + '/' + str(GameScores[2]) + ' [' + str(GameScores[3]) +']' ))
        print(str(str(GameScores[4]) + ' ' + str(GameScores[5]) + '/' + str(GameScores[6]) + ' [' + str(GameScores[7]) +']' ))
        print(str(str(GameScores[8]) + ' ' + str(GameScores[9]) + '/' + str(GameScores[10]) + ' [' + str(GameScores[11]) +']' ))
        print(str(BatTeam)+' ' +str(Score)+'/' + str(Wickets)+ ' [' +str(OverCount) + ']')  
        if (GameOvers-OverCount+1) < GameOvers and (Score+GameScores[5]) <= (GameScores[1]+GameScores[9]) and Wickets != 10 and FollowOn == False:
            print(str(BatTeam)+ ' require ' + str((GameScores[1]+GameScores[9]-GameScores[5]-Score+1)) + ' more runs in ' +str((GameOvers-TotalOvers-OverCount)) + ' overs.')
        if (GameOvers-OverCount+1) < GameOvers and (Score+GameScores[5]) <= (GameScores[1]+GameScores[9]) and Wickets != 10 and FollowOn == True:
            print(str(BatTeam)+ ' require ' + str((GameScores[5]+GameScores[9]-GameScores[1]-Score+1)) + ' more runs in ' +str((GameOvers-TotalOvers-OverCount)) + ' overs.')
        
    print ('')
    if declare (x) == 'declare':
        dec = 1
    import time
    time.sleep(1 * delay)


def innings (BatTeam):
    global GameOvers
    global OverCount, TotalOvers
    global GameScores
    global Score
    global card
    global BowlCard, FallOfWickets, dec
    global SpellCount
    global Wickets
    global Team1Captain, Team1WK
    global Innings
    x = 0
    card = MakeCard(x)
    BowlCard = MakeBowlCard(x)
    SpellCount = MakeSpellCount(x)
    OverCount = 0
    overs = range(1,(GameOvers+1))
    for i in overs:
            over (i)
            OverCount = OverCount + 1
            if Wickets > 9:
                break
            if Innings == 3 and (int(Score)+GameScores[5]) > ((GameScores[1] + GameScores[9])) and FollowOn == False:
                break
            if Innings == 3 and (int(Score)+GameScores[1]) > ((GameScores[5] + GameScores[9])) and FollowOn == True:
                break
            if GameOvers < OverCount+TotalOvers or dec == 1:
                break
            
    Results = open('scorecard.txt', 'a')
    a = range (1,12)
    if Innings < 2:
        print (str(' '+Team1Name + ' - 1st innings'))
        Results.write(str(' '+Team1Name+ ' - 1st innings'))
    elif Innings == 2 and FollowOn == False:
        print (str(' '+Team1Name + ' - 2nd innings'))
        Results.write(str(' '+Team1Name + ' - 2nd innings'))
    elif Innings == 2 and FollowOn == True:
        print (str(' '+Team1Name + ' - 2nd innings (following on)'))
        Results.write(str(' '+Team1Name + ' - 2nd innings (following on)'))
    else:
        print (str(' '+Team1Name + ' - 2nd innings (Target: ' + str(GameScores[1]+GameScores[9]-GameScores[5]+1) + ')'))
        Results.write(str(' '+Team1Name + ' - 2nd innings (Target: ' + str(GameScores[1]+GameScores[9]-GameScores[5]+1)) + ')')
    
    Results.write('\n')
    for i in a:
        if card[i][2] > 0 and card[i][4] == '':
            card[i][4] = 'not out'
        if card[i][0] == Team1Captain and card[i][0] == Team1WK:
            prefix = '*+'
        elif card[i][0] == Team1Captain:
            prefix = '*'
        elif card[i][0] == Team1WK:
            prefix = '+'
        else:
            prefix = ' '
        NameFormat = str(card[i][0])
        NameLength = max(len(s) for s in Team1)
        if prefix == '*+':
            NameFormat = NameFormat.ljust(NameLength)
        else:
            NameFormat = NameFormat.ljust(NameLength+1)
        DismissalFormat = str(card[i][4])
        BowlNameLength = 0
        for t in range(1,11):
            if len(card[t][4]) > BowlNameLength:
                BowlNameLength = len(card[t][4])
        
        DismissalFormat = DismissalFormat.rjust(3+BowlNameLength)
        RunsFormat = str(card[i][1])
        RunsFormat = RunsFormat.rjust(3)
        BallsFormat = str(' (' + str(card[i][2]) + ')' )
        BallsFormat = BallsFormat.rjust(6)
        
        print (str(prefix) + NameFormat + ' ' + DismissalFormat + ' ' + RunsFormat + BallsFormat)
        Results.write(str(prefix) + NameFormat + ' ' + DismissalFormat + ' ' + RunsFormat + BallsFormat)
        Results.write('\n')
    
    if Innings < 3 and Wickets < 10:
        print (str(('(' + str(Wickets) + ' wickets declared - '+str(OverCount) +' overs)  '+str(Score) )).rjust(NameLength+BowlNameLength+10))
        Results.write (str(('(' + str(Wickets) + ' wickets declared - '+str(OverCount) +' overs)  '+str(Score) )).rjust(NameLength+BowlNameLength+10))
    else:
        print (str(('(' + str(Wickets) + ' wickets - '+str(OverCount) +' overs)  '+str(Score) )).rjust(NameLength+BowlNameLength+10))
        Results.write (str(('(' + str(Wickets) + ' wickets - '+str(OverCount) +' overs)  '+str(Score) )).rjust(NameLength+BowlNameLength+10))
    print (' ')
    Results.write('\n')

    if Wickets > 0:
        for w in range (0,(len(FallOfWicket))):
            #print (str(' ' + str(FallOfWicket[w]) + '-' + str(w+1) + ' '), end=''),
            Results.write(str(' ' + str(FallOfWicket[w]) + '-' + str(w+1) + ' '))
        print (' ')
        Results.write('\n')


    Results.write('\n')
    print (' ')

    for i in a:
        if (BowlCard[i][1]) > 0:
            NameFormat = str(BowlCard[i][0])
            NameLength = max(len(s) for s in Team2)
            NameFormat = NameFormat.ljust(NameLength+1)
            OversFormat = str(BowlCard[i][1])
            OversFormat = OversFormat.rjust(2)
            MaidensFormat = str(BowlCard[i][2])
            MaidensFormat = MaidensFormat.rjust(2)
            RunsFormat = str(BowlCard[i][3])
            RunsFormat = RunsFormat.rjust(3)
            WicketsFormat = str(BowlCard[i][4])
            WicketsFormat = WicketsFormat.rjust(2)
            print (str(' ' +NameFormat+ ' ' + OversFormat + ' - ' + MaidensFormat + ' - ' + RunsFormat + ' - ' + WicketsFormat))
            Results.write(str(' ' +NameFormat+ ' ' + OversFormat + ' - ' + MaidensFormat + ' - ' + RunsFormat + ' - ' + WicketsFormat))
            Results.write('\n')

    Results.write('\n')

    print ('')
    if Innings == 3 and Wickets == 10 and ((GameScores[1] + GameScores[9]) > (Score+GameScores[5])):
        print (str(str(BowlTeam) + ' wins by ' +str((GameScores[1] + GameScores[9])-(Score+GameScores[5]))) + ' runs.')
        Results.write((str(str(BowlTeam) + ' wins by ' +str((GameScores[1] + GameScores[9])-(Score+GameScores[5]))) + ' runs.'))
        for i in range (0, 22):
            if MOM[i][0] in Team2:
                MOM[i][1] = MOM[i][1] + 100
    elif Innings == 3 and (Score+GameScores[5]) > ((GameScores[1] + GameScores[9])):
        print (str(str(BatTeam) + ' wins by ' +str(10-Wickets) + ' wickets.'))
        Results.write ((str(str(BatTeam) + ' wins by ' +str(10-Wickets) + ' wickets.')))
        for i in range (0, 22):
            if MOM[i][0] in Team1:
                MOM[i][1] = MOM[i][1] + 100
    elif Innings == 3 and (Score+GameScores[5]) == GameScores[1]+GameScores[9]:
        print ('Match tied.')
        Results.write('Match tied.')
    if Innings == 0:
        print(str(BatTeam)+' ' +str(Score)+'/' + str(Wickets)+ ' [' +str(OverCount) + ']')

    Results.close()

def switch (a):
    a = a
    global Bowl1
    global Bowl2
    global Bat1
    global Bat2
    global BatTeam
    global BowlTeam
    global Score, Innings
    global Wickets
    global GameScores
    global OverCount, TotalOvers
    global Team1
    global Team2
    global Team1WK
    global Team2WK
    global Team1Name
    global Team2Name
    global Team1BatAbi
    global Team2BatAbi
    global card, BowlCard, MOM
    global Team1BatAvs, Team2BatAvs, Team1BowlAvs, Team2BowlAvs, Team1BowlAbi, Team2BowlAbi, Team1ERs, Team2ERs
    global FatigueList, FallOfWicket, LastWicket, FollowOn
    global Team1Captain, Team2Captain, Team1Roles, Team2Roles

    if FollowOn == False:
        GameScores.append(BatTeam)
        GameScores.append(Score)
        GameScores.append(Wickets)
        GameScores.append(OverCount)
    Score = 0
    Wickets = 0
    if FollowOn == False:
        for i in range (0, 11):
            for j in range (0, 22):
                if card[i][0] == MOM[j][0]:
                    if Innings < 2:
                        MOM[j][1] = MOM[j][1] + card[i][1]
                    elif Innings == 2:
                        MOM[j][1] = MOM[j][1] + 1.5*card[i][1]
                    else:
                        MOM[j][1] = MOM[j][1] + 2*card[i][1]
                if BowlCard[i][0] == MOM[j][0]:
                    MOM[j][1] = MOM[j][1] + 25*int(BowlCard[i][4])
                    MOM[j][1] = MOM[j][1] + 1.5*BowlCard[i][1]
                    MOM[j][1] = MOM[j][1] - (BowlCard[i][3])/2

    TotalOvers = TotalOvers + OverCount

    OverCount = 0

    Team1, Team2 = Team2, Team1
    Team1Name, Team2Name = Team2Name, Team1Name

    BatTeam, BowlTeam = BowlTeam, BatTeam
    Team1WK, Team2WK = Team2WK, Team1WK
    Team1BatAbi, Team2BatAbi = Team2BatAbi, Team1BatAbi
    Team1BatAvs, Team2BatAvs = Team2BatAvs, Team1BatAvs
    Team1BowlAbi, Team2BowlAbi = Team2BowlAbi, Team1BowlAbi
    Team1BowlAvs, Team2BowlAvs = Team2BowlAvs, Team1BowlAvs
    Team1Captain, Team2Captain = Team2Captain, Team1Captain
    Team1Roles, Team2Roles = Team2Roles, Team1Roles
    Team1ERs, Team2ERs = Team2ERs, Team1ERs
    
    Bat1 = Team1[0]
    Bat2 = Team1[1]
    Bowl1 = Team2[9]
    Bowl2 = Team2[10]

    card =[
    ['name','runs','balls faced','out?','dismissal','fours','sixes'],
    [],
    [],
    [],
    [],
    [],
    [],
    [],
    [],
    [],
    [],
    []
        ]

    FatigueList = []
    FallOfWicket = [0]
    LastWicket = [0,'','',0,'']

    if FollowOn == False:
        Innings = Innings + 1
    print ()
    if Innings < 4:
        print ('CHANGE OF INNINGS')
    print ()


WinningTeam = ''
FollowOn = False
innings (BatTeam)
if GameOvers < OverCount+TotalOvers:
    print ('Match Drawn.')
    Results = open('scorecard.txt', 'a')
    Results.write('Match Drawn.')
    Results.close()
else:
    switch (x)
    innings (BatTeam)
    switch (x)
    if GameScores[1] - GameScores[5] > 200:
        FollowOn = True
        print ('Follow-on enforced.')
        switch (x)
        innings (BatTeam)
        if Score + GameScores[5] >= GameScores[1]:
            FollowOn = False
            switch (x)
            FollowOn = True
            innings (BatTeam)                
        else:
            FollowOn=False 
            switch (x)
            Results = open('scorecard.txt', 'a')
            print (str( str(BatTeam) + ' wins by an innings and ' + str(GameScores[1]-(GameScores[5] + GameScores[9])) + ' runs.'))
            Results.write(str( str(BatTeam) + ' wins by an innings and ' + str((GameScores[1]-GameScores[5]-GameScores[9]))     + ' runs.'))
            Results.close()
            WinningTeam = Team1
    else:
        innings(BatTeam)
        if Score + GameScores[1] < GameScores[5]:
            print (str( str(BatTeam) + ' wins by an innings and ' + str(GameScores[5]-(GameScores[1] + Score)) + ' runs.'))
            Results = open('scorecard.txt', 'a')
            Results.write(str( str(BatTeam) + ' wins by an innings and ' + str((GameScores[5]-GameScores[1]-Score))    + ' runs.'))
            Results.close()
            WinningTeam=Team1
        else:
            switch (x)
            innings (BatTeam)
            switch (x)


for i in range (0, 22):
    if MOM[i][0] in WinningTeam:
        MOM[i][1] = MOM[i][1] + 100

if GameOvers < OverCount+TotalOvers:
    print ('Match Drawn.')
    Results = open('scorecard.txt', 'a')
    Results.write('Match Drawn.')
    Results.close()

MaxMOM = 0
for i in range (0, 22):
    if MOM[i][1] > MaxMOM:
        MaxMOM = MOM[i][1]
        ManOfMatch = MOM[i][0]
MOM.sort(key = lambda x: x[1], reverse = True)
#print (MOM)
print ( str ('Man of the Match: ' + str(ManOfMatch)))
Results = open('scorecard.txt', 'a')
Results.write('\n')
Results.write( str ('Man of the Match: ' + str(ManOfMatch)))
Results.close()
