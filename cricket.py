import random, time
import datetime

CurrentTime = datetime.datetime.now()
CurrentYear = CurrentTime.year

BatAbi = 1 #batsman's ability
BowlAbi = 1 #bowler's ability
BaseRPO = 3
BaseWkRt = ((1757-215)/92749)
Base4Rt = (5495/92749)
Base6Rt = (380/92749)
BaseScrRt = ((47446 - (5495*4) - (380*6)) / 92749)

#  2017 only    Mat	Inns	NO	Runs	HS	Ave	BF	SR	100	50	0	4s	6s
# 	191	47	1757	215	47446	244*	30.76	92749	51.15	92	228	173	5495	380

GameOvers = 450 #maximum number of overs in the game


### THIS SECTION PROVIDES THE FUNCTIONS THAT WILL LET THE USER PICK THEIR HISTORICAL OR CUSTOM TEAMS


def CustomOrHistorical (x):
    y = ''
    while y != 'h' and y!= 'c' and y != 'r': #loops until given acceptable input
        y = str(input(str("Type 'h' for historical teams, 'c' for custom teams, or 'r' to recreate a real test match. " )))
        if y == 'h':
            return 'historical'
        if y == 'c':
            return 'custom'
        if y == 'r':
            return 'recreate'
        else:
            print ('Invalid input. ')

def HistoricalYearsSelect (x):
    valid = 0
    Years = [x for x in range (1877, CurrentYear+1) if x < 1914 or x > 1946 or 1919 < x < 1939] #Defines acceptable years
    while valid == 0: #loops until given acceptable answer
        YearInput = str(input("Type 'all' for all-time teams, 'random' for a random year, or input a year (or range of years): ")) #User Input
        YearInput = ''.join(YearInput.split()) #removing spaces

        if YearInput == 'same':
            global FirstYear, LastYear
            valid = 1
            return str(str(FirstYear)+'-'+str(LastYear))

        elif YearInput == 'random':
            Year = random.choice(Years)
            print ('')
            print (Year)
            print ('')
            valid = 1
            return str(str(Year)+'-'+str(Year)) #returns in form XXXX-XXXX

        elif YearInput == 'all':
            valid = 1
            return '1877-{}'.format(CurrentYear)

        elif YearInput == 'current':
            valid = 1
            return '{}-{}'.format(CurrentYear-2, CurrentYear)

        elif "-" in YearInput: #sees if a range has been selected
            Range = YearInput
            Range = Range.split('-') #turns into a set [Year1, Year2]
            #print (Range)
            if Range[0] == '': #validates blank sides of ranges as being equal to the smallest or largest possible value
                Range[0] = str(1877)
            if Range[1] == '':
                Range [1] = str(CurrentYear)
            #print (Range)
            try:
                if int(Range[0]) in Years and int(Range[1]) in Years: #checks if the two range inputs are acceptable years
                    valid = 1
                    return str(Range[0]+'-'+Range[1]) #returns in form XXXX-YYYY
                else: #if the Years aren't acceptable, returns to top of loop
                    print ('Invalid input. Please enter valid years. ')
            except: #starts function loop again if error
                print ('Invalid input. ')

        else:
            try:
                if int(YearInput) in Years:
                    valid = 1
                    return str(str(YearInput)+'-'+str(YearInput)) #returns in form XXXX-XXXX
                else: #if YearInput is an integer but not a valid year, returns to top of function
                    print ('Invalid input. ')

            except: #if YearInput isn't an integer, returns to top of function
                print ('Invalid input. ')



def DataValidation (x):
    global PlayersTemp
    for i in range (0, x): #turns the data into the right formats
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
        PlayersTemp[i][8] = int(PlayersTemp[i][8])

def PossibleTeams (x):
    global CustomTeams
    PossibleTeams = []
    CustomTeams = []
    with open ('customteams.txt') as g: #reads customteams.txt
        for line in g:
            CustomTeams.append(line)
    for i in range (0, len(CustomTeams)):
        try:
            if CustomTeams[i] == '\n': #finds the team names following a blank line
                PossibleTeams.append(CustomTeams[i+1][0:-1]) #adds the names to PossibleTeams
        except:
            continue
    return PossibleTeams


def CustomSelect (x):
    global PlayersTemp, CustomTeams, TeamName
    PlayersTemp = []
    z = ''

    while z != 'l' and z != 'n': #loops until given acceptable input
        z = str(input ("Type 'l' to load a saved custom team, or 'n' to select a new one. "))


    if z == 'n': #new custom team
        Players = []
        with open('alldata.txt') as f:
            for line in f:
                PlayersTemp.append(line[0:-1]) #opens the data of all players and adds it to the set PlayersTemp
        DataValidation(len(PlayersTemp)) #corrects the format for all the Players in PlayersTemp

        TeamName = str(input ('Input the name of the custom team. '))
        n = 0 #number of players in custom team
        while n < 11:
            PlayerName = str(input("Please enter a player's name. "))
            success = 0 #tracks for a successful match
            PartialMatches = []
            for i in range (0, len(PlayersTemp)): #all players in DB
                if PlayerName == PlayersTemp[i][0]: #if the name is in..
                    Players.append(PlayersTemp[i]) #add the data to stats
                    print ('Success - Player in database added to team.')
                    print (PlayersTemp[i][0:6])
                    n = n+1
                    success = 1
                    break #stop searching
                elif PlayerName in PlayersTemp[i][0]: #partial match
                    PartialMatches.append(PlayersTemp[i][0])


            if success == 0: #searched every player - found no matching names
                if len(PartialMatches) == 0:
                    print ('Player not found, please try again.' )
                else:
                    print ('Did you mean one of these players? ' + str(PartialMatches))


        moreoption = ''
        while moreoption != 'n': #asking user if they want to continue past 11 players
            moreoption = str( input ("Type 'y' to add more players to squad, or 'n' to stop. "))
            if moreoption == 'n':
                break
            if moreoption == 'y':
                PlayerName = str(input("Please enter a player's name. "))
                success = 0 #tracks for a successful match
                for i in range (0, len(PlayersTemp)): #all players in DB
                        if PlayerName == PlayersTemp[i][0]: #if the name is in..
                            Players.append(PlayersTemp[i]) #add the data to stats
                            print ('Success - Player in database added to team.')
                            print (PlayersTemp[i][0:6])
                            n = n+1
                            success = 1
                            break #stop searching
                        elif PlayerName in PlayersTemp[i][0]: #partial match
                            PartialMatches.append(PlayersTemp[i][0])


            if success == 0: #searched every player - found no matching names
                if len(PartialMatches) == 0:
                    print ('Player not found, please try again.' )
                else:
                    print ('Did you mean one of these players? ' + str(PartialMatches)) #offers possibilities

        with open('customteams.txt', 'a') as customfile:
            customfile.write(str(TeamName)) #write the team name to customteams.txt
            customfile.write('\n') #new line
            for i in range (0, len(Players)):
                customfile.write(str(Players[i])) #writes each player's data to customteams.txt
                customfile.write('\n')
            customfile.write('\n') #blank line after the team is finished
        print ('Team saved to customteams.txt')
        return Players



    elif z == 'l': #load custom team
        valid = 0
        Options = PossibleTeams(x)
        Players = []

        while valid == 0: #checks if a valid team has been selected
            TeamName = str(input (str('Select a team from: ' +str(Options) + ' '))) #finds names of all saved teams
            if TeamName in Options:
                valid = 1 #stop checking for teams

                for i in range (0, len(CustomTeams)-1):
                    if CustomTeams[i][0:-1] == TeamName: #find the line with the team's name on it
                        moredata = True
                        n = 1
                        while moredata == True:
                            try:
                                Players.append(CustomTeams[i+n][1:-2]) #add the next line
                                n = n+1
                                if CustomTeams[i+n] == '\n': #if the line is blank...
                                    moredata = False #stop adding more lines
                            except: #if try gives an error, stop looking
                                break
                        break #stop when you find the team name
            for i in range (0, len(Players)):
                y = 1
                Players[i] = str(Players[i])
                Players[i] = Players[i].split(',')
                Players[i][0] = Players[i][0][1:-1]
                Players[i][1] = float(Players[i][1])
                Players[i][2] = float(Players[i][2])
                Players[i][3] = str(Players[i][3])[2:-1]
                Players[i][4] = int(Players[i][4])
                Players[i][5] = int(Players[i][5])
                Players[i][6] = float(Players[i][6])
                Players[i][7] = float(Players[i][7])
                Players[i][8] = int(Players[i][8])
            return Players


def CountrySelect(x,y):
    global Team1Name, Team1Years, FirstYear, LastYear
    x = int(x)
    y = int(y)
    Teams = ['England', 'Australia', 'South Africa', 'West Indies', 'New Zealand', 'India', 'Pakistan', 'Sri Lanka', 'Zimbabwe', 'Bangladesh', 'Ireland', 'Afghanistan', 'random', 'all']
    if y < 2018:
        Teams.remove('Ireland')
        Teams.remove('Afghanistan')
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
    if y < 1889 or (x > 1970 and y < 1992):
        Teams.remove('South Africa')

    if Team1Years == FirstYear or Team1Years == LastYear:
        Teams.remove(Team1Name)

    valid = 0
    while valid == 0: #cycles until given valid input
        SelectedTeam = str( input ('Select a team. The options are: ' + str(Teams) + ' '))
        if SelectedTeam == 'random':
            Teams.remove('random')
            Teams.remove('all')
            SelectedTeam = random.choice(Teams)
            print ('')
            print (SelectedTeam)
            print ('')
        if SelectedTeam in Teams:
            valid = 1
            return SelectedTeam
        else:
            print ('Invalid team.')

