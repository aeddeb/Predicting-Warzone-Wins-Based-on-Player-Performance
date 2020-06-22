# -*- coding: utf-8 -*-
"""
Created on Mon Jun 22 15:43:55 2020

@author: ali_e
"""


def get_wins(data, win_data):
    '''
    Parameters
    ----------
    data : BeautifulSoup ResultSet
        Contains the player info that was scraped from the web.
    win_data : List
        Extracted elements are appended to this win_data list.

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
        
        
        #need to get previous player username and wins to check for duplicates (refer to elif statement below) except for the first player
        if player != 0:
            previous_p = data[player - 1].find('span', attrs = {'class':'trn-ign__username'}).text.lower()
            previous_w = int((data[player - 1].find('td', attrs = {'class':'stat'}).text).replace(',',''))
        
        #if first player, put their info into the list as no duplicates are possible at this point
        if player == 0:
            win_data.append([username,platform,wins,mp])
       
        #checking for duplicates by looking at username and number of wins
        elif ((username.lower() in previous_p) or (previous_p in username.lower())) and (wins == previous_w):
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