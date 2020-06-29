# -*- coding: utf-8 -*-
"""
Created on Mon Jun 22 15:43:55 2020

@author: ali_e

Saving all functions for scraping in this py file
"""

# 1. Extracting win data per player and saving it into a nested list
def get_wins(data, win_data = [['username','platform','wins','matches played']]):
    '''
    Get win data for each player from a scraped page from cod.tracker.gg.
    
    Parameters
    ----------
    data : BeautifulSoup ResultSet
        Contains the player info that was scraped from the wins leaderboard.
    win_data : List
        Extracted elements are appended to this win_data list.
        For each player in data, the following is extracted:
            1. Username
            2. Wins
            3. Matches Played
            4. Platform (e.g. playstation)

    Returns
    -------
    win_data
    '''
    #platform classes associated with svg tag
    #need this list to ensure the platform tag is selected in the following for loop
    platform_classes = ['platform-icon platform-icon platform-atvi', 'platform-icon platform-icon platform-battlenet',
                    'platform-icon platform-icon platform-xbl', 'platform-icon platform-icon platform-psn']
    
    #for each player on the page...
    for player in range(len(data)):
        
        #...get username, wins, matches played (mp) and platform
        username = data[player].find('span', attrs = {'class':'trn-ign__username'}).text
        wins = int((data[player].find('td', attrs = {'class':'stat'}).text).replace(',',''))
        mp = int((data[player].find('td', attrs = {'class':'stat collapse'}).text).replace(',',''))
        #there are many svg tags (e.g. rank, twitch icon) so needed to specify class; then select class 
        #and remove irrelevant info, leaving only the platform name
        platform = (data[player].find('svg', attrs= {'class':platform_classes})['class'][-1]).replace('platform-','')
        #for username, need to check if the player is on activision or not...
        if platform != 'atvi':
            username = data[player].find('span', attrs = {'class':'trn-ign__username'}).text
        #...if not, we need to remove the special number identifier at the end and retain just the original username
        else:
            username = data[player].find('span', attrs = {'class':'trn-ign__username'}).text
            username = username.split('#')[0]
        
        
        #need to get previous player username and wins to check for duplicates (refer to elif statement below)
        previous_p = (win_data[-1][0]).lower()
        previous_w = win_data[-1][2]
        
       
        #checking for duplicates by looking at username and number of wins (number of wins may be off by up to 5 as database updates)
        if ((username.lower() in previous_p) or (previous_p in username.lower())) and (wins - previous_w in range(-5,6)):
            #if platform is not activision, then one of the main 3 platforms is already identified
            if win_data[-1][1] != 'atvi':
                continue
            #if not, get the relevant platform used by the player
            else:
                win_data[-1][1] = platform
       
        #if no duplicate exists, simply append their info to the win_data list
        else:
            win_data.append([username,platform,wins,mp])
            
    return win_data