def CallPlayers (a, x, y):
    global PlayersTemp
    PlayersTemp = []
    Players = []
    x = int(x)
    y = int(y)
    country = ''.join(a.split()).lower() #removes spaces
    with open(str(str(country) + 'data.txt')) as f:
        for line in f:
            PlayersTemp.append(line[0:-1])
    DataValidation (len(PlayersTemp)) #converts data
    for i in range (0, len(PlayersTemp)):
        if PlayersTemp[i][4] <= y and PlayersTemp[i][5] >= x:
            Players.append(PlayersTemp[i])
    return Players

def RecreateSelect (x): #module that runs to select recreated tests
    y = 0
    while (1877 > y or y > CurrentYear) and y!= 'all': #loop until given a valid year
        try:
            y = input('Which year did your test match take place in? ')
            if y == 'random':
                y = random.choice(1877, CurrentYear)
                y = int(y)
                break
            if y == 'all':
                break
            y = int(y)
        except:
            print ('Invalid input.')

    Tests = []

    f = open('testmatchlist.txt','r') #read testmatchlist.txt
    for line in f:
        if str(y) in line or y == 'all':
            Tests.append(line[1:-2])
    f.close()

    ValidTests = []

    for i in range(0, len(Tests)): #get rid of apostraphes
        Tests[i] = Tests[i].replace("St John's", "'St Johns'")
        Tests[i] = Tests[i].replace("Lord's", "'Lords'")
        Tests[i] = Tests[i].replace("St George's", "'St Georges'")
        Tests[i] = Tests[i].split("'")
        Tests[i][0] = int(Tests[i][0][:-2]) #correctly format
        if y == 'all':
            for j in range (2, 7):
                Tests[i].pop(j)
            Tests[i][9] = int(Tests[i][9][2:])
            ValidTests.append(Tests[i])
            continue
        if Tests[i][0] != y:
            continue
        for j in range (2, 7):
            Tests[i].pop(j)
        Tests[i][9] = int(Tests[i][9][2:])
        ValidTests.append(Tests[i])

    print ('List of test matches in {}:'.format(y)) #print tests that took place in selected year
    for i in range (0, len(ValidTests)):
        formatted = '{} - {} vs. {}, {}, {}'.format(ValidTests[i][4],ValidTests[i][1],ValidTests[i][2],ValidTests[i][3],ValidTests[i][8])
        print (formatted)

    n = 0
    while n == 0: #loops until given a valid test
        try:
            z = int(input('Enter the number of the Test match you wish to simulate. '))
        except:
            print ('Invalid input.')
        for i in range (0, len(ValidTests)):
            if 'Test # {}'.format(z) == ValidTests[i][4]:
                q = i
                n = ValidTests[i][9] #cricinfo scorecard ID
                print ('Loading. ')
                break

    from bs4 import BeautifulSoup
    import requests
    import re
    url = 'http://www.espncricinfo.com/ci/engine/match/{}.html'.format(n) #url for selected game

    def Lineup(x): #finds the lineup 
        r = requests.get(url)
        data = r.content
        soup = BeautifulSoup(data, 'html.parser')
        players = []
        findtext = '{} 1st Innings'.format(x) #finds the team's first batsmen
        player = soup.find(text = findtext).parent.parent.parent.next_sibling.contents[0].contents[0].contents[1].contents[0].contents[0].contents[0]
        players.append(player)
        #print (player)
        n = 1
        for i in range (1,11): #find the next ten players
            try:
                player = soup.find(text = findtext).parent.parent.parent.next_sibling.contents[0].contents[i].contents[0].contents[0].contents[0].contents[0]
                if '<' not in player and 'Fall of wickets' not in player and 'Did not bat' not in player:
                    players.append(player)
                    #print (player.parent.parent.contents)
                    n = n+1
            except:
                n = n
        c = 1
        while n < 11:
            player = soup.find(text='Did not bat').parent.parent.parent.contents[c].contents[0].contents[0]
            player = player.replace(', ','')
            if 'Did not bat' not in player:
                players.append(player)
                #print (player)
                n = n+1
                c = c+1
        #print (players)
        return players

    def ReadPlayers (x, y): #find the players in the relevant data file
        global PlayersTemp
        PlayersTemp = []
        Players = []
        if y == 'ICC World XI':
            y = 'all'
        country = ''.join(y.split()).lower() #removes spaces
        with open(str(str(country) + 'data.txt')) as f:
            for line in f:
                PlayersTemp.append(line[0:-1])
        DataValidation (len(PlayersTemp)) #converts data
        for i in range (0, 11):
            for j in range (0, len(PlayersTemp)):
                if PlayersTemp[j][0] == x[i]:
                    Players.append(PlayersTemp[j])
                    #print (PlayersTemp[j])
                    break
        return Players

    def PlayerValidate (x):
        if 'jnr' in x:
            x = x.replace('jnr', ' jnr')
        if 'snr' in x:
            x = x.replace('snr', ' snr')
        if "Sir TC O'Brien" in x:
            x = x.replace('Sir ', '')
        if 'RJ Hadlee' in x:
            x = 'Sir RJ Hadlee'
        if 'Hon.LH Tennyson' in x:
            x = x.replace('Hon.LH', 'Lord')
        if 'OC Da Costa' in x:
            x = x.replace('Da', 'da')
        if 'Mehrab Hossain' in x:
            x = 'Mehrab Hossain jnr'
        if 'Enamul Haque' in x:
            x = 'Enamul Haque jnr'
            

        return x


    print ('')
    print (str(ValidTests[q][1]))
    print ('')    
    HomeTeam = Lineup (ValidTests[q][1])
    for i in range (0, 11):
        print (HomeTeam[i])
        #time.sleep(0.8)
        if ' (c)' in HomeTeam[i] and ' †' in HomeTeam[i]:
            HomeTeam[i] = HomeTeam[i].replace(' (c)','')
            HomeTeam[i] = HomeTeam[i].replace(' †','')
            HomeCapt = HomeTeam[i]
            HomeWK = HomeTeam[i]
        if ' (c)' in HomeTeam[i]:
            HomeTeam[i] = HomeTeam[i].replace(' (c)','')
            HomeCapt = HomeTeam[i]
        if ' †' in HomeTeam[i]:
            HomeTeam[i] = HomeTeam[i].replace(' †','')
            HomeWK = HomeTeam[i]
        HomeTeam[i] = PlayerValidate(HomeTeam[i])
    HomeTeamData = ReadPlayers (HomeTeam, ValidTests[q][1])
    print ('')
    print (str(ValidTests[q][2]))
    print ('')    
    AwayTeam = Lineup (ValidTests[q][2])
    for i in range (0, 11):
        print (AwayTeam[i])
 #       time.sleep (0.8)
        if ' (c)' in AwayTeam[i] and ' †' in AwayTeam[i]:
            AwayTeam[i] = AwayTeam[i].replace(' (c)','')
            AwayTeam[i] = AwayTeam[i].replace(' †','')
            AwayCapt = AwayTeam[i]
            AwayWK = AwayTeam[i]
        if ' (c)' in AwayTeam[i]:
            AwayTeam[i] = AwayTeam[i].replace(' (c)','')
            AwayCapt = AwayTeam[i]
        if ' †' in AwayTeam[i]:
            AwayTeam[i] = AwayTeam[i].replace(' †','')
            AwayWK = AwayTeam[i]
        AwayTeam[i] = PlayerValidate(AwayTeam[i])
    AwayTeamData = ReadPlayers (AwayTeam, ValidTests[q][2])
    #print (HomeTeamData, AwayTeamData)

    return [ValidTests[q][1], HomeTeamData, HomeCapt, HomeWK, ValidTests[q][2], AwayTeamData, AwayCapt, AwayWK, y]





def Choice (x):
    global TeamName, FirstYear, LastYear
    mode = CustomOrHistorical (x) #returns either 'historical'. 'custom' or recreate
    if mode == 'historical':
        Years = HistoricalYearsSelect (x)
        Range = Years.split('-')
        FirstYear = Range[0] #first eligible year
        LastYear = Range[1] #last eligible year
        TeamName = CountrySelect(FirstYear, LastYear)
        Players = CallPlayers (TeamName, FirstYear, LastYear)
        return Players

    elif mode == 'custom':
        FirstYear = 1877
        LastYear = CurrentYear
        Players = CustomSelect (x)
        return Players

    elif mode == 'recreate':
        return 'recreate'
        




############








########### THIS SECTION SELECTS THE ELEVEN PLAYERS FROM THE AVALIABLE SQUAD






