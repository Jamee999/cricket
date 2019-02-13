import random, time, os, pexpect, shutil, copy, datetime

CurrentTime = datetime.datetime.now()
CurrentYear = CurrentTime.year

print ('')
print ('')

PlayersTemp = []
with open('alldata.txt') as f:
    for line in f:
        if line[0:-1] not in PlayersTemp:
            PlayersTemp.append(line[0:-1])

for i in range (0, len(PlayersTemp)):
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
    if PlayersTemp[i][7] == 0:
        PlayersTemp[i][7] = 1.4
    PlayersTemp[i][8] = int(PlayersTemp[i][8])

Year = 0
Number = 0
Games = 0

while Year < 1877 or Year > CurrentYear:
    Year = input('What year would you like to draft players from? ')
    if Year == 'all':
        break
    Year = int(Year)
while Number < 2 or Number > 257:
    Number = input('How many teams would you like to draft? ')
    Number = int(Number)
if Number < 12:
    while (Games < 1 or Games > 20):
        Games = input('How many times should the teams play each other? ')
        Games = int(Games)
else:
    Games = 1

folder = str(input('Input the name of the folder to save scorecards to. '))

try:
    os.mkdir(folder)
except:
    q = 100

TeamNames = []
DefaultTeams = ['London', 'Melbourne', 'Mumbai', 'Dubai', 'Cape Town', 'Lahore', 'Bridgetown', 'Kolkata', 'Sydney', 'Manchester', 'Auckland', 'Colombo', 'Delhi', 'Dhaka', 'Kingston', 'Johannesburg', 'Abu Dhabi', 'Perth', 'Harare', 'New York', 'Birmingham', 'Karachi', 'Wellington', 'Georgetown', 'Chennai', 'Brisbane', 'Durban', 'Port of Spain', 'Kabul', 'Dublin', 'Galle', 'Chittagong', 'Adelaide', 'Nottingham', 'Islamabad', 'Christchurch', 'Bangalore', 'Kandy', 'Tokyo', 'Port Elizabeth', 'Leeds', 'Faisalabad', 'Hamilton', 'Bulawayo', 'Antigua', 'Hong Kong', 'Hobart', 'Sharjah', 'Mohali', 'South London', 'Los Angeles', 'Centurion', 'Ahmedabad', 'Cardiff', 'Dunedin', 'Peshawar', 'Amsterdam', 'Rawalpindi', 'Nairobi', 'Toronto', 'Bloemfontein', 'Singapore', 'Napier', 'Windhoek', 'Edinburgh', 'Multan', 'Pretoria', 'Bristol', 'Jaipur', 'Canberra', 'Durham', 'Kimberley', 'Cairns', 'Kuala Lumpur', 'Grenada', 'Invercargill', 'Belfast', 'East London', 'Gold Coast', 'Southampton', 'Port Moresby', 'Dambulla', 'Leicester', 'Bermuda', 'Miami', 'Townsville', 'Alice Springs', 'Worcester', 'Kathmandu', 'Darwin', 'St Lucia', 'Newcastle', 'Pune', 'Copenhagen', 'Canterbury', 'Shanghai', 'Queenstown', 'Kampala', 'Seoul', 'Chicago', 'Paris', 'Derby', 'Mexico City', 'Chelmsford', 'Vancouver', 'Taunton', 'Berlin', 'Sylhet', 'Surat', 'Sao Paulo', 'Buenos Aires', 'Northampton', 'Beijing', 'Hove', 'St Vincent', 'Rome', 'Palmerston North', 'Lucknow', 'Jakarta', 'St Kitts', 'Montego Bay', 'Milan', 'Dominica', 'Houston', 'Bay of Plenty','Barcelona', 'Wollongong', 'Kandahar', 'Liverpool', 'Geelong', 'Ballarat' , 'New Plymouth', 'Launceston', 'Suva', 'Bangkok', 'Manila', 'Taipei', 'Kochi', 'Chandigarh', 'Mysore', 'Jaffna', 'Thimphu' , 'Quetta', 'Bahawalpur',  'Muscat',  'Bahrain', 'Qatar', 'Kuwait', 'Cairo', 'Jerusalem', 'Athens', 'Istanbul', 'Bucharest', 'Moscow', 'Vienna', 'Monaco' , 'Cambridge', 'Oxford', 'Exeter', 'Glasgow', 'Aberdeen', 'Cork', 'Montreal', 'Philadelphia', 'Washington', 'Atlanta', 'San Francisco', 'Seattle', 'New Orleans', 'Las Vegas', 'San Juan', 'Santo Domingo', 'Tobago', 'Bogota', 'Rio de Janeiro', 'Gaborone', 'Polokwane', 'Pietermaritzburg', 'Mutare', 'Mombasa', 'Lagos', 'Casablanca', 'Spanish Town', 'Norwich', 'Macau', 'Osaka', 'Nelson', 'Whangarei', 'Bendigo', 'Nagpur', 'Madurai', 'Visakhapatnam', 'Patna', 'Kanpur', 'Khulna', "Cox's Bazar", 'Indore', 'Madrid', 'Prague', 'Warsaw', 'Munich', 'Stockholm', 'Potchefstroom', 'Wagga Wagga', 'Bundaberg', 'Sheffield', 'Swansea', 'Lincoln', 'Limerick', 'Blackpool', 'Zagreb', 'Belgrade', 'Naples', 'Beirut', 'Budapest', 'Tblisi', 'Hanoi', 'Chengdu', 'Busan', 'Kyoto', 'Yokohama', 'Mackay', 'Sunshine Coast', 'Gisborne', 'Tonga', 'Samoa', 'Honolulu', 'Dallas', 'San Diego', 'St. Louis', 'Detroit', 'Denver', 'Monterrey', 'Aruba', 'Curacao', 'Montserrat', 'Lima', 'Montevideo', 'Accra', 'Dakar', 'Lisbon', 'Hamburg', 'Frankfurt', 'Brussels', 'Hull', 'Peterborough', 'Waterford', 'Oslo', 'Helsinki', 'Amman', 'Tel-Aviv', 'Middlesborough', 'Colwyn Bay', 'Riyadh', 'Tehran', 'Baghdad']


