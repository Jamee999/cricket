Test match cricket simulator

How to run: Download all the files, and then direct your command line to the folder where the files were downloaded. You may need to download python from https://www.python.org/ first, in order to make it work.

There are several different programs inside the folder. To run them, you will need to enter the name of the file in the command line (eg. historical.py), or possibly 'python3' and then the name of the file (eg. python3 historical.py) depending on your operating system.

List of the different programs that can be run:

**altcricket.py** - Simulate the entire history of Test match cricket, with a number of different alternate historical options.

**custom.py** - Run a game or series of games between custom teams. The teams can be loaded from a textfile, or created using the database of real players.

**customleague.py** - Run a round-robin league between a number of custom teams.

**draft.py** - Draft a team and the program will simulate a league. You can also have the computer draft all the teams.

**historical.py** - Run a game or series of games between historical or all-time teams. 

**historicalleague.py** - Run a round-robin league between a number of historical or all-time teams.


If you manually edit the team data files, you need to then run the **pickleplayers.py** file, before any changes will show up in your sim.

If you ever want to revert back to the cricinfo-scraped data, you can run the **playersconvert.py** file, and the changes you made will disappear.