def Select (Players):
    global BowlCount, SpinCount, customteamsave, PaceFactor, SpinFactor
    import random
    from operator import itemgetter
    SelectedTeam = []

    OpenCount = 0 #these variables track the various types of players in the team
    WKCount = 0
    BowlCount = 0
    SpinCount = 0

    Players.sort(key = lambda x: x[1] + 5*(random.random()-random.random()), reverse=True) #sort by batting average
    for i in range (0, 3):
        SelectedTeam.append(Players[i]) #add the top 3 players to the team...
    Players.pop(0) #and remove them from the selection pool
    Players.pop(0)
    Players.pop(0)

    Players.sort(key = lambda x: x[2] + 3*(random.random()-random.random())) #sort by bowling average
    for i in range (0,2): #add best 2 players to the team
        SelectedTeam.append(Players[i])
    if Players[0][1] > 25 and Players[1][1] > 25: #if both their batting averages are >25...
        SelectedTeam.append(Players[2]) #add the 3rd best bowler
        Players.pop(0)
    Players.pop(0) #remove from pool
    Players.pop(0)

    for i in range (0, (len(SelectedTeam))): #counting if the selected players are openers or keepers
        if 'WK' in SelectedTeam[i][3]:
            WKCount = WKCount + 1
        if 'Open' in SelectedTeam[i][3]:
            OpenCount = OpenCount+1

    if OpenCount + WKCount > 0: #if they are, add another batsman for every opener or keeper already selected
        Players.sort(key = lambda x: x[1] + 5*(random.random()-random.random()), reverse=True)
        for i in range (0, (OpenCount+WKCount)):
            SelectedTeam.append(Players[i])
        for i in range (0, (OpenCount+WKCount)):
            Players.pop(0)

    OpenCount = 0
    WKCount = 0

    for i in range (0, (len(SelectedTeam))): #recount (why?)
        if 'WK' in SelectedTeam[i][3]:
            WKCount = WKCount + 1
        if 'Open' in SelectedTeam[i][3]:
            OpenCount = OpenCount+1
    Players.sort(key=lambda x: x[1], reverse=True)
    if OpenCount < 2: #if the openers haven't been selected yet
        import copy
        Openers = copy.deepcopy(Players) #make a set called openers
        for i in range (0, (len(Openers)-1)):
            if 'Open' not in Openers[i][3]:
                Openers[i][1] = Openers[i][1] - 10
        Openers.sort(key = lambda x: x[1] + 5*(random.random()-random.random()), reverse=True) #sort by batting av, with a 10 run penalty for non-openers
        for i in range (0, 2-OpenCount):
            if 'Open' not in Openers[i][3]:
                Openers[i][1] = Openers[i][1] + 10
                Openers[i][3] = Openers[i][3] + 'FillIn' #non openers get the filin tag
            SelectedTeam.append(Openers[i])
            for j in range(0, (len(Players)-1)):
                if Players[j][0] == Openers[i][0]:
                    Players.remove(Players[j])
            if 'Bat' not in Openers[i][3] and 'WK' not in Openers[i][3] and 'Part' not in Openers[i][3]:
                BowlCount = BowlCount+1

    WKCount = 0

    for i in range (0, (len(SelectedTeam))): #count WKs
        if 'WK' in SelectedTeam[i][3]:
            WKCount = WKCount + 1
            WKName = SelectedTeam[i][0]

    if WKCount == 0: #if there's no WK in team, select the WK with the best batting av
        Keepers = [x for x in Players if 'WK' in x[3]]
        #print (Keepers)
        if len(Keepers) > 0:
            Keepers.sort(key = lambda x: x[1] + 5*(random.random()-random.random()), reverse = True)
            SelectedTeam.append(Keepers[0])
            WKName = Keepers[0][0]
            Players.remove(Keepers[0])
        else:
            Players.sort(key = lambda x: x[1] + 15*(random.random() - random.random()), reverse = True)
            #Players[0][3] = Players[0][3] + 'FakeWK' #if there's no keepers in the pool, pick a non-WK, label with FakeWK
            SelectedTeam.append(Players[0])
            WKName = 'WK NEEDED!!!'
            Players.remove(Players[0])

    PaceCount = 0

    for i in range (0, len(SelectedTeam)): #count the number of bowlers, pacers, spinners in the team
        if 'Bat' not in SelectedTeam[i][3] and 'WK' not in SelectedTeam[i][3] and 'Part' not in SelectedTeam[i][3]:
            if SelectedTeam[i][1] < 30:
                BowlCount = BowlCount+1
            elif SelectedTeam[i][1] < 40:
                BowlCount = BowlCount + 0.5
            else:
                BowlCount = BowlCount + (1/4)
        if 'Spin' in SelectedTeam[i][3] and 'Part' not in SelectedTeam[i][3]:
            SpinCount = SpinCount + 1
        if ('Fast' in SelectedTeam[i][3] or 'Med' in SelectedTeam[i][3]) and 'Part' not in SelectedTeam[i][3]:
            PaceCount = PaceCount + 1

    def Value (x): #defining how to calculate the value of the remaining players
        global BowlCount, SpinCount
        if 'Bat' in x[3] or 'WK' in x[3]: #batting average
            return x[1]/(PaceFactor*SpinFactor) + 5*(random.random()-random.random())
        elif 'Part' in x[3]:
            if PaceCount < 2 and 'Spin' not in x[3]: #batting average + 50-BowlAv
                return (x[1]/(PaceFactor*SpinFactor) + (max(0, (50-x[2]))))/2  + 5*(random.random()-random.random())
            else:
                return (x[1]/(PaceFactor*SpinFactor) + (max(0, (50-x[2]))))/2  + 5*(random.random()-random.random())

        else:
            if 'Spin' in x[3] and 'Part' not in x[3]: #the value of bowling average is modified by the makeup of the rest of the side and the pitch conditions
                if SpinCount > 0:
                    return (x[1]/(PaceFactor*SpinFactor) + (max(0, (45-x[2])*(PaceFactor/SpinFactor)) * (250/BowlCount**4)) + 5*(random.random()-random.random()))
                else:
                    return (x[1]/(PaceFactor*SpinFactor) + (max(0, (50-x[2])*(PaceFactor/SpinFactor)) * (500/BowlCount**4)) + 5*(random.random()-random.random())) 
            else:
                if PaceCount <2:
                    return (x[1]/(PaceFactor*SpinFactor) + (max(0, (50-x[2])*(SpinFactor/PaceFactor)) * (250/BowlCount**4))  + 5*(random.random()-random.random()))
                else:
                    return (x[1]/(PaceFactor*SpinFactor) + (max(0, (45-x[2])*(SpinFactor/PaceFactor)) * (250/BowlCount**4))  + 5*(random.random()-random.random()))

    n = len(SelectedTeam)
    for i in range (n, 11): #fill the team up to 11 players
        Players.sort(key = lambda x: Value (x), reverse = True) #resort by the adjusted value function after each player is selected
        SelectedTeam.append(Players[0]) #add the players
        Players.pop(0)
        if 'Bat' not in SelectedTeam[i][3] and 'WK' not in SelectedTeam[i][3] and 'Part' not in SelectedTeam[i][3]:
            if SelectedTeam[i][1] < 30:
                BowlCount = BowlCount+1
            elif SelectedTeam[i][1] < 40:
                BowlCount = BowlCount + 0.5
            else:
                BowlCount = BowlCount + (1/4)
        if 'Spin' in SelectedTeam[i][3] and 'Part' not in SelectedTeam[i][3]:
            SpinCount = SpinCount + 1
        if 'Fast' in SelectedTeam[i][3] or 'Med' in SelectedTeam[i][3]:
            PaceCount = PaceCount + 1

    if WKName == 'WK NEEDED!!!':
        for i in range (10):
            SelectedTeam.sort(key = lambda x: x[2], reverse = True)
            WKName = SelectedTeam[0][0]
            SelectedTeam[0][3] = SelectedTeam[0][3] + 'FakeWK'
            

    def Order (y): #putting the selected players in batting order
        Lineup = []
        #print (y)
        #print (' ')
        q = y
        for i in q:
            if 'Open' in i[3]:
                i.append(1) #adds value for openers
            if 'FillIn' in i[3]:
                i.append(0.7)
            if 'WK' in i[3]:
                try:
                    i[9] = i[9] - 0.5 #reduces the value for keeper-openers
                except:
                    i.append(0)
            if  'Open' not in i[3] and 'WK' not in i[3] and 'FillIn' not in i[3]:
                i.append(0)

        q = sorted(q, key = itemgetter(9,1), reverse = True) #sort by if an opener, then by batting average
        Lineup.append(q[0])
        Lineup.append(q[1])
        t = 0
        if q[2][1] > (q[3][1] - 15): #if there are 3+ openers, put the 3rd best at 3, unless the best non-opener is much better than him
            Lineup.append(q[2])
            t = 1
        q.pop(0)
        q.pop(0)
        if t == 1: #if three openers picked, remove them all from the order calculation
            q.pop(0)

        def Position (x):
            Av = x[1] + 3*(random.random()-random.random())
            if 'Bat' in x[3] or 'Part' in x[3]: #allrounders and WKs bat lower down
                Av = Av + 10
            return Av

        q = sorted (q, key = lambda x: Position (x), reverse = True) #sort by average modified by role
        for i in range(0,9-t):
            Lineup.append(q[i])
        for j in range (0,11): #add the remaining players to the order
            print (Lineup[j][0])
 #           time.sleep (0.8)
            Lineup[j].pop()
        return (Lineup)

    SelectedTeam = Order (SelectedTeam)
    return SelectedTeam

########################

def DataConvert (x):
    Names = []
    BatAvs = []
    BowlAvs = []
    Roles = []
    ERs = []
    for i in range (0, len(x)): #turns the player-by-player data into category-by-category
        #print (x[i])
        Names.append(x[i][0])
        BatAvs.append(x[i][1])
        BowlAvs.append(x[i][2])
        Roles.append(x[i][3])
        ERs.append(x[i][7])
    return (Names, BatAvs, BowlAvs, Roles, ERs)

def CaptainSelect(x):
    #print (x)
    x = sorted(x, key=lambda y: int(y[8])*random.random()+random.random(), reverse=True)
    return x[0][0]

###################

# THE FUNCTIONS ABOVE ARE CALLED IN THIS SECTION

PaceFactor = 1 + (0.3*random.random()) * (random.random()-random.random()) #how good the pitch is for pace. 0.75-1.25, lower is better for bowling
#PaceFactor = 1.1
SpinFactor = 1 + (0.3*random.random()) * (random.random()-random.random()) #same for spin
#SpinFactor = 0.75

print ('')