while len(TeamNames) < Number:
    y = input('Enter the name of a team. ')
    if y == 'default':
        TeamNames = []
        while len(TeamNames) < Number:
            TeamNames.append(DefaultTeams[0])
            DefaultTeams.pop(0)
    else:       
        TeamNames.append(y)

if ('East London' or 'South London') in TeamNames and 'London' in TeamNames:
    TeamNames[0] = 'North London'
else:
    TeamNames[0] = TeamNames[0]

Teams = []

TeamTemplate = ['Name', 'Open', 'Open', 'Bat', 'Bat', 'Bat', 'AR', 'WK', 'Seam', 'Seam', 'Bowl', 'Spin']

print (TeamNames)

UserTeam = 3
while UserTeam not in TeamNames:
    UserTeam = str (input('Enter the name of the team you would like to draft, or type "go" to have the computer select all teams. '))
    if UserTeam == 'go':
        break
print ('')
print ('')
TeamNames.sort(key=lambda x: random.random())

for i in range (0, len(TeamNames)):
    Teams.append([TeamNames[i]])
    for j in range (1, 12):
        if Teams[i][0] != UserTeam:
            Teams[i].append(TeamTemplate[j])

if Year == 'all':
    FilteredPlayers = PlayersTemp
else:
    FilteredPlayers = [x for x in PlayersTemp if x[4] <= Year and x[5] >= Year]

