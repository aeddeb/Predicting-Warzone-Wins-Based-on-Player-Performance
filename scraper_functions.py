# -*- coding: utf-8 -*-
"""
Created on Mon Jun 22 15:43:55 2020

@author: ali_e

Saving all functions for scraping in this py file
"""

# 1. Extracting win data per player and saving it into a nested list
def get_wins(data, platform, win_data = [['username','platform','wins','matches played']]):
    '''
    Get win data for each player from a scraped page from cod.tracker.gg.
    
    Parameters
    ----------
    data : BeautifulSoup ResultSet
        Contains the player info that was scraped from the wins leaderboard.
    platform: string
        Contains the name of the platform the players play on.
    win_data : Nested List
        Extracted elements are appended to this win_data list.
        For each player in data, the following is extracted:
            1. Username
            2. Platform (e.g. playstation)
            3. Wins
            4. Matches Played

    Returns
    -------
    win_data
    '''
    
    #for each player on the page...
    for player in range(len(data)):
        
        #...get username, wins, matches played (mp) and platform
        username = data[player].find('span', attrs = {'class':'trn-ign__username'}).text
        wins = int((data[player].find('td', attrs = {'class':'stat'}).text).replace(',',''))
        mp = int((data[player].find('td', attrs = {'class':'stat collapse'}).text).replace(',',''))

        #for username, need to check if the player is on battlenet or not...
        if platform != 'battlenet':
            username = data[player].find('span', attrs = {'class':'trn-ign__username'}).text
        #...if not, we need to add the special player id onto the username to avoid duplicate names
        else:
            username = data[player].find('span', attrs = {'class':'trn-ign__username'}).text 
            player_id = data[player].find('span', attrs = {'class':'trn-ign__discriminator'}).text
            username = username + player_id
        
    #add the players info to the win_data list
    win_data.append([username,platform,wins,mp])
            
    return win_data