def PitchReport(PaceFactor, SpinFactor):
    if PaceFactor < 0.9 and SpinFactor < 0.9: #prints a report based on the pitch
        if PaceFactor*SpinFactor > 0.7:
            print ('Pitch report: good for bowling.')
        else:
            print ('Pitch report: GREAT for bowling.')
    elif PaceFactor < 0.9 and SpinFactor > 0.9:
        if PaceFactor > 0.8:
            print ('Pitch report: Good for seam bowlers.')
        else:
            print ('Pitch report: GREAT for seam bowlers!')
    elif PaceFactor >0.9 and SpinFactor <0.9:
        if SpinFactor > 0.8:
            print ('Pitch report: Good for spinners.')
        else:
            print ('Pitch report: GREAT for spinners.')
    elif PaceFactor*SpinFactor < 1.1:
        print ('Pitch report: even battle between bat and ball.')
    elif PaceFactor*SpinFactor < 1.3:
        print ('Pitch report: good for batting.')
    else:
        print ('Pich report: looks like a road! GREAT for batting.')


Team1Name = ''
Team1Years = ''
x = 0
print ('')
print ('Home Team')
print ('')
    
Players = Choice (x)

if Players != 'recreate':
    x = 0
    while x < 1:
        try: #if the selected team fails, ask again
            SelectedTeam = Select (Players)
            x = 1
        except:
            print ('That combination of year and team is not possible.')
            print ('')
            Players = Choice (x)
    t = DataConvert (SelectedTeam)
    x = 0

    Team1Name = TeamName #putting the data into the right format
    Team1 = t[0]
    Team1BatAvs = t[1]
    Team1BowlAvs = t[2]
    Team1Roles = t[3]
    Team1ERs = t[4]
    Team1Captain = CaptainSelect (SelectedTeam)
    for i in range (0, 11): #selecting the lowest-batting WK to be the keeper
        if 'WK' in t[3][i]:
            Team1WK = t[0][i]
        if t[4][i] == 0: #fixing 0 ERs
            t[4][i] == 0.7


    if FirstYear != LastYear: #setting up the years for the scorecard
        Team1Years = (str(FirstYear)) + ' - ' + str(LastYear)
    else:
        Team1Years = (str(LastYear))

    print ('')

    print ('Away Team')
    print ('')

    x = 0
    while x < 1: #duplicates the process for Team Two
        Players = Choice (x)
        try: #if the selected team fails, add one year on either end and try again
            SelectedTeam = Select (Players)
            x = 1
        except:
            print ('That combination of year and team is not possible.')
    t = DataConvert (SelectedTeam)
    x = 0

    Team2Name = TeamName
    Team2 = t[0]
    Team2BatAvs = t[1]
    Team2BowlAvs = t[2]
    Team2Roles = t[3]
    Team2ERs = t[4]
    Team2Captain = CaptainSelect (SelectedTeam)
    for i in range (0, 11):
        if 'WK' in t[3][i]:
            Team2WK = t[0][i]
        if t[4][i] == 0: #fixing 0 ERs
            t[4][i] == 0.7

else:
    RealTest = RecreateSelect (x)
    #print (RealTest)
    #(ValidTests[q][1], HomeTeamData, HomeCapt, HomeWK, ValidTests[q][2], AwayTeamData, AwayCapt, AwayWK, Year)
    Team1Name = RealTest[0]
    #RealLineup = Select (RealTest[1])
    a = DataConvert(RealTest[1])
    Team1 = a[0]
    Team1BatAvs = a[1]
    Team1BowlAvs = a[2]
    Team1Roles = a[3]
    Team1ERs = a[4]
    Team1Captain = RealTest[2].replace(' (c)','')
    Team1WK = RealTest[3]
    Team1Years = str(RealTest[8])
    Team2Name = RealTest[4]
    #RealLineup = Select (RealTest[5])
    b = DataConvert(RealTest[5])
    Team2 = b[0]
    Team2BatAvs = b[1]
    Team2BowlAvs = b[2]
    Team2Roles = b[3]
    Team2ERs = b[4]
    Team2Captain = RealTest[6]
    Team2WK = RealTest[7]
    FirstYear = RealTest[8]
    LastYear = RealTest[8]

Team1BatAbi = []
Team1BowlAbi = []
for i in range(0,11):
    Team1BatAbi.append((Team1BatAvs[i]/30)) #batting and bowling abilities averaged at 1
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

print('')
PitchReport (PaceFactor, SpinFactor)

PaceFactor = PaceFactor**0.5 #square root applied to both runs/ball and wickets/ball combines to make the average a multiple of the factor
SpinFactor = SpinFactor**0.5

print (' ')
delay = str(input ('Enter "slow" to watch the game in over-by-over mode, or anything else to proceed with quicksim. '))
if delay == 'slow':
    delay = 1 #in seconds at the end of each over, and
else:
    delay = 0





Header = open('scorecard.txt','w') #writing the top lines of the scorecard

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
for i in range (0,11): #setting up the man of the match tracking
    MOMTemp = [Team1[i],0]
    MOMTemp2 = [Team2[i],0]
    MOM.append(MOMTemp)
    MOM.append(MOMTemp2)

def MakeCard (x): #empty batting scorecard
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

def MakeBowlCard (x): #empty bowling scorecard
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

def RunStats (x): #when x runs are scored, add x runs to the batter's total
    global card
    global Bat1
    global Bowl1
    for i in range (0,12):
        if card[i][0] == Bat1:
            card[i][1] = card[i][1] + x
            break

def BallStats (x): #when the batsman faces a ball, add 1 to his balls total
    global card
    global Bat1
    global Bowl1
    for i in range (0,12):
        if card[i][0] == Bat1:
            card[i][2] = card[i][2] + x
            break

def OverStats (x): #add 1 to the bowler's overs column
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

def MaidenStats (x): #add 1 to the bowler's maidens column
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

def BowlWicketStats (x): #add x to the bowler's runs column
    global BowlCard
    for i in range (0,12):
        if BowlCard[i][0] == x:
            BowlCard[i][4] = (BowlCard[i][4] + 1)
            break

x = 0

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

    outcome = random.choice([Team1Name, Team2Name])
    Results = open('scorecard.txt', 'a') #writes the toss result and decision to the scorecard
    print (str(outcome + ' has won the toss.'))
    Results.write((str(outcome + ' has won the toss.')))
    Results.write('\n')
    rand = random.random()
    if outcome == Team1Name and rand > 0.2: #rand decides if to bat or bowl first
        print( str(Team1Captain + ' has elected to bat first.'))
        Results.write(str(Team1Captain + ' has elected to bat first.'))
    elif outcome == Team1Name and rand < 0.2: #if necessary, switches to have the second team batting first
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
    Results.close() #closes scorecard

x = 0
toss (x) #runs toss module

Bat1 = Team1[0] #sets first two batsmen
Bat2 = Team1[1]

Bowl1 = Team2[9] #legacy
Bowl2 = Team2[10]

BatTeam = Team1Name
BowlTeam = Team2Name

Score = 0 #sets variables
Wickets = 0
TotalOvers = 0

GameScores = [] #creates game history
FallOfWicket = [0] #creates FOW log

Innings = 0


#######GAMEPLAY FUNCTIONS START HERE