def Selection (x):

    if ['DG Bradman', 94.35, 51.12, 'Bat', 1928, 1948, 0.5, 1.0424710424710426, 24] in FilteredPlayers:
        return ['DG Bradman', 94.35, 51.12, 'Bat', 1928, 1948, 0.5, 1.0424710424710426, 24]
    
    if x == 'Open':
        try:
            Openers = [x for x in FilteredPlayers if 'Open' in x[3]]
            Openers.sort(key=lambda x: x[1], reverse = True)
            return Openers[0]
        except:
            FilteredPlayers.sort(key = lambda x: x[1], reverse = True)
            return FilteredPlayers[0]
    elif x == 'Bat':
        FilteredPlayers.sort(key = lambda x: x[1], reverse = True)
        return FilteredPlayers[0]
    elif x == 'WK':
        try:
            WKs = [x for x in FilteredPlayers if 'WK' in x[3]]
            WKs.sort(key= lambda x: x[1], reverse = True)
            return WKs[0]
        except:
            FilteredPlayers.sort(key = lambda x: x[1], reverse = True)
            return FilteredPlayers[0]
    elif x == 'AR':
        ARs = [x for x in FilteredPlayers if 'Bat' not in x[3] and 'Part' not in x[3] and 'WK' not in x[3]]
        ARs.sort(key=lambda x: x[1] + max(0, (40-x[2])), reverse = True)
        return ARs[0]
    elif x == 'Seam':
        Seamers = [x for x in FilteredPlayers if x[3] == 'Med' or x[3] == 'Fast']
        Seamers.sort(key=lambda x: x[1] + max(0, 3*(45-x[2])), reverse = True)
        return Seamers[0]
    elif x == 'Spin':
        Seamers = [x for x in FilteredPlayers if x[3] == 'Spin']
        Seamers.sort(key=lambda x: x[1] + max(0, 3*(45-x[2])), reverse = True)
        return Seamers[0]
    elif x == 'Bowl':
        Bowlers = [x for x in FilteredPlayers if 'Bat' not in x[3] and 'Part' not in x[3] and 'WK' not in x[3]]
        Bowlers.sort(key=lambda x: x[1] + max(0, 3*(45-x[2])), reverse = True)
        return Bowlers[0]

def UserSelection(x):
    Suggestions = []
    SugNames = []
    
    Openers = [x for x in FilteredPlayers if 'Open' in x[3]]
    Openers.sort(key=lambda x: x[1], reverse = True)
    for i in range (6):
        try:
            Suggestions.append([Openers[i][0], Openers[i][3]])
            SugNames.append(Openers[i][0])
        except:
            Suggestions = Suggestions

    FilteredPlayers.sort(key = lambda x: x[1], reverse = True)
    for i in range (12):
        if FilteredPlayers[i][0] not in SugNames:
            Suggestions.append([FilteredPlayers[i][0], FilteredPlayers[i][3]])
            SugNames.append(FilteredPlayers[i][0])

    WKs = [x for x in FilteredPlayers if 'WK' in x[3] and x[0] not in SugNames]
    for i in range (5):
        try:
            Suggestions.append([WKs[i][0], WKs[i][3]])
            SugNames.append(WKs[i][0])
        except:
            Suggestions = Suggestions

    ARs = [x for x in FilteredPlayers if 'Bat' not in x[3] and 'Part' not in x[3] and 'WK' not in x[3] and x[0] not in SugNames]
    ARs.sort(key=lambda x: x[1] + max(0, (40-x[2])), reverse = True)
    for i in range (7):
        try:
            Suggestions.append([ARs[i][0], ARs[i][3]])
            SugNames.append(ARs[i][0])
        except:
            Suggestions = Suggestions

    Bowlers = [x for x in FilteredPlayers if 'Bat' not in x[3] and 'Part' not in x[3] and 'WK' not in x[3] and x[0] not in SugNames]
    Bowlers.sort(key=lambda x: x[1] + max(0, 4*(45-x[2])), reverse = True)
    for i in range (15):
        try:
            Suggestions.append([Bowlers[i][0], Bowlers[i][3]])
            SugNames.append(Bowlers[i][0])
        except:
            Suggestions = Suggestions

    try:
        Spinners = [x for x in FilteredPlayers if x[3] == 'Spin' and x[0] not in SugNames]
        Spinners.sort(key= lambda x: x[1] + max(0, 4*(45-x[2])), reverse = True)
        for i in range (3):
            Suggestions.append([Spinners[i][0], Spinners[i][3]])
            SugNames.append(Spinners[i][0])
    except:
        WKs = WKs

    print ('')
    print ('Team so far:')
    print (UserTeamNames)
    
    Suggestions.sort(key = lambda x: x[0], reverse = False)
    
    print ('')
    print ('List of suggested players: ')
    print ('')
    print (Suggestions)

    for i in range (len(Suggestions)):
        Suggestions.append(Suggestions[i][0])

    SelectedPlayer = ''
    print ('')
    while SelectedPlayer not in Suggestions:
        SelectedPlayer = input('Enter the name of your selection: ')
        if SelectedPlayer in Suggestions:
            UserTeamNames.append(SelectedPlayer)

    
    print ('')
    return SelectedPlayer

