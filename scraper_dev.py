# -*- coding: utf-8 -*-
"""
Created on Sat Jun 20 03:48:07 2020

@author: ali_e

Goals:
    
1. Extract name, player, platform and value for metric for 1 page.

2. Figure out where to store the above data.

3. Figure out how to go to the next page.

4. Repeat steps 1-3.

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


#platform classes associated with svg tag
#need this list to ensure the platform tag is selected in the following for loop
platform_classes = ['platform-icon platform-icon platform-atvi', 'platform-icon platform-icon platform-battlenet',
                    'platform-icon platform-icon platform-xbl', 'platform-icon platform-icon platform-psn']

#going to save win data per player as a list of lists which can later be put in a pd DataFrame
#initializing main list
win_data = [['username','platform','wins','matches played']]

player_dict = {}

#for each player on the page...
for player in range(len(data)):
    
    #...get username, wins, matches played (mp) and platform
    username = data[player].find('span', attrs = {'class':'trn-ign__username'}).text
    wins = int((data[player].find('td', attrs = {'class':'stat'}).text).replace(',',''))
    mp = int((data[player].find('td', attrs = {'class':'stat collapse'}).text).replace(',',''))
    #there are many svg tags (e.g. rank, twitch icon) so needed to specify class; then select class 
    #and remove irrelevant info, leaving only the platform name
    platform = (data[player].find('svg', attrs= {'class':platform_classes})['class'][-1]).replace('platform-','')
    #print(username, wins, mp, platform)
    
    #getting lower case username for matching
    username_l = username.lower()
    #determining if player should be added to win_data or not; by default, it is True unless a duplicate exists
    add_player = True
    
    #if the player already exists in the player_dict, then we will not add them to the dict or list but we will update
    #their platform to reflect one of the 3 main ones
    if username_l in player_dict:
        add_player = False
        #...change the platform if the current one is atvi...
        if player_dict[username_l][0] == 'atvi':
            player_dict[username_l] = [platform, wins]
        #...or don't if it is not atvi
        else:
            continue
    #if user is not in dict, add them to dict
    else:
        player_dict[username_l] = [platform, wins]
    
    
    #need to get previous player username and wins to check for duplicates (refer to elif statement below)
    previous_p = data[player - 1].find('span', attrs = {'class':'trn-ign__username'}).text.lower()
    previous_w = int((data[player - 1].find('td', attrs = {'class':'stat'}).text).replace(',',''))
   
    #checking for duplicates by looking at username and number of wins
    if ((username.lower() in previous_p) or (previous_p in username.lower())) and (wins - previous_w in range(-5,6)):
        #if platform is not activision, then one of the main 3 platforms is already identified
        if win_data[-1][1] != 'atvi':
            continue
        #if not, get the relevant platform used by the player
        else:
            win_data[-1][1] = platform
   
    #if no proximate duplicate exists, check that there is no duplicate in the dict and appends their info to the win_data list
    else:
        #if duplicate exists, do not add the player again but make sure the relevant platform is included in the list
        if add_player == False:
            #checking win_data in reverse for the duplicate and then updating the player's platform to the relevant one
            for index in range(len(win_data)-1,-1,-1):
                #print(win_data, len(win_data), index)
                if win_data[index][0].lower() == username_l:
                    win_data[index][1] = player_dict[username_l][0]
                    break
        #if no duplicate exists, add the player to the win_data list
        else:
            win_data.append([username,platform,wins,mp])

'''
Next tasks:

2. Save the data that is being collected (pd DataFrame?, np.array?)
-save in a nested list; then put into dataFrame

3. Cycle through pages and collecting the info 

Completed:
    1. Have to figure out how to deal with duplicates [DONE]
    - if a duplicate exists, remove the activision account as it does not tell us which
    platform the player is on
'''






