def ball (x): #function for each ball
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
    global det, AggFactor, PaceFactor, SpinFactor

    for i in range (0, 11): #finds the type of bowler
        if Bowl1 == Team2[i]:
            Bowl1Role = Team2Roles[i]
            break
    det = 1
    Day = -(-(TotalOvers+OverCount+1)//90) #works out what day it is and sets the deteriation modifier
    if 'Spin' in Bowl1Role:
        if Day == 1:
            det = 1.3
        elif Day == 2:
            det = 1.2
        elif Day == 3:
            det = 1.1
        elif Day == 4:
            det = 0.9
        else:
            det = 0.7
    else:
        if Day == 1:
            det = 1.1
        if Day == 2:
            det = 1.05
        if Day == 3:
            det = 1
        if Day == 4:
            det = 0.95
        if Day == 5:
            det = 0.9

    if ('Fast' in Bowl1Role or 'Med' in Bowl1Role) and (OverCount % 80) < 10: #new ball increases wicket chance
        det = det * 0.9

    Position = Team1.index(Bat1)
    if (Bat1 == Team1[0] or Bat1 == Team1[1]) and 'FillIn' in Bat1: #penalises fill-in opener
        BatAbi = Team1BatAbi[Position] - (1/3)
    else:
        BatAbi = Team1BatAbi[Position] #finds the batsman's ability

    #works out the batsman's form - i.e. how set he is at the crease - as a function of runs scored and balls faced. max is 1.1, min is 0.9
    #last variable is a penalty for having played very long innings for tiredness
    Form = 0.9 + min(0.10, (card[Position+1][2]/500)) + min(0.1,(card[Position+1][1]/250)) + min(0, ((200-card[Position+1][2])/2000))
    if ((TotalOvers+OverCount) % 90) < 6: #form can't be > 0.9 for the first five overs of the day
        Form = min(Form, 0.9)

    #print (Form, det, AggFactor)

    BowlPosition = Team2.index(Bowl1)
    BowlER = Team2ERs[BowlPosition] #how good the bowler is at not conceding runs
    BowlAbi = Team2BowlAbi[BowlPosition] / BowlER #how good the bowler is at taking wickets

    #print (BatAbi, BowlER, BowlAbi)

    if 'Spin' in Bowl1Role: #what type of bowler is bowling
        PitchFactor = SpinFactor
    else:
        PitchFactor = PaceFactor

    if 'FakeWK' in Team2Roles: #20% less likely to take a wicket if you don't have a real WK
        AdjustedWkRt = 0.8 * BaseWkRt * (1/(BatAbi**0.8)) * (1/(BowlAbi)) * (1/(det**0.5)) * (1/Form**0.5) *AggFactor * (max(1, AggFactor**2)) * (1/PitchFactor)
    else:
        AdjustedWkRt = BaseWkRt * (1/(BatAbi**0.8)) * (1/(BowlAbi)) * (1/(det**0.5)) * (1/Form**0.5) *AggFactor * (max(1, AggFactor**2)) * (1/PitchFactor)
    Adjusted6Rt = Base6Rt * (BatAbi**0.2) * BowlER * (det**0.5) * (Form**0.5) * AggFactor * PitchFactor #chance of a 6
    Adjusted4Rt = Base4Rt * (BatAbi**0.2) * BowlER * (det**0.5) * (Form**0.5) * AggFactor * PitchFactor #chance of a 4
    AdjustedScrRt = BaseScrRt * (BatAbi**0.2) * BowlER * (det**0.5) * (Form**0.5) * AggFactor * PitchFactor #chance of another type of run

    #batsman ability affects chance to get out more than rate of scoring
    #modifiers are squarerooted on scoring rate and wicket rate, together they affect overall average

    rand = random.random() #number between 0 and 1 to determine ball outcome

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

    elif rand < (AdjustedWkRt + Adjusted6Rt + Adjusted4Rt + (AdjustedScrRt)/1.3):
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
    elif rand < (AdjustedWkRt + Adjusted6Rt + Adjusted4Rt + (AdjustedScrRt)/1.3 + 2*AdjustedWkRt): #2 chances for every wicket on average
        return 'Chance!'

    else:
        return 'No run.'

def ChangeBatsman (x): #runs after a wicket falls
    global Bat1
    global Team1
    global Wickets
    global WicketsOver
    if (Wickets+WicketsOver) == 10: #does nothing if the innings is over
        return Bat1
    x = x
    NextBat = Team1[(Wickets+WicketsOver+1)] #brings the new batsman into the game
    print (' ')
    print (str('New Batsman: ' + str(NextBat))) #tells player
    print (' ')
    return NextBat


def MakeSpellCount (x): #to track the length of active bowling spells
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



FatigueList = [] #the last 30 overs bowled get added to the list

def second_smallest(numbers):
    a1, a2 = float('inf'), float('inf')
    for x in numbers:
        if x <= a1:
            a1, a2 = x, a1
        elif x < a2:
            a2 = x
    return a2

def BowlChoice (x): #function to decide who bowls the next over
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
    Day = -(-(TotalOvers+OverCount+1)//90) #modifier in use for spinners
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

    if Innings > 1 and OverCount == 0: #pick new bowlers at the start of the inning
        Bowl1 = ''
        Bowl2 = ''

    for i in range (0,12):
        if SpellCount[i][0] == Bowl2 and OverCount != 0: #add one to the spell count of the bowler who bowled the last over
            SpellCount[i][1] = SpellCount[i][1] + 1

    if OverCount % 80 < 2: #when the new ball comes, much less likely spinners to start
        import copy
        OpenAvs = copy.deepcopy(Team2BowlAvs)
        for i in range(0,11):
            if 'Spin' in Team2Roles[i] or 'Bat' in Team2Roles[i]:
                OpenAvs[i] = OpenAvs[i] + 50

    if OverCount == 0: #pick the best non-spin bowler for the first over of the innings
        j = min(OpenAvs)
        k = OpenAvs.index(j)
        return Team2[k]
    elif OverCount == 1: #pick the second best non-spin bowler for the first over of the innings
        j = second_smallest(OpenAvs)
        k = OpenAvs.index(j)
        return Team2[k]
    for i in a: #find which player on the bowling card bowled last from this end
        if Team2[i] == Bowl1:
            y = i
        if BowlCard[i][0] == Bowl1:
            BowlCardNo = i
        if OverCount < 2:
            BowlCardNo = 2

    if BowlCard[BowlCardNo][3] != 0: #calculates if the bowler has conceded more than 4RPO
        if (BowlCard[BowlCardNo][3]/BowlCard[BowlCardNo][1]) > 4:
            ExcessRPO = BowlCard[BowlCardNo][3] - 4*BowlCard[BowlCardNo][1]
        else:
            ExcessRPO = 0
    else:
        ExcessRPO = 0

    #z^2 is the probability (0-100) that a bowler will be removed from the attack

    #if 'Fast' not in Team2Roles[y] and 'Part' not in Team2Roles[y] and 'Bat' not in Team2Roles[y]:
#        z = SpellCount[(y+1)][1] - BowlCard[BowlCardNo][4] + (ExcessRPO)/4
 #   else:
    z = SpellCount[y+1][1] - BowlCard[BowlCardNo][4] + (ExcessRPO)/4 #base is Spell Length - Wickets + ExcessRPO
    if 'Part' in Team2Roles[y]: #add 2 if a part-timer
        z = z+2
    if 'Bat' in Team2Roles[y]: #add 3 if a batsman (non-part-timer or all-rounder)
        z = z+3
    z = z**2 #square z
    if OverCount % 80 < 2: #pick a new bowler every new ball
        Bowl1 = ''
        z = 100
    if 'Fast' in Team2Roles[y]: #fast bowlers get tired more quickly
        z = 1.5*z

    #print (z)
    prob = (int(z)/100)
    if random.random() < prob: #if the bowler needs to be changed
        t = 0
        q = 11 #starting with the #11 in the bowling team's lineup
        while t == 0: #loops until a new bowler is chosen
            for i in range (0,10):
                if Team2[q-1] == BowlCard[i][0]: #find the player's spot in the bowling card
                    CardNo = i
                    break
                else:
                    CardNo = 12

                # print (q, CardNo)



                if BowlCard[CardNo][1] != 0: #if the bowler has bowled ing the innings
                    if (BowlCard[CardNo][3]/BowlCard[CardNo][1]) > 4:
                        ExcessRPO = BowlCard[CardNo][3] - 4*BowlCard[CardNo][1] #Runs conceded above 4/over
                    else:
                        ExcessRPO = 0
                else:
                    ExcessRPO = 0

                #this section converts a player's innings stats and abilities into d - a modified average. lower is better.
                if 'Fast' in Team2Roles[q-1]: #bowling av + overs in the last 30 bowled squared + excess rpo - 2*wickets taken + 5*currentspelllength
                    d = Team2BowlAvs[(q-1)] + (FatigueList.count((Team2[(q-1)]))**2) + ExcessRPO - 2*BowlCard[CardNo][4] + 5*SpellCount[q][1]
                else: #non fast bowlers tire quicker
                    d = Team2BowlAvs[(q-1)] + ((FatigueList.count((Team2[(q-1)]))**2)/5) + ExcessRPO - 2*BowlCard[CardNo][4] + 2*SpellCount[q][1]
                if 'Part' in Team2Roles[q-1]: #part timers should be penalized
                    d = d+20
                if 'Bat' in Team2Roles[q-1]: #batsmen even more so
                    d = d+50
                if (OverCount % 80) < 15 and 'Spin' in Team2Roles[q-1]: #spinners penalized in the first 15 overs
                    d = d+50
                elif (OverCount % 80) < 25 and 'Spin' in Team2Roles[q-1]: #and a bit less for the first 25
                    d = d+25
                if Team2[q-1] == Bowl1: #bowling is changing
                    d = 500
                if OverCount < 50 and ('Part' in Team2Roles[q-1] or 'Bat' in Team2Roles[q-1]): #less likely to pick rare bowler in first 50 overs
                    d = d+100
                Partnership = (Score+RunsOver) - FallOfWicket[-1]
                if Partnership > 150 and ('Part' in Team2Roles[q-1] or 'Bat' in Team2Roles[q-1]): #but more likely to try and break a long partnership
                    d = d-20
                if 'Spin' in Team2Roles[q-1]: #spin bowlers adjusted for what day it is
                    d = d*det*(SpinFactor**2)
                else: #spin and pace adjusted for the pitch 
                    d = d*(PaceFactor**2)
                # print (d)

                if d <= 40: #converts d into a probability
                    c = 0.5 + ((40-d)/50)
                elif d <= 80:
                    c = 0.5 - ((d-40)/100)
                else:
                    c = 0.1 - ((d-80)/1500)

                if c <= 0:
                    c = (1/1500)

                b = random.random()
                if b < c and SpellCount[q][0] != Bowl2 and SpellCount[q][0] != Team2WK: #sees if the probability is  met
                    t = 1
                    if SpellCount[q][0] !=Bowl1:
                        print (str('New Bowler: ') + str(SpellCount[q][0])) #and brings the bowler on to bowl
                        print (' ')
                        SpellCount[(y+1)][1] = 0
                    return SpellCount[q][0]
                if q > 1: #iterates from the bottom of the lineup to the top
                    q = q-1
                else: #then goes back to the top
                    q = 11
    else: #if the bowler isn't being brought off
        return Bowl1



def Wicket (x,y): #this function decides the details on a dismisall if ball() decides the batsmen should be out
    global Team1
    global Team2
    global Team2WK
    global Team2Roles
    global card, BowlCard
    name = Team1.index(x) + 1 #finds the batsman's place in the lineup
    card[name][3] = 1 #switches the batsman's line in the card to say he is out
    rand = random.random() #between 0 and 1
    for i in range(0,12): #finds the bowler's place in bowlcard
        if y == BowlCard[i][0]:
            PlayerNumber = i
            break
    Role = Team2Roles[PlayerNumber] #finds what type of bowler the bowler is
    #all probabilities are derived from all time statistics
    if rand < 0.2143: #bowled
        card[name][4] = str('b. ' + str(y))
        LastWicket[2] = str('b. ' + str(y))
        return str('b. ' + str(y))
    elif rand < 0.3573: #lbw
        card[name][4] = str('lbw. b. ' +str(y))
        LastWicket[2] = str('lbw. b. ' +str(y))
        return str('lbw. b. ' +str(y))
    elif rand < 0.52: #caught behind
        card[name][4] = str('c. ' + str(Team2WK) + ' b. ' +str(y))
        LastWicket[2] = str('c. ' + str(Team2WK) + ' b. ' +str(y))
        return str('c. ' + str(Team2WK) + ' b. ' +str(y))
    elif rand < 0.9065: #caught by a fielder (all non WKs currently have an even chance)
        Fielder = random.choice(Team2)
        if Fielder != y:
            card[name][4] = str('c. ' + str(Fielder) + ' b. ' + str(y))
            LastWicket[2] = str('c. ' + str(Fielder) + ' b. ' + str(y))
            return str('c. ' + str(Fielder) + ' b. ' + str(y))
        else: #caught and bowled
            card[name][4] = str('c. & b. ' +str(y))
            LastWicket[2] = str('c. & b. ' +str(y))
            return str('c. & b. ' +str(y))
    elif rand < 0.9568: #adjusted by +0.01 #stumped if a spinner
        if random.random() > 0.9 and ('Med' in Role or 'Spin' in Role):
            card[name][4] = str('st. ' + str(Team2WK) + ' b. ' +str(y))
            LastWicket[2] = str('st. ' + str(Team2WK) + ' b. ' +str(y))
            return str('st. ' + str(Team2WK) + ' b. ' +str(y))
        else: #else bowled
            Fielder = random.choice(Team2)
            if Fielder != y:
                card[name][4] = str('c. ' + str(Fielder) + ' b. ' + str(y))
                LastWicket[2] = str('c. ' + str(Fielder) + ' b. ' + str(y))
                return str('c. ' + str(Fielder) + ' b. ' + str(y))
            else:
                card[name][4] = str('c. & b. ' +str(y))
                LastWicket[2] = str('c. & b. ' +str(y))
                return str('c. & b. ' +str(y))
    elif rand < 0.9919: #adjusted by +0.01 #run out
        Fielder = random.choice(Team2)
        card[name][4] = str('run out ('+str(Fielder) + ')')
        LastWicket[2] = str('run out ('+str(Fielder) + ')')
        BowlCard[(PlayerNumber)][4] = (BowlCard[(PlayerNumber)][4] - 1)
        return str('run out ('+str(Fielder) + ')')
    else: #hitwicket has been adjusted down because i felt like it was happening too often
        card[name][4] = str('hit wicket b. ' + str(y))
        LastWicket[2] = str('hit wicket b. ' + str(y))
        return str('hit wicket b. ' + str(y))


def milestone (x): #this is called after every ball. it checks if the batsman or partnership passed a multiple of 50
    global RunsOver, WicketsOver, card, Bat1, FallOfWicket, Score, Wickets
    for i in range(1,12): #find the batsman's scorecard line
        if Bat1 == card[i][0]:
            PlayerNo = i
            break
    if x == '1 run.': #the input is the return from ball()
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
    if (BatsmanScore % 50) < j: #if he passed a multiple of 50 on the last ball
        print (' ')
        print (str('Milestone: ' + str(card[PlayerNo][0]) + ' ' + str(card[PlayerNo][1]) + '* (' + str(card[PlayerNo][2]) + ')'))
        print (' ')
        import time
        time.sleep(delay)

    Partnership = (Score+RunsOver) - FallOfWicket[-1]
    if (Partnership % 50) < j: #if the partnership passed a multiple of 50 on the last ball
        print (' ')
        print (str('Partnership: ' + str(Partnership) + ' (' +str(LastWicket[3]) + ' balls)'))
        if Wickets > 0:
            print ( str( 'Last Wicket: '+ str(LastWicket[0]) + '/' + str(Wickets)+' - ' + str(LastWicket[1]) + ' ' + str (LastWicket[2]) + ' '+ str(LastWicket[4])))
        print (' ')
        import time
        time.sleep(delay)


# ['Score at Last Wicket', 'Last Man Out', 'How Last Man Out', 'Balls Since Last Wicket'

LastWicket = [0,'','',0,'']

def declare (x): #called after every over and at the fall of each wicket. decides if the batting team should declare or not
    global card, Bat1, Bat2, Innings, Score, GameScores, TotalOvers, GameOvers, OverCount
    import random
    a = 0
    b = 0
    for i in range (1, 11): #finds each batsman's score
        if Bat1 == card[i][0]:
            a = card[i][1]
        if Bat2 == card[i][0]:
            b = card[i][1]
    if (a % 100 > 89) or (b % 100 > 89): #doesn't declare if a batsman is near a century
        return 'continue'
    if Innings == 0 and (Score > 500 or OverCount > 150 ) and random.random() < (Score/50000): #1st innings declarations getting more likely from 500 runs or 150 overs
        print ('')
        print ('Innings declared.')
        return 'declare'
    if Innings == 1 and Score > 500 and (Score-GameScores[1] > -50) and random.random() < 0.1: #can declare 50 behind if score > 500 in second innings
        print ('')
        print ('Innings declared.')
        return 'declare'
    if Innings == 1 and ((Score/GameScores[1]) > 2) and OverCount > 100 and random.random() < 0.02: #or if they've doubled up a team's score after 100 overs
        print ('')
        print ('Innings declared.')
        return 'declare'
    if Innings == 2 and ((3*(GameOvers-TotalOvers-OverCount)) + 50 < (GameScores[1]+Score-GameScores[5])) and random.random() < 0.2 and FollowOn == False:
        print ('') #starts deciding to declare when the target would be 3 RPO + 50
        print ('Innings declared.')
        return 'declare'


def over (x): #module calls or contains everything to run an over
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

    c = 0 #c is the balls in an over count
    RunsOver = 0
    WicketsOver = 0

    r = BowlChoice (x) #runs the function that chooses the bowler
    Bowl1 = r
    BowlName = Bowl1
    o = Team2.index(Bowl1) #bowler's postion in the side
    print (str('Over ' + str (x) + ': '+str(Bowl1) + ' to bowl. ' +str((SpellCount[o+1][1])) + ' overs in spell so far.'))
    import time
    time.sleep(delay/2)
    OverStats (Bowl1) #add one to the bowler's over count
    FatigueList.append(Bowl1) #add this over to the fatigue list
    if len(FatigueList) > 25: #remove the oldest over in the fatigue list, which lists the last 25 overs bowled
        FatigueList.pop(0)

    AggFactor = 1 #AggFactor is the aggression of the batting team. it modifies runs and wickets
    #INNINGS COUNTING STARTS AT ZERO
    if Innings < 3:
        if Score > 400: #start pushing the pace once you get past 400
            AggFactor = 1 + (Score-400)/500
        if Wickets > 1 and (Score/Wickets) < 15: #play carefully if in early trouble
            AggFactor = 0.8
    elif Innings == 2: #batting third, push the pace when you get a lead of 250
        if Score + GameScores[1] - GameScores[5] > 250:
            AggFactor = 1 + (Score-250)/500
    else: #fourth innings
        Target = (GameScores[1]+GameScores[9]-GameScores[5]+1)
        RemainingOvers = (GameOvers-TotalOvers-OverCount)
        if RemainingOvers == 0: #to avoid div/0 errors
            RemainingOvers = 1
        if (Target-Score)/RemainingOvers > 6 and RemainingOvers > 15: #if the target is ungettable, play for a draw
            AggFactor = 0.7
        if Wickets > 6 and Target-Score > 50 and RemainingOvers < 50: #if close to losing, play carefully
            AggFactor = 0.7
        if (Target-Score)/RemainingOvers < (10-Wickets) and RemainingOvers < 25: #if you need to push the pace, bat harder
            if RemainingOvers <= 5 and (Target-Score) < 50 and Wickets < 8:
                AggFactor = 1 + 2*((Target-Score)/RemainingOvers)
            else:
                AggFactor = 1+((10-Wickets)/10)

    while c < 6: #runs six times for an over
        dec = 0
        y = (ball (c)) #run the ball() function
        print (str('Ball ' +str(c+1)+ ': ' +str(Bowl1) + ' to ' + str (Bat1) + ': ' +str(y))) #print the result
        milestone (y) #check for a milestone
        LastWicket[3] = LastWicket[3] + 1 #add one to the number of balls in the partnership
        if y == 'WICKET!!!' and (Wickets+WicketsOver) <= 9: #do this if a wicket falls and the innings isn't over
            x = int(Wickets + 2)

            b = range(1,11)
            for i in b: #find the batsman's place in the batting card
                if card[i][0] == Bat1:
                    z = i
            Dismissal = Wicket (Bat1, Bowl1) #find the wicket type
            print (' ') #print it
            print (str(card[z][0] + ' ' + str(Dismissal) + ' ' + str(card[z][1]) + ' (' + str(card[z][2]) + ')'))
            Partnership = (Score+RunsOver) - FallOfWicket[-1]
            print (str('Partnership: ' + str(Partnership) + ' (' +str(LastWicket[3]) + ' balls)')) #print the partnership
            print (str(str(BatTeam)+' ' +str(Score+RunsOver)+'/' + str(Wickets+WicketsOver)))
            if (Wickets+WicketsOver) > 1: #add the score to the fall of wicket log
                FallOfWicket.append(Score+RunsOver)
            elif (Wickets+WicketsOver) == 1:
                FallOfWicket[0] = (Score+RunsOver)
            LastWicket[0] = (Score+RunsOver) #adjust the last wicket tracker
            LastWicket[1] = Bat1
            LastWicket[3] = 0
            for i in range (0,11):
                if card[i][0] == Bat1:
                    #print (card)
                    LastWicket[4] = card[i][1]
                    break
            if declare(x) == 'declare': #check to see if the team should declare
                c = 6 #if yes, end the over
                dec = 1

            Bat1 = ChangeBatsman (x) #bring in the new batsman
            import time
            time.sleep(delay)

        if y == 'WICKET!!!' and (Wickets+WicketsOver) > 9: #if the innings is over
            print ('')
            b = range(1,12)
            for i in b:
                if card[i][0] == Bat1:
                    z = i
            Dismissal = Wicket (Bat1, Bowl1) #decide and record the wicket
            print (str(card[z][0]  + ' ' + str(Dismissal) + ' ' + str(card[z][1]) + ' (' + str(card[z][2]) + ')'))
            Partnership = (Score+RunsOver) - FallOfWicket[-1]
            print (str('Partnership: ' + str(Partnership) + ' (' +str(LastWicket[3]) + ' balls)'))

            FallOfWicket.append(Score+RunsOver) #end innings
            print ('')
            print ('All Out.')
            print ('')
            break


        c = c + 1 #increase the ball counter
        if y == '1 run.' or y == '3 runs.': #if there's an odd number of runs, change who is on strike
            Bat1, Bat2 = Bat2, Bat1

        if Innings == 3 and FollowOn == False and ((int(Score+RunsOver)+GameScores[5]) > (GameScores[1] + GameScores[9])): #check if the game is over
            c = 6
        if Innings == 3 and FollowOn == True and (int(Score+RunsOver)+GameScores[1]) > (GameScores[5]+GameScores[9]):
            c = 6
        import time
        time.sleep(delay/2) #if in over-by-over mode, pause

    OverCount = OverCount+1
    if RunsOver == 0: #if a maiden, add to the maiden counter
        MaidenStats (Bowl1)
    BowlRunsStats (RunsOver) #add to the bowler's runs counter

    Score = Score + RunsOver #change the innings totals
    Wickets = Wickets + WicketsOver

    import time
    time.sleep(delay/3)
    if Wickets  != 10: #print over stats
        if WicketsOver == 0:
            print (str(str(RunsOver)+ ' runs from the over. ' +str(BatTeam)+' ' +str(Score)+'/' + str(Wickets)+ ' after ' +str(x) + ' overs. (' +str(round((Score/(OverCount+1)),1)) + ' RPO)'))
        elif WicketsOver == 1:
            print (str(str(RunsOver)+ ' runs and ' +str(WicketsOver)+ ' wicket from the over. ' +str(BatTeam)+' ' +str(Score)+'/' + str(Wickets)+ ' after ' +str(OverCount) + ' overs. (' +str(round((Score/(OverCount+1)),1)) + ' RPO)'))
        else:
            print (str(str(RunsOver)+ ' runs and ' +str(WicketsOver)+ ' wickets from the over. ' +str(BatTeam)+' ' +str(Score)+'/' + str(Wickets)+ ' after ' +str(OverCount) + ' overs. (' +str(round((Score/(OverCount+1)),1)) + ' RPO)'))
    # print (FallOfWicket)

    if Wickets > 0: #print the last wicket details
        print ( str( 'Last Wicket: '+ str(LastWicket[0]) + '/' + str(Wickets)+' - ' + str(LastWicket[1]) + ' ' + str (LastWicket[2]) + ' '+ str(LastWicket[4])))

    a = range (1,12) #print the bowler's stats
    for i in a:
        if BowlCard[i][0] == BowlName:
            print (str(str(BowlName) + ' ' +str(BowlCard[i][1]) + ' - ' +str(BowlCard[i][2]) + ' - ' +str(BowlCard[i][3]) + ' - ' + str(BowlCard[i][4])))
            break

    #change ends
    Bowl1, Bowl2 = Bowl2, Bowl1
    Bat1, Bat2 = Bat2, Bat1
    BowlName = Bowl1


    if (len(Bat1) > len(Bat2)): #format the batsmen's score outpets
        LongerName = len(Bat1)
    else:
       LongerName = len(Bat2)

    time.sleep(delay/3)
    for i in a: #print both batsmen's scores
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
    if Innings == 1: #print scores so far
        print ()
        print(str(str(GameScores[0]) + ' ' + str(GameScores[1]) + '/' + str(GameScores[2]) + ' [' + str(GameScores[3]) +']' ))
        print(str(BatTeam)+' ' +str(Score)+'/' + str(Wickets)+ ' [' +str(OverCount) + ']')
        if (Score > GameScores[1]):
            print(str((BatTeam) + ' leads by ' + str((Score-GameScores[1])) + ' runs.'))
        elif (GameScores[1] > Score):
            print(str((BatTeam) + ' trails by ' + str((GameScores[1]-Score)) + ' runs.'))
        else:
            print('Scores level.')

    if Innings == 2: #print scores so far
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

    if Innings == 3: #print scores so far and target required
        print ()
        print(str(str(GameScores[0]) + ' ' + str(GameScores[1]) + '/' + str(GameScores[2]) + ' [' + str(GameScores[3]) +']' ))
        print(str(str(GameScores[4]) + ' ' + str(GameScores[5]) + '/' + str(GameScores[6]) + ' [' + str(GameScores[7]) +']' ))
        print(str(str(GameScores[8]) + ' ' + str(GameScores[9]) + '/' + str(GameScores[10]) + ' [' + str(GameScores[11]) +']' ))
        print(str(BatTeam)+' ' +str(Score)+'/' + str(Wickets)+ ' [' +str(OverCount) + ']')
        if (TotalOvers+OverCount) < GameOvers and (Score+GameScores[5]) <= (GameScores[1]+GameScores[9]) and Wickets != 10 and FollowOn == False:
            print(str(BatTeam)+ ' require ' + str((GameScores[1]+GameScores[9]-GameScores[5]-Score+1)) + ' more runs in ' +str((GameOvers-TotalOvers-OverCount)) + ' overs.')
        if (TotalOvers+OverCount) < GameOvers and (Score+GameScores[5]) <= (GameScores[1]+GameScores[9]) and Wickets != 10 and FollowOn == True:
            print(str(BatTeam)+ ' require ' + str((GameScores[5]+GameScores[9]-GameScores[1]-Score+1)) + ' more runs in ' +str((GameOvers-TotalOvers-OverCount)) + ' overs.')

    print ('')
    if declare (x) == 'declare': #decide if to declare
        dec = 1

    Day = -(-(TotalOvers+OverCount)//90)
    if (TotalOvers+OverCount)% 90 == 0 and TotalOvers+OverCount != 0:
        print (str( ('End of day ' + str(Day) + '.')))
        print ('')
    
    import time
    time.sleep(2.5 * delay) #pause if in over-by-over


def innings (BatTeam): #contains each innings
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
    card = MakeCard(x) #sets scorecards to empty
    BowlCard = MakeBowlCard(x)
    SpellCount = MakeSpellCount(x)
    OverCount = 0
    overs = range(1,(GameOvers+1))
    for i in overs: #runs over() until innings is over or game is over. most of the output happens in this little block
            over (i)
            if Wickets > 9:
                break
            if Innings == 3 and (int(Score)+GameScores[5]) > ((GameScores[1] + GameScores[9])) and FollowOn == False:
                break
            if Innings == 3 and (int(Score)+GameScores[1]) > ((GameScores[5] + GameScores[9])) and FollowOn == True:
                break
            if GameOvers <= OverCount+TotalOvers or dec == 1: #stop the innings if the team declares or the game is over
                break

    Results = open('scorecard.txt', 'a') #write header line of innings on scorecard
    if Innings < 2:
        print (str(' '+Team1Name + ' - 1st innings'))
        Results.write(str(' '+Team1Name+ ' - 1st innings'))
    elif Innings == 2 and FollowOn == False:
        print (str(' '+Team1Name + ' - 2nd innings'))
        Results.write(str(' '+Team1Name + ' - 2nd innings'))
    elif Innings == 2 and FollowOn == True:
        print (str(' '+Team1Name + ' - 2nd innings (following on)'))
        Results.write(str(' '+Team1Name + ' - 2nd innings (following on)'))
    elif Innings ==3 and FollowOn == False: #prints final innings target to scorecord
        print (str(' '+Team1Name + ' - 2nd innings (Target: ' + str(GameScores[1]+GameScores[9]-GameScores[5]+1) + ')'))
        Results.write(str(' '+Team1Name + ' - 2nd innings (Target: ' + str(GameScores[1]+GameScores[9]-GameScores[5]+1)) + ')')
    elif Innings ==3 and FollowOn == True:
        print (str(' '+Team1Name + ' - 2nd innings (Target: ' + str(GameScores[5]+GameScores[9]-GameScores[1]+1) + ')'))
        Results.write(str(' '+Team1Name + ' - 2nd innings (Target: ' + str(GameScores[5]+GameScores[9]-GameScores[1]+1)) + ')')

    Results.write('\n')
    a = range (1,12) #for each batsman in the lineup
    for i in a:
        if card[i][2] > 0 and card[i][4] == '': #not out if they faced at least one ball and don't have a wicket recorded
            card[i][4] = 'not out'
        if card[i][0] == Team1Captain and card[i][0] == Team1WK: #for captain or keeper
            prefix = '*+'
        elif card[i][0] == Team1Captain:
            prefix = '*'
        elif card[i][0] == Team1WK:
            prefix = '+'
        else:
            prefix = ' '
        NameFormat = str(card[i][0]) #name from batting card
        NameLength = max(len(s) for s in Team1)
        if prefix == '*+':
            NameFormat = NameFormat.ljust(NameLength)
        else:
            NameFormat = NameFormat.ljust(NameLength+1) #column should be as wide as the longest name + 1
        DismissalFormat = str(card[i][4])
        BowlNameLength = 0
        for t in range(1,12):
            if len(card[t][4]) > BowlNameLength:
                BowlNameLength = len(card[t][4]) #find the longest dismissal

        DismissalFormat = DismissalFormat.rjust(3+BowlNameLength) #wicket description column length
        RunsFormat = str(card[i][1])
        RunsFormat = RunsFormat.rjust(3) #3 digits space in runs column
        BallsFormat = str(' (' + str(card[i][2]) + ')' )
        BallsFormat = BallsFormat.rjust(6) #6 digits space including brackets in runs column

        print (str(prefix) + NameFormat + ' ' + DismissalFormat + ' ' + RunsFormat + BallsFormat) #print and write the scorecard for each player
        Results.write(str(prefix) + NameFormat + ' ' + DismissalFormat + ' ' + RunsFormat + BallsFormat)
        Results.write('\n')

    if Innings < 3 and dec == 1: #write the number of wickets and overs and if the innings was declared
        print (str(('(' + str(Wickets) + ' wickets declared - '+str(OverCount) +' overs)  '+str(Score) )).rjust(NameLength+BowlNameLength+10))
        Results.write (str(('(' + str(Wickets) + ' wickets declared - '+str(OverCount) +' overs)  '+str(Score) )).rjust(NameLength+BowlNameLength+10))
    else:
        print (str(('(' + str(Wickets) + ' wickets - '+str(OverCount) +' overs)  '+str(Score) )).rjust(NameLength+BowlNameLength+10))
        Results.write (str(('(' + str(Wickets) + ' wickets - '+str(OverCount) +' overs)  '+str(Score) )).rjust(NameLength+BowlNameLength+10))
    print (' ')
    Results.write('\n')

    if Wickets > 0: #print and write fall of each wicket
        for w in range (0,(len(FallOfWicket))):
            print (str(' ' + str(FallOfWicket[w]) + '-' + str(w+1) + ' '), end=''),
            Results.write(str(' ' + str(FallOfWicket[w]) + '-' + str(w+1) + ' '))
        print (' ')
        Results.write('\n')
    else:
        Results.write('\n')


    Results.write('\n')
    print (' ')

    for i in a:
        if (BowlCard[i][1]) > 0: #writes the bowling figures
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
    import time
    time.sleep(delay*2)

    print ('') #results
    if Innings == 3 and Wickets == 10 and ((GameScores[1] + GameScores[9]) > (Score+GameScores[5])) and FollowOn==False: #if the team batting fourth is bowled out
        print (str(str(BowlTeam) + ' wins by ' +str((GameScores[1] + GameScores[9])-(Score+GameScores[5]))) + ' runs.')
        Results.write((str(str(BowlTeam) + ' wins by ' +str((GameScores[1] + GameScores[9])-(Score+GameScores[5]))) + ' runs.'))
        for i in range (0, 22): #Man of Match winning team bonus
            if MOM[i][0] in Team2:
                MOM[i][1] = MOM[i][1] + 100
    elif Innings == 3 and (Score+GameScores[5]) > ((GameScores[1] + GameScores[9])) and FollowOn==False: #if team batting fourth wins
        print (str(str(BatTeam) + ' wins by ' +str(10-Wickets) + ' wickets.'))
        Results.write ((str(str(BatTeam) + ' wins by ' +str(10-Wickets) + ' wickets.')))
        for i in range (0, 22):
            if MOM[i][0] in Team1:
                MOM[i][1] = MOM[i][1] + 100
    elif Innings == 3 and (Score+GameScores[1]) > ((GameScores[5] + GameScores[9])) and FollowOn==True: #if team batting fourth after enforcing follow-on wins
        print (str(str(BatTeam) + ' wins by ' +str(10-Wickets) + ' wickets.'))
        Results.write ((str(str(BatTeam) + ' wins by ' +str(10-Wickets) + ' wickets.')))
        for i in range (0, 22):
            if MOM[i][0] in Team1:
                MOM[i][1] = MOM[i][1] + 100
    elif Innings == 3 and FollowOn==True and Wickets == 10 and (Score+GameScores[1]) < (GameScores[5] + GameScores[9]): #if team follows on and wins
        print (str(str(BowlTeam) + ' wins by ' +str((GameScores[5] + GameScores[9])-(Score+GameScores[1]))) + ' runs.')
        Results.write((str(str(BowlTeam) + ' wins by ' +str((GameScores[5] + GameScores[9])-(Score+GameScores[1]))) + ' runs.'))
        for i in range (0, 22): #Man of Match winning team bonus
            if MOM[i][0] in Team2:
                MOM[i][1] = MOM[i][1] + 100
    elif Innings == 3 and (Score+GameScores[5]) == GameScores[1]+GameScores[9]: #if a tie
        print ('Match tied.')
        Results.write('Match tied.')
    if Innings == 0:
        print(str(BatTeam)+' ' +str(Score)+'/' + str(Wickets)+ ' [' +str(OverCount) + ']')

    Results.close()

def switch (a): #this is the module which swaps sides to start a new innings. runs differently for the follow-on
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

    if FollowOn == False: #add data to the game scores log
        GameScores.append(BatTeam)
        GameScores.append(Score)
        GameScores.append(Wickets)
        GameScores.append(OverCount)
    Score = 0
    Wickets = 0
    if FollowOn == False:
        for i in range (0, 11): #add to the man of the match points
            for j in range (0, 22):
                if card[i][0] == MOM[j][0]:
                    if Innings < 2:
                        MOM[j][1] = MOM[j][1] + card[i][1] #1 point for 1st or second innings runs
                    elif Innings == 2:
                        MOM[j][1] = MOM[j][1] + 1.5*card[i][1] #1.5 points for 3rd innings runs
                    else:
                        MOM[j][1] = MOM[j][1] + 2*card[i][1] #2 points for 4th innings runs
                if BowlCard[i][0] == MOM[j][0]: #bowlers
                    MOM[j][1] = MOM[j][1] + 25*int(BowlCard[i][4]) #25 points per wicket
                    MOM[j][1] = MOM[j][1] + 1.5*BowlCard[i][1] #1.5 points per over bowled
                    MOM[j][1] = MOM[j][1] - (BowlCard[i][3])/2 #-0.5 points per runs conceded. 3RPO = break even

    TotalOvers = TotalOvers + OverCount #TotalOvers is the game's over count

    OverCount = 0

    Team1, Team2 = Team2, Team1 #swap everything
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

    Bat1 = Team1[0] #opening batsmen in
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
    if Innings < 3:
        print ('CHANGE OF INNINGS')
        print ()


WinningTeam = []
FollowOn = False
innings (BatTeam) #innings 1
if GameOvers < OverCount+TotalOvers: #if a draw
    print ('Match Drawn.')
    Results = open('scorecard.txt', 'a')
    Results.write('Match Drawn.')
    Results.close()
else:
    switch (x)
    innings (BatTeam) #innings 2
    switch (x)
    if GameOvers <= OverCount+TotalOvers and Wickets != 10:
        print ('Match Drawn.')
        Results = open('scorecard.txt', 'a')
        Results.write('Match Drawn.')
        Results.close()
    elif GameScores[1] - GameScores[5] > 200: #does the follow-on need to be enforced?
        FollowOn = True
        print ('Follow-on enforced.')
        switch (x)
        innings (BatTeam) #innings 3
        if GameOvers <= OverCount+TotalOvers and Wickets != 10:
            print ('Match Drawn.')
            Results = open('scorecard.txt', 'a')
            Results.write('Match Drawn.')
            Results.close()
        elif Score + GameScores[5] >= GameScores[1]:
            FollowOn = False
            switch (x)
            FollowOn = True
            innings (BatTeam) #innings four
        elif Score + GameScores[5] < GameScores[1] and Wickets == 10:
            FollowOn=False
            switch (x)
            Results = open('scorecard.txt', 'a')
            print (str( str(BatTeam) + ' wins by an innings and ' + str(GameScores[1]-(GameScores[5] + GameScores[9])) + ' runs.'))
            Results.write(str( str(BatTeam) + ' wins by an innings and ' + str((GameScores[1]-GameScores[5]-GameScores[9]))     + ' runs.'))
            Results.close()
            WinningTeam = BowlTeam
    else:
        innings(BatTeam) #innings3
        if Score + GameScores[1] < GameScores[5] and Wickets == 10:
            print (str( str(BowlTeam) + ' wins by an innings and ' + str(GameScores[5]-(GameScores[1] + Score)) + ' runs.'))
            Results = open('scorecard.txt', 'a')
            Results.write(str( str(BowlTeam) + ' wins by an innings and ' + str((GameScores[5]-GameScores[1]-Score))    + ' runs.'))
            Results.close()
            WinningTeam = BowlTeam
        elif GameOvers <= OverCount+TotalOvers and Wickets != 10:
            print ('Match Drawn.')
            Results = open('scorecard.txt', 'a')
            Results.write('Match Drawn.')
            Results.close()
        else:
            switch (x)
            innings (BatTeam) #innings four
            switch (x)


for i in range (0, 22):
    if MOM[i][0] in WinningTeam:
        MOM[i][1] = MOM[i][1] + 100 #winning team gets a 100point MOM bonus

scorecard = []
aa = open('scorecard.txt', 'r')
for line in aa:
    scorecard.append(line)
    
if GameOvers <= OverCount+TotalOvers and 'Match Drawn' not in scorecard:
    print ('Match Drawn.')
    Results = open('scorecard.txt', 'a')
    Results.write('Match Drawn.')
    Results.close()

MOM.sort(key = lambda x: x[1], reverse = True) #sort MOM table by points
#print (MOM)
print ( str ('Man of the Match: ' + str(MOM[0][0]))) #MOM is the highest points scorer
Results = open('scorecard.txt', 'a')
Results.write('\n')
Results.write( str ('Man of the Match: ' + str(MOM[0][0])))
Results.write('\n')
PaceFactor, SpinFactor = PaceFactor**2, SpinFactor**2
Results.write('Pace: {}, Spin: {}'.format(round(PaceFactor,2), round(SpinFactor,2)))
Results.close()
PitchReport (PaceFactor, SpinFactor)
print ('Results saved to scorecard.txt')

print ('')
print ('') #end of program