UserTeamNames = []
t = 1
x = 0
while t < 10*len(Teams):
    for i in range (0, len(Teams)):
        if Teams[i][0] != UserTeam:
            pick = False
            while pick == False:
                n = random.choice(range(1,12))
                if Teams[i][n] == TeamTemplate[n]:
                    Choice = Selection (TeamTemplate[n])
                    Teams[i][n] = Choice
                    print (t, Teams[i][0], Teams[i][n][0])
                    h = open('{}/draft.txt'.format(folder),'a')
                    h.write('{} {} {}'.format(t, Teams[i][0], Teams[i][n][0]))
                    h.write('\n')
                    h.close()
                    time.sleep(1/5)
                    t = t+1
                    FilteredPlayers.remove(Choice)
                    pick = True
        else:
            UserPick = UserSelection (x)
            for j in range (len(FilteredPlayers)):
                if UserPick == FilteredPlayers[j][0]:
                    Teams[i].append(FilteredPlayers[j])
                    h = open('{}/draft.txt'.format(folder),'a')
                    h.write('{} {} {}'.format(t, Teams[i][0], FilteredPlayers[j][0]))
                    h.write('\n')
                    h.close()
                    FilteredPlayers.remove(FilteredPlayers[j])
                    t = t+1
                    break

    for i in range (len(Teams)-1,0,-1):
        if Teams[i][0] != UserTeam:
            pick = False
            while pick == False:
                n = random.choice(range(1,12))
                if Teams[i][n] == TeamTemplate[n]:
                    Choice = Selection (TeamTemplate[n])
                    Teams[i][n] = Choice
                    print (t, Teams[i][0], Teams[i][n][0])
                    h = open('{}/draft.txt'.format(folder),'a')
                    h.write('{} {} {}'.format(t, Teams[i][0], Teams[i][n][0]))
                    h.write('\n')
                    h.close()
                    time.sleep(1/5)
                    t = t+1
                    FilteredPlayers.remove(Choice)
                    pick = True
        else:
            UserPick = UserSelection (x)
            for j in range (len(FilteredPlayers)):
                if UserPick == FilteredPlayers[j][0]:
                    Teams[i].append(FilteredPlayers[j])
                    h = open('{}/draft.txt'.format(folder),'a')
                    h.write('{} {} {}'.format(t, Teams[i][0], FilteredPlayers[j][0]))
                    h.write('\n')
                    h.close()
                    FilteredPlayers.remove(FilteredPlayers[j])
                    t = t+1
                    break

    i = 0
    if Teams[i][0] != UserTeam:
        pick = False
        while pick == False:
            n = random.choice(range(1,12))
            if Teams[i][n] == TeamTemplate[n]:
                Choice = Selection (TeamTemplate[n])
                Teams[i][n] = Choice
                print (t, Teams[i][0], Teams[i][n][0])
                h = open('{}/draft.txt'.format(folder),'a')
                h.write('{} {} {}'.format(t, Teams[i][0], Teams[i][n][0]))
                h.write('\n')
                h.close()
                time.sleep(1/5)
                t = t+1
                FilteredPlayers.remove(Choice)
                pick = True

    else:
        UserPick = UserSelection (x)
        for j in range (len(FilteredPlayers)):
            if UserPick == FilteredPlayers[j][0]:
                Teams[i].append(FilteredPlayers[j])
                h = open('{}/draft.txt'.format(folder),'a')
                h.write('{} {} {}'.format(t, Teams[i][0], FilteredPlayers[j][0]))
                h.write('\n')
                h.close()
                FilteredPlayers.remove(FilteredPlayers[j])
                t = t+1
                break


