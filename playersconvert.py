import random, pickle
from callcricketnew import player
import pickleplayers

nations = ['england', 'australia', 'southafrica', 'westindies', 'newzealand', 'india', 'pakistan', 'srilanka', 'zimbabwe', 'bangladesh', 'afghanistan', 'ireland']

h = open ('alldata.txt','w')
h.close()

g = open('dob.txt','w')
g.close()

for i in nations:
    country = i

    Lines = []
    with open(str(str(country) + 'players.txt')) as f:
        for line in f:
            Lines.append(line[1:-2])

    #print (Lines[0])

    Years = []

    with open ('eradata.txt') as f:
        for line in f:
            line = line[:-1]
            #print (line)
            x = line.split(', ')
            Years.append(x)
            #print (x)

    ERYears = []
    with open ('er_data.txt') as f:
        for line in f:
            line = line[:-1]
            #print (line)
            x = line.split(', ')
            ERYears.append(x)
            #print (x)
    ERYears.append(['2018','3.11'])
    ERYears.append(['2019','3.11'])
    ERYears.append(['2020','3.11'])

    Averages = []
    MidYear = []

    Players = []
    AllData = []

    for i in range (0, 144):
        Years[i][0] = int(Years[i][0])
        Years[i][1] = float(Years[i][1])
        ERYears[i][0] = float(ERYears[i][0])
        Averages.append(Years[i][1])
        MidYear.append(Years[i][0])
        Years.append(ERYears[i][1])

    for i in range (0, len(Lines)): 
        GameData = []
        Input = Lines[i]
        Set = Input.split(',')
        print (Set)
        Set[0] = Set[0][1:-1]
        Set[1] = Set[1][2:-1]
        for j in range (2, 20):
            try:
                Set[j] = Set[j].strip()
            except:
                Set.append(0)
            try:
                Set[j] = int(Set[j])
            except:
                try:
                    Set[j] = float(Set[j])
                except:
                    try:
                        Set[j] = int(Set[j][1:-1])
                    except:
                        try:
                            Set[j] = float(Set[j][1:-1])
                        except:
                            Set[j] = 0
                                           
        Name = Set[0]
        BowlStyle = Set[1]
        BowlStyle = BowlStyle.lower()
        Tests = Set[2]
        Runs = Set[3] 
        BallsFaced = Set[4] 
        TimesOut = Set[5]
        BallsBowled = Set[6]
        RunsAllowed = Set[7]
        Wickets = Set[8]
        FirstYear = Set[9]
        LastYear = Set[10]
        AvYear = round((FirstYear+LastYear)/2)
        FCGames = Set[11]
        FCRuns = Set[12]
        FCBatAv = Set[13]
        FCWickets = Set[14]
        FCBowlAv = Set[15]
        CaptGames = Set[17]
        WKGames = Set[18]
        OpenInns = Set[19]

        g = open('dob.txt','a')
        dobstats = [Set[0], Set[9], Set[16]]
        print (dobstats)
        g.write (str(dobstats))
        g.write('\n')

        FCBatAv = min(FCBatAv, 50)
        if AvYear > 1900:
            FCBowlAv = max (FCBowlAv, 23)
        else:
            FCBowlAv = max (FCBowlAv, 13)

        print (Set)
        
        GameData.append(Set[0])

        n = MidYear.index(AvYear)
        EraAv = Averages[n]
        AllData.append(Set)
        EconAv = ERYears[n][1]
        #print (EraAv)

        #####
        # FILTER OUT UNWANTED PLAYERS
        #####

        if LastYear < 1:
            continue
     
        ##### 
        

        try:
            RawTestBatAv = (Runs / TimesOut)
        except:
            RawTestBatAv = Runs
        if TimesOut < 35:
            if LastYear >= 2016 and TimesOut < 20:
                x = max(3,(min(FCBatAv/1.25,FCBatAv-10)))
                AdjustedBatAv = ((TimesOut*RawTestBatAv) + ((35-TimesOut)*x))/35
            elif FCGames >= 30:
                x = max((1.75 - (FCGames-30)/750), (4/3))
                AdjustedBatAv = ((TimesOut*RawTestBatAv) + ((35-TimesOut)*(FCBatAv/x)))/35
            elif FCGames < 30:
                AdjustedBatAv = (RawTestBatAv/3) + (FCBatAv/5.25) + 6
        else:
            AdjustedBatAv = RawTestBatAv
        EraAdjustedBatAv = (30/EraAv) * AdjustedBatAv
        EraAdjustedBatAv = round(EraAdjustedBatAv,2)
        GameData.append(EraAdjustedBatAv)

        if Wickets != 0:
            RawBowlAv = (RunsAllowed/Wickets)
        else:
            RawBowlAv = max (40, RunsAllowed)
        if BallsBowled == 0:
            AdjustedBowlAv = 400
        elif FCWickets < 10:
            AdjustedBowlAv = 200
        elif BallsBowled < 10000 and LastYear >= 2016:
            AdjustedBowlAv = max(FCBowlAv*1.25, FCBowlAv+10)
            AdjustedBowlAv = ((RawBowlAv*BallsBowled) + ((10000-BallsBowled)*AdjustedBowlAv))/10000

        elif BallsBowled < 10000 and FCWickets >= 100:
            x = max((4/3), 1.75 - (FCWickets-100)/2000)
            AdjustedBowlAv = ((RawBowlAv*BallsBowled) + ((10000-BallsBowled)*FCBowlAv*x))/10000
            
        elif BallsBowled < 10000 and FCWickets < 100:
            AdjustedBowlAv= (RawBowlAv/3) + (FCBowlAv*(7/12)) + 20
        if BallsBowled > 10000:
            AdjustedBowlAv = RawBowlAv
        EraAdjustedBowlAv = (30/EraAv) * AdjustedBowlAv
        if EraAdjustedBowlAv > 100:
            EraAdjustedBowlAv = 100
        EraAdjustedBowlAv = round(EraAdjustedBowlAv, 2)
        GameData.append(EraAdjustedBowlAv)

        print (Name, Tests)
        if WKGames >= 40 or (WKGames/Tests) >=(1/3):
            Role = 'WK'
        elif (BallsBowled/Tests) < 24:
            Role = 'Bat'
        elif (Wickets/Tests) < 1.5 and ((BallsBowled/Tests) < 90 or EraAdjustedBatAv > 20):
            if 'fast' in BowlStyle:
                Role = 'PartFast'
            elif 'spin' in BowlStyle or 'break' in BowlStyle or 'slow' in BowlStyle:
                Role = 'PartSpin'
            else:
                Role = 'PartMed'
        else:
            if 'fast' in BowlStyle:
                Role = 'Fast'
            elif 'spin' in BowlStyle or 'break' in BowlStyle or 'slow' in BowlStyle:
                Role = 'Spin'
            else:
                Role = 'Med'

        if OpenInns > 50 or (OpenInns/Tests > 0.8):
            Role = 'Open' + Role

        if BallsFaced > 60:
            BatRunsPerBall = (Runs/BallsFaced)*2
        else:
            BatRunsPerBall = 1
        if BatRunsPerBall < 0.5:
            BatRunsPerBall = 0.5
        if BatRunsPerBall > 2:
            BatRunsPerBall = 2

        try:
            BowlER = (RunsAllowed/BallsBowled) / (float(EconAv)/6)
        except:
            BowlER = 1.2

        if BowlER == 0:
            BowlER = 1.2

        if BowlER > 1.2:
            BowlER = 1.2

        if BowlER < 0.8:
            BowlER = 0.8

        GameData.append(Role)
        GameData.append(FirstYear)
        GameData.append(LastYear)
        GameData.append(BatRunsPerBall)
        GameData.append(BowlER)
        GameData.append(CaptGames)
        
        Players.append(GameData)
        
    filename = (str(country) + 'data.txt')
    g = open(filename,'w')
    h = open ('alldata.txt','a')
    for i in range (0, len(Players)):
        g.write(str(Players[i]))
        g.write('\n')
        h.write(str(Players[i]))
        h.write('\n')
    g.close()
    h.close()
    
    

    print (str('Data written to ' +str(country) +'data.txt'))

pickleplayers.run()