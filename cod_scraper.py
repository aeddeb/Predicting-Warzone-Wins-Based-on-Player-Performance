# -*- coding: utf-8 -*-
"""
Created on Sat Jun 20 03:48:07 2020

@author: ali_e

Goals:
    
1. Extract name, player console and value for metric for 1 page.

2. Figure out where to store the above data.

3. Figure out how to go to the next page.

4. Repeat steps 1-3.

_______________________________________________________________________________

After, need to get other metrics (figure out which ones are needed).

Then, need a way to match the metric to the player and only have 1 instance of their name.
"""

import requests
from bs4 import BeautifulSoup

url = 'https://cod.tracker.gg/warzone/leaderboards/battle-royale/all/Wins?page='

#can later use a loop to go through the pages
page_num = str(1)

page = requests.get(url + page_num)

soup = BeautifulSoup(page.content, 'html.parser')


# ----------------------------------------------------------------------------
# Need to select row and extract console, player name, wins and Matches Played

#each row of player data has a tr tag
data = soup.find_all('tr')
#removing first row which is just the table heading
del data[0]

platform_classes = ['platform-icon platform-icon platform-atvi', 'platform-icon platform-icon platform-battlenet',
                    'platform-icon platform-icon platform-xbl', 'platform-icon platform-icon platform-psn']

#for each player on the page...
for player in data:
    
    #...get username, wins, matches played (mp) and platform
    username = player.find('span', attrs = {'class':'trn-ign__username'}).text
    wins = int((player.find('td', attrs = {'class':'stat'}).text).replace(',',''))
    mp = int((player.find('td', attrs = {'class':'stat collapse'}).text).replace(',',''))
    #there are many tags with svg (e.g. rank, twitch icon) so needed to specify class; then selected class 
    #and removed irrelevant info, leaving only the platform name
    platform = (player.find('svg', attrs= {'class':platform_classes})['class'][-1]).replace('platform-','')
    print(username, wins, mp, platform, round(wins/mp,3))

    
'''
Next tasks:
1. Have to figure out how to deal with duplicates
- if a duplicate exists, remove the activision account as it does not tell us which
platform the player is on

2. Save the data that is being collected (pd DataFrame?, np.array?)

3. Cycle through pages and collecting the info 
'''