for i in range (0, len(Teams)):
    if Teams[i][0] != UserTeam:
        pick = False
        while pick == False:
            n = random.choice(range(1,12))
            if Teams[i][n] == TeamTemplate[n]:
                Choice = Selection (TeamTemplate[n])
                Teams[i][n] = Choice
                print (t, Teams[i][0], Teams[i][n][0])
                h = open('{}/draft.txt'.format(folder),'a')
                h.write('{} {} {}'.format(t, Teams[i][0], Teams[i][n][0]))
                h.write('\n')
                h.close()
                time.sleep(1/5)
                t = t+1
                FilteredPlayers.remove(Choice)
                pick = True

    else:
        UserPick = UserSelection (x)
        for j in range (len(FilteredPlayers)):
            if UserPick == FilteredPlayers[j][0]:
                Teams[i].append(FilteredPlayers[j])
                h = open('{}/draft.txt'.format(folder),'a')
                h.write('{} {} {}'.format(t, Teams[i][0], FilteredPlayers[j][0]))
                h.write('\n')
                h.close()
                FilteredPlayers.remove(FilteredPlayers[j])
                t = t+1
                break


while len(FilteredPlayers) > 2*Number and len(Teams[0]) < 15:

    for i in range (len(Teams)-1,0,-1):
        if Teams[i][0] != UserTeam:
            FilteredPlayers.sort(key=lambda x: x[1] + 1.5*max(0, (45-x[2])), reverse = True)
            Teams[i].append(FilteredPlayers[0])
            print (t, Teams[i][0], FilteredPlayers[0][0])
            h = open('{}/draft.txt'.format(folder),'a')
            h.write('{} {} {}'.format(t, Teams[i][0], FilteredPlayers[0][0]))
            h.write('\n')
            h.close()
            t = t + 1
            FilteredPlayers.pop(0)

        else:
            UserPick = UserSelection (x)
            for j in range (len(FilteredPlayers)):
                if UserPick == FilteredPlayers[j][0]:
                    Teams[i].append(FilteredPlayers[j])
                    h = open('{}/draft.txt'.format(folder),'a')
                    h.write('{} {} {}'.format(t, Teams[i][0], FilteredPlayers[j][0]))
                    h.write('\n')
                    h.close()
                    FilteredPlayers.remove(FilteredPlayers[j])
                    t = t+1
                    break

    if Teams[i][0] != UserTeam:
        i = 0
        FilteredPlayers.sort(key=lambda x: x[1] + 1.5*max(0, (45-x[2])), reverse = True)
        Teams[i].append(FilteredPlayers[0])
        print (t, Teams[i][0], FilteredPlayers[0][0])
        h = open('{}/draft.txt'.format(folder),'a')
        h.write('{} {} {}'.format(t, Teams[i][0], FilteredPlayers[0][0]))
        h.write('\n')
        h.close()
        t = t + 1
        FilteredPlayers.pop(0)

    else:
        UserPick = UserSelection (x)
        for j in range (len(FilteredPlayers)):
            if UserPick == FilteredPlayers[j][0]:
                Teams[i].append(FilteredPlayers[j])
                h = open('{}/draft.txt'.format(folder),'a')
                h.write('{} {} {}'.format(t, Teams[i][0], FilteredPlayers[j][0]))
                h.write('\n')
                h.close()
                FilteredPlayers.remove(FilteredPlayers[j])
                t = t+1
                break

        
    for i in range (0, len(Teams)):
        if Teams[i][0] != UserTeam:
            FilteredPlayers.sort(key=lambda x: x[1] + 1.5*max(0, (45-x[2])), reverse = True)
            Teams[i].append(FilteredPlayers[0])
            print (t, Teams[i][0], FilteredPlayers[0][0])
            h = open('{}/draft.txt'.format(folder),'a')
            h.write('{} {} {}'.format(t, Teams[i][0], FilteredPlayers[0][0]))
            h.write('\n')
            h.close()
            t = t + 1
            FilteredPlayers.pop(0)
        else:
            UserPick = UserSelection (x)
            for j in range (len(FilteredPlayers)):
                if UserPick == FilteredPlayers[j][0]:
                    Teams[i].append(FilteredPlayers[j])
                    h = open('{}/draft.txt'.format(folder),'a')
                    h.write('{} {} {}'.format(t, Teams[i][0], FilteredPlayers[j][0]))
                    h.write('\n')
                    h.close()
                    FilteredPlayers.remove(FilteredPlayers[j])
                    t + t+1
                    break

