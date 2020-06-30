# -*- coding: utf-8 -*-
"""
Created on Mon Jun 22 15:43:55 2020

@author: ali_e

Saving all functions for scraping in this py file
"""

#lIBRARIES
#------------------------------------------------------------------------------
import requests
from bs4 import BeautifulSoup
from tqdm import tqdm
#------------------------------------------------------------------------------


#FUNCTIONS
#------------------------------------------------------------------------------
# 1. Extracting win data per player and saving it into a nested list
def get_stat(data, platform, feature, scraped_data):
    '''
    Get win data for each player from a scraped page from cod.tracker.gg.
    
    Parameters
    ----------
    data : BeautifulSoup ResultSet
        Contains the player info that was scraped from the wins leaderboard.
    platform: string
        Contains the name of the platform the players play on.
    feature: string
        Name of feature being scraped e.g. Wins.
    win_data : Dictionary
        Extracted elements are placed into this dictionary with the key being 
        the player's username.
        The associated value is a list containing the player's:
            1. Platform (e.g. playstation)
            2. Stat (e.g. Wins)
            3. Matches Played (Only scraped if feature is Wins)

    Returns
    -------
    scraped_data
    
    '''
    
    assert isinstance(scraped_data, dict), 'scraped_data must be a dictionary'
    
    #for each player on the page...
    for player in range(len(data)):
        
        #for username, need to check if the player is on battlenet or not...
        if platform != 'battlenet':
            username = data[player].find('span', attrs = {'class':'trn-ign__username'}).text
        #...if not, we need to add the special player id onto the username to avoid duplicate names
        else:
            name = data[player].find('span', attrs = {'class':'trn-ign__username'}).text 
            try:
                player_id = data[player].find('span', attrs = {'class':'trn-ign__discriminator'}).text
                username = name + player_id
            except:
                username = name

        if feature == 'Wins':
            #...get username, wins, matches played (mp) and platform
            wins = int((data[player].find('td', attrs = {'class':'stat'}).text).replace(',',''))
            mp = int((data[player].find('td', attrs = {'class':'stat collapse'}).text).replace(',',''))
            #add the players info to the win_data list
            #win_data.append([username,platform,wins,mp])
            scraped_data[username] = [platform, wins, mp]
        else:
            #...get other statistic
            stat = data[player].find('td', attrs = {'class':'stat'}).text
            scraped_data[username] = [platform, stat]
            
    return scraped_data



def scrape_pages(platform, feature,  end, scraped_data, start=1):
    '''
    Cycle through pages of cod.tracker.gg and extract info.
    
    Parameters
    ----------
    platform: string
        Contains the name of the platform the players play on.
    feature: string
        Name of feature being scraped e.g. Wins.
    
    Returns
    -------
    
    '''
    url = f"https://cod.tracker.gg/warzone/leaderboards/battle-royale/{platform}/{feature}?page="
    
    for num in tqdm(range(start,end)):

        try:
            #getting page number
            page_num = str(num)
    
            page = requests.get(url + page_num)
    
            soup = BeautifulSoup(page.content, 'html.parser')
    
            # ----------------------------------------------------------------------------
            # Need to select row and extract console, player name, wins and Matches Played
    
            #each row of player data has a tr tag
            data = soup.find_all('tr')
            #removing first row which is just the table heading
            del data[0]
            
            scraped_data = get_stat(data, platform, feature, scraped_data)
                
        except:
            print(f'Encountered error at batch {num}')
            return scraped_data 
        
    return scraped_data