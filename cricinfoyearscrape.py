#scrapes cricinfo statguru to find the average runs/wicket for the 5 years either side of the year input
#runs through the data for all years in test history
#outputs to eradata.txt

from bs4 import BeautifulSoup
import requests
import re

#f = open('eradata.txt','w')
#f.close()

def scrape (Year):

    global ReducedStats
    
    url = str('http://stats.espncricinfo.com/ci/engine/stats/index.html?class=1;filter=advanced;groupby=overall;orderby=runs;spanmax1=31+Dec+' + str(Year+5) + ';spanmin1=01+Jan+' +str(Year-5) +';spanval1=span;template=results;type=bowling')
    r = requests.get(url)
    print (url)
    data = r.content

    soup = BeautifulSoup(data, 'html.parser')

    Average1 = str(soup.find(text = 'Overall figures').parent.parent.contents[5].contents[1].contents[25])
    Average1 = Average1[4:-5]
    Average2 = str(soup.find(text = 'Overall figures').parent.parent.contents[5].contents[1].contents[23])
    Average2 = Average2[4:-5]
    Average3 = str(soup.find(text = 'Overall figures').parent.parent.contents[5].contents[1].contents[27])
    Average3 = Average3[4:-5]
    Average4 = str(soup.find(text = 'Overall figures').parent.parent.contents[5].contents[1].contents[29])
    Average4 = Average4[4:-5]

    Average = Average1

    if 2 < float(Average1) < 5:
        Average = Average1

    if 2 < float(Average2) < 5:
        Average = Average2

    if 2 < float(Average3) < 5:
        Average = Average3

    if 2 < float(Average4) < 5:
        Average = Average4

    f = open('ERdata.txt','a')
    f.write (str(str(Year) + ', '+ str(Average)))
    f.write ('\n')
    f.close()
    print (Year, Average)

#scrape (2018)
    
for i in range (1918 , 2018):
    scrape (i)