try:
    shutil.copy('customteams.txt','tempcustomteams.txt')
except:
    t = t


for i in range (0, len(Teams)):
    f = open('customteams.txt','a')
    f.write(str(Teams[i][0]))
    f.write('\n')
    print ('')
    print (Teams[i][0])
    for j in range (1, len(Teams[i])):
        print (Teams[i][j])
        f.write(str(Teams[i][j]))
        f.write('\n')
    f.write('\n')
    f.close()



print ('')

def game (x,y,z):
    cricket = pexpect.spawn('python3 cricket.py')
    time.sleep (0.1)
    cricket.expect_exact("Type 'h' for historical teams, 'c' for custom teams, or 'r' to recreate a real test match. ")
    cricket.sendline ('c')
    time.sleep (0.1)
    cricket.expect_exact("Type 'l' to load a saved custom team, or 'n' to select a new one. ")
    cricket.sendline ('l')
    time.sleep (0.1)
    cricket.expect("Select a team")
    cricket.sendline (y)
    time.sleep (0.1)
    cricket.expect_exact("Type 'h' for historical teams, 'c' for custom teams, or 'r' to recreate a real test match. ")
    cricket.sendline ('c' )
    time.sleep (0.1)
    cricket.expect_exact("Type 'l' to load a saved custom team, or 'n' to select a new one. ")
    cricket.sendline ('l')
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

Teams.sort(key = lambda x: random.random())

if Number < 12:
    Groups = [[]]
    GroNum = 1
    for i in range (Number):
        Groups[0].append(Teams[i][0])

elif Number < 24:
    Groups = [ [],[]]
    GroNum = 2
    for i in range (Number):
        if i < Number/2:
            Groups[0].append(Teams[i][0])
        else:
            Groups[1].append(Teams[i][0])

elif Number < 32:
    Groups = [ [],[],[],[]]
    GroNum = 4
    for i in range (Number):
        if i < Number/4:
            Groups[0].append(Teams[i][0])
        elif i < Number/2:
            Groups[1].append(Teams[i][0])
        elif i < 3*Number/4:
            Groups[2].append(Teams[i][0])
        else:
            Groups[3].append(Teams[i][0])

else:
    if Number <= 80:
        GroNum = int(Number/8 - ((Number%8)/8))
    elif Number <=120:
        GroNum = int(Number/12 - ((Number%12)/12))
    else:
        GroNum = int(Number/16 - ((Number%16)/16))
    
    Groups = []
    for j in range (GroNum):
        Groups.append([])
    for i in range (Number):
        check = False
        for k in range (1, GroNum+1):
            if i < k*Number/GroNum and check == False:
                Groups[k-1].append(Teams[i][0])
                check = True
                
