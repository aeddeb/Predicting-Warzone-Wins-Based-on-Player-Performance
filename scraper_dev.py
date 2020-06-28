# -*- coding: utf-8 -*-
"""
Created on Sat Jun 20 03:48:07 2020

@author: ali_e

Goals:
    
1. Extract name, player, platform and value for metric for 1 page. [Done]
-for loop below --> converted to function in scraper_functions.py

2. Figure out where to store the above data. [Done]
-temporarily in nested list; then place into Pandas DataFrame

3. Figure out how to go to the next page. [Done]
-cycle through page

4. Repeat steps 1-3. 
-will be developed in cod_scraper.py

After, need to get other metrics (figure out which ones are needed).

Then, need a way to match the metric to the player and only have 1 instance of their name.
"""

import requests
from bs4 import BeautifulSoup
from fuzzywuzzy import fuzz

# ----------------------------------------------------------------------------


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
            player_dict[username_l] = [platform, wins, mp]
        #...or don't if it is not atvi
        else:
            continue
    #if user is not in dict, add them to dict
    else:
        player_dict[username_l] = [platform, wins, mp]
    
    
    #need to get previous player's (in win_data list) username and wins to check for duplicates (refer to elif statement below)
    previous_p = win_data[-1][0].lower()
    previous_w = win_data[-1][2]
   
    #checking for proximate duplicates by looking at username and number of wins
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
                if win_data[index][0].lower() in username_l:
                    win_data[index][1] = player_dict[username_l][0]
                    break
        #if no duplicate exists, add the player to the win_data list
        else:
            win_data.append([username,platform,wins,mp])





#Looking for optimal ratio to include in above for loop when searching for duplicates
def fuzzy_score(token_1, token_2):
    t1_l = token_1.lower()
    t2_l = token_2.lower()
    r = fuzz.ratio(token_1, token_2)
    r_l = fuzz.ratio(t1_l, t2_l)
    pr = fuzz.partial_ratio(token_1, token_2)
    pr_l = fuzz.partial_ratio(t1_l, t2_l)
    tsr = fuzz.token_sort_ratio(token_1, token_2)
    tsr_l = fuzz.token_sort_ratio(t1_l, t2_l)
    print(f'Token 1: {token_1}')
    print(f'Token 2: {token_2}')
    print('                  U  | L')
    print(f'Ratio:            {r} , {r_l}')
    print(f'Partial ratio:    {pr} , {pr_l}')
    print(f'Token sort Ratio: {tsr} , {tsr_l}')
    print()

fuzzy_score('TeePee', 'TeePee__')

fuzzy_score("zZReaper_Zz", "Reaper Gameplays")

fuzzy_score("The GaGod", "GaGod")

fuzzy_score("ShuKz", "TBG_ShuKz")

fuzzy_score("sWKiller9086", "sW Kout")

fuzzy_score("Antoinejuif", "antoine_le_JUIF")

fuzzy_score("CCaNaDa", "CaNaDeeZy")

fuzzy_score("MerK_JJD", "merkjjd")

fuzzy_score("Mmafighter210", " Mma fighter 210")

#trying two different players with similar wins and same console
fuzzy_score('PiggyTony', 'Mixcn')

fuzzy_score('basher', 'baysoldier')
'''
We can remove a duplicate by assessing 3/4 criteria:
    - they have above 30 ratio score
    - they have similar number of wins (+/-5)
    - they have different platforms
    - main differentiator: number of matches played (within range of 25)

Possible solution:
    We create a temporary dictionary that is filtered from the main player_dict
    using the criteria mentioned above.
    
    The temp dict should have a length of 1 only if there is a player that meets those conditions.
    Then we can remove duplicate,
    If no duplicate found, skip

'''








