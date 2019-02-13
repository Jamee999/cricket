from bs4 import BeautifulSoup
import requests
import re
import datetime

CurrentTime = datetime.datetime.now()
CurrentYear = CurrentYear.year

def get_num(x):
    return int(''.join(ele for ele in x if ele.isdigit()))

def gamescrape (Year):
    url = str('http://stats.espncricinfo.com/ci/engine/records/team/match_results.html?class=1;id='+str(Year)+';type=year')
    r = requests.get(url)
    #print (url)
    data = r.content
    soup = BeautifulSoup(data, 'html.parser')
    games = soup.find(text = 'Team 1').parent.parent.parent.parent.contents[5]
    return games
    

g = open('testmatchlist.txt', 'w')
g.close()

for x in range (1877, CurrentYear+1):
    y = 0
    try:
        games = gamescrape(x)
        y = len(games)
        
    except:
        continue
    z = int((y-1)/2)
    for j in range (1, 2*z, 2):
        try:
            Test = games.contents[j]

            Details = []
            Details.append(x)

            for i in range (1, 4):
                try:
                    Details.append(Test.contents[i].contents[0].contents[0])
                except:
                    continue
            for i in range (6, 14):
                try:
                    Details.append(Test.contents[i].contents[0].contents[0])
                except:
                    continue         
            try:
                Details.append(Test.contents[5].contents[0].contents[0])
                Details.append(str(Test.contents[7])[33:-5])
            except:
                Details.append('Draw')
                Details.append('Draw')
            Details.append(str(Test.contents[11])[20:-5])
            n = get_num(str(Test.contents[13].contents[0])[27:-14])
            #/ci/engine/match/62397.html
            Details.append(n)

            print (Details)
            f = open('testmatchlist.txt', 'a')
            f.write(str(Details))
            f.write('\n')
            f.close()
            
        except:
            continue