#print (GroNum)
#print (Groups)

n = 1
for k in range (0, len(Groups)):
    for a in range (Games):
        for i in range (len(Groups[k])-1):
            for j in range (0, len(Groups[k])-i-1):
                game (n, Groups[k][i], Groups[k][i+j+1])
                f=open('{}/scorecard{}.txt'.format(folder, n),'r')
                result = f.readlines()[-3]
                f.close()
                e=open('{}/results.txt'.format(folder),'a')
                e.write('{} v. {} - '.format(Groups[k][i], Groups[k][i+j+1]))
                e.write(result)
                e.close()
                print('{} v. {}'.format(Groups[k][i], Groups[k][i+j+1]))
                print (result)
                n = n + 1

GroupGames = copy.deepcopy(n)
TotalGames = n
#Team, Games, Wins, Losses, Draws, Innings Wins
Table = []
Results = []

g = open('{}/results.txt'.format(folder),'r')
for line in g:
    Results.append(line)
g.close()

for i in range(len(Teams)):
    Table.append([Teams[i][0],0,0,0,0,0])
    for j in range(len(Results)):
        if Teams[i][0] in Results[j]:
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
print('Team           Games  Wins  Losses  Draws  Innings Wins')
e = open('{}/table.txt'.format(folder),'a')
e.write('Team           Games  Wins  Losses  Draws  Innings Wins')
e.write('\n')
for j in range (GroNum):
    for i in range(len(Table)):
        if Table[i][0] in Groups[j]:
            print('{} {}     {}    {}     {}      {}'.format(Table[i][0].ljust(16),str(Table[i][1]).ljust(2),str(Table[i][2]).ljust(2),str(Table[i][3]).ljust(2),str(Table[i][4]).ljust(2),str(Table[i][5]).ljust(2)))
            e.write('{} {}     {}    {}     {}      {}'.format(Table[i][0].ljust(16),str(Table[i][1]).ljust(2),str(Table[i][2]).ljust(2),str(Table[i][3]).ljust(2),str(Table[i][4]).ljust(2),str(Table[i][5]).ljust(2)))
            e.write('\n')
    print ('')
    e.write('\n')
e.close()

if len(Groups) == 1:
    print('')
    print ('Final:')
    game (n, Table[0][0], Table[1][0])
    f=open('{}/scorecard{}.txt'.format(folder, n),'r')
    result = f.readlines()[-3]
    f.close()
    e=open('{}/results.txt'.format(folder),'a')
    e.write('{} v. {} - '.format(Table[0][0], Table[1][0]))
    e.write(result)
    e.close()
    print('{} v. {}'.format(Table[0][0], Table[1][0]))
    print (result)

else:
    GroupWinners = []
    for i in range (len(Groups)):
        check = False
        for j in range (len(Table)):
            if Table[j][0] in Groups[i] and check == False:
                GroupWinners.append(Table[j][0])
                check = True
    #print (GroupWinners)

    Table = []

    if len(GroupWinners) == 2:
        print('')
        print ('Final:')
        game (n, GroupWinners[0], GroupWinners[1])
        f=open('{}/scorecard{}.txt'.format(folder, n),'r')
        result = f.readlines()[-3]
        f.close()
        e=open('{}/results.txt'.format(folder),'a')
        e.write('{} v. {} - '.format(GroupWinners[0], GroupWinners[1]))
        e.write(result)
        e.close()
        print('{} v. {}'.format(GroupWinners[0], GroupWinners[1]))
        print (result)

    else:
        print ('')
        print ('Championship Group:')
        print ('')
        n1 = 0
        for i in range (0, len(GroupWinners)-1):
            for j in range (1, len(GroupWinners)-i):
                game (n, GroupWinners[i], GroupWinners[i+j])
                f=open('{}/scorecard{}.txt'.format(folder, n),'r')
                result = f.readlines()[-3]
                f.close()
                e=open('{}/results.txt'.format(folder),'a')
                e.write('{} v. {} - '.format(GroupWinners[i], GroupWinners[i+j]))
                e.write(result)
                e.close()
                print('{} v. {}'.format(GroupWinners[i], GroupWinners[i+j]))
                print (result)
                n = n + 1
                n1 = n1 + 1

        Results = []
        g = open('{}/results.txt'.format(folder),'r')
        for line in g:
            Results.append(line)
        g.close()
        ChampResults = Results[GroupGames-1:]
        #print (ChampResults)

        for i in range(len(GroupWinners)):
            Table.append([GroupWinners[i],0,0,0,0,0])
            for j in range(n1):
                if GroupWinners[i] in ChampResults[j]:
                    Table[i][1] = Table[i][1] + 1
                    if ChampResults[j].count(GroupWinners[i]) == 2:
                        Table[i][2] = Table[i][2] + 1
                        if 'innings' in ChampResults[j]:
                            Table[i][5] = Table[i][5] + 1
                    elif 'Drawn' in ChampResults[j] or 'tied' in ChampResults[j]:
                        Table[i][4] = Table[i][4] + 1
                    else:
                        Table[i][3] = Table[i][3] + 1

        Table.sort(key=lambda x: x[2]*3.01 + x[4] + x[5], reverse = True)
        print('Team           Games  Wins  Losses  Draws  Innings Wins')
        e = open('{}/table.txt'.format(folder),'a')
        e.write('\n')
        e.write('Team           Games  Wins  Losses  Draws  Innings Wins')
        e.write('\n')

        for i in range(len(Table)):
            if Table[i][0] in GroupWinners:
                print('{} {}     {}    {}     {}      {}'.format(Table[i][0].ljust(16),str(Table[i][1]).ljust(2),str(Table[i][2]).ljust(2),str(Table[i][3]).ljust(2),str(Table[i][4]).ljust(2),str(Table[i][5]).ljust(2)))
                e.write('{} {}     {}    {}     {}      {}'.format(Table[i][0].ljust(16),str(Table[i][1]).ljust(2),str(Table[i][2]).ljust(2),str(Table[i][3]).ljust(2),str(Table[i][4]).ljust(2),str(Table[i][5]).ljust(2)))
                e.write('\n')
        e.close()
        print ('')

print ('Calculating statistics.')
print ('')

for j in range (1, TotalGames):
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
    for j in range(len(Teams)):
        for k in range (len(Teams[j])):
            if batstats[i][0] == Teams[j][k][0]:
                teamname = Teams[j][0]
                break
    g.write('{} ({}) - {} runs @ {}'.format(batstats[i][0], teamname, batstats[i][2], (round(batstats[i][2]/batstats[i][1],2))))
    g.write('\n')
    runssum = runssum + batstats[i][2]
    wicketssum = wicketssum + batstats[i][1]
g.close()
h = open('{}/stats.txt'.format(folder),'a')

for i in range (len(bowlnames)):
    for j in range(len(Teams)):
        for k in range (len(Teams[j])):
            if bowlstats[i][0] == Teams[j][k][0]:
                teamname = Teams[j][0]
                break
    if bowlstats[i][4] > 0:
        h.write('{} ({}) - {} wickets @ {} (ER: {}, SR: {})'.format(bowlstats[i][0], teamname, bowlstats[i][4], round((bowlstats[i][3]/bowlstats[i][4]),2), round((bowlstats[i][3]/bowlstats[i][1]),2),round((6*bowlstats[i][1]/bowlstats[i][4]),2)))
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
                if batstats[i][2]/batstats[i][1] > 35 and batstats[i][1] > (3+Number/20) and bowlstats[j][3]/bowlstats[j][4] < 35 and bowlstats[j][4] > (5+Number/10):
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

shutil.copy('customteams.txt','{}/customteams.txt'.format(folder))
shutil.copy('tempcustomteams.txt','customteams.txt')

print ('')
print ('')
