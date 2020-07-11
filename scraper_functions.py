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
#------------------------------------------------------------------------------


#FUNCTIONS
#------------------------------------------------------------------------------
# 1. Extracting player stats from cod.tracker.gg and saving it into a dictionary
def get_stat_cdtr(data, platform, feature, scraped_data):
    '''
    Get stat for each player from a scraped page from cod.tracker.gg.
    
    Parameters
    ----------
    data : BeautifulSoup ResultSet
        Contains the player info that was scraped from the leaderboard.
    platform: string
        Contains the name of the platform the players play on.
    feature: string
        Name of feature being scraped e.g. Wins.
    win_data : Dictionary
        Extracted elements are placed into this dictionary with the key being 
        the player's username.
        The associated value is a dictionary containing the player's:
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

        #...get username, stat, matches played (mp) and platform
        stat = data[player].find('td', attrs = {'class':'stat'}).text
        mp = int((data[player].find('td', attrs = {'class':'stat collapse'}).text).replace(',',''))
        scraped_data[username] = {'platform' : platform, feature : stat, 'mp': mp}
            
    return scraped_data




# 2. Extracting player stats from codstats.net and saving it into a dictionary
def get_stat_cdst(data, feature, scraped_data):
    '''
    Get stat for each player from a scraped page from cod.tracker.gg.
    
    Parameters
    ----------
    data : BeautifulSoup ResultSet
        Contains the player info that was scraped from the leaderboard.
    feature: string
        Name of feature being scraped e.g. Wins.
    win_data : Dictionary
        Extracted elements are placed into this dictionary with the key being 
        the player's username.
        The associated value is a dictionary containing the player's:
            1. Platform (e.g. playstation)
            2. Stat (e.g. Wins)

    Returns
    -------
    scraped_data
    
    '''
    
    assert isinstance(scraped_data, dict), 'scraped_data must be a dictionary'
    
    #platform converter; using this to convert names of platforms to coincide with other website
    platform_dict = {'pc' : 'battlenet', 'xbox' : 'xbl', 'ps4' : 'psn'}

    #for each player on the page...
    for player in range(len(data)):
        
        #get platform; if activison, skip player
        platform = data[player]['href'].split('/')[3]
        if platform == 'act':
            continue
        
        #if not, get player username and stats
        username = data[player].find('div', attrs = {'style' : 'width:500px;font-size:16px;letter-spacing:.1em'}).text.replace('\r\n\t\r\n\t', '')
        stat = data[player].find('div', attrs = {'style' : 'color:#52bafe;display: flex;overflow:auto;display:inline-block;flex-grow: 1; flex-wrap: wrap; min-width:50px;max-width:100px;text-align:center;'}).text.replace('\r\n\t', '')
        #getting correct version of platform
        platform = platform_dict[platform]

        scraped_data[username] = {'platform' : platform, feature : stat}
            
    return scraped_data




#3. URL selector
def select_url(website, feature, platform):
    '''
    Selects url to be scraped.

    Parameters
    ----------
    website : str
        String containing the name of the desired website. 
        Options:
            Type 'cdtr' for cod.tracker.gg.
            Type 'cdst' for codstats.net.
    feature : str
        String containing the name of the desired feature. E.g. Wins
        For cdtr, options are:
            'Wins', 'Kills', 'Deaths', 'Downs', 'TimePlayed', 'Score', 'ScorePerMinute', 'Contracts', or 'Top10'.
        For cdst, options are:
            'KillsPerMin', 'DamageDone', 'DamageTaken', 'HeadshotsPercentage', 'TimeMoving', 'LastStandKills',
            'CachesOpened', 'KioskPurchases', 'TabletsPickedUp', 'TeamSurvival', or 'Revived'.  
    platform : str (Optional)
        String of the desired platform. Only needed if website is cdtr. Otherwise, not used.
        Options for 'cdtr':
            'psn', 'xbl', or 'battlenet'. 

    Returns
    -------
    url : string
        String of desired url to be scraped.
    '''
    if website == 'cdtr':
        assert feature in ['Wins', 'Kills', 'Deaths', 'Downs', 'TimePlayed', 'Score', 'ScorePerMinute', 'Contracts', 'Top10'], 'You have not selected a feature from the feature set'
        url = f"https://cod.tracker.gg/warzone/leaderboards/battle-royale/{platform}/{feature}?page="

    elif website == 'cdst':

        url_dict = {'KillsPerMin' : 'kpm/16',
                    'DamageDone' : 'damageDone/161',
                    'DamageTaken' : 'damageTaken/161',
                    'HeadshotsPercentage' : 'headshotPercentage/161',
                    'TimeMoving' : 'percentTimeMoving/161',
                    'LastStandKills' : 'objectiveLastStandKill/161',
                    'CachesOpened' : 'objectiveBrCacheOpen/161',
                    'KioskPurchases' : 'objectiveBrKioskBuy/161',
                    'TabletsPickedUp' : 'objectiveBrMissionPickupTablet/161',
                    'TeamSurvival' : 'teamSurvivalTime/161',
                    'Revived' : 'objectiveReviver/161'}
        
        assert feature in url_dict.keys(), 'You have not selected a feature from the feature set' 
        
        url = f"https://codstats.net/warzone/leaderboards/{url_dict[feature]}&page="

    else:
        print('You have not selected a valid website. Options are "cdst" and "cdtr".')

    return url



#4. Cycle through pages and extract player stats
def scrape_pages(website, feature, scraped_data, platform, start = 1, max_page = 10000):
    '''
    Cycle through pages of cod.tracker.gg and extract info.
    
    Parameters
    ----------
    platform : string
        Contains the name of the platform the players play on.
    feature : string
        Name of feature being scraped e.g. Wins.
    max_page : int
        The max number of pages to scrape. This is a safety measure against infinite scraping.
    scraped_data : dict
        Can be empty list or list with previous player data in which this function appends data to.
    start : int
        Starting page number for scraping.
    
    Returns
    -------
    scraped_data : dict
        Dictionary containing player info. Key if player name and value contains player's platoform and stat.
    '''
    #get url
    url = select_url(website, feature, platform)
    
    #starting page number (by default, starts at page 1)
    num = start
    
    #skip errors with retry
    retry = 1

    #while the current page number is less than the max page number specified by the user...
    while num < max_page:
       
        #...scrape the page and add the player's info to the scraped_data dictionary
        try:
            #getting page number
            page_num = str(num)
            
            #adding a user agent to avoid 403 errors
            if num % 2 == 0:
                user = 'Mozilla/5.0'
            else:
                user = 'Chrome/63.0.3239.132'

            #requestng page info
            page = requests.get(url + page_num, headers={'User-Agent':user})
            
            #if we reach the end of the database in cod.tracker.gg, break from loop
            if website == 'cdtr':
                if "no players to rank" in page.text.lower():
                    break
            
            #parsing page with BeautifulSoup
            soup = BeautifulSoup(page.content, 'html.parser')

            #if we reach the end of the database in codstats.net, break from loop
            if website == 'cdst':
                num_players = soup.find('a', attrs = {'class' : 'white'})
                if num_players == None:
                    break

            # ----------------------------------------------------------------------------
            # Need to select row and extract player name and stats
            #check if website is cod.tracker.gg and get data
            if website == 'cdtr':
                #each row of player data has a tr tag
                data = soup.find_all('tr')
                #removing first row which is just the table heading
                del data[0]
                #get all players info
                scraped_data = get_stat_cdtr(data, platform, feature, scraped_data)
            
            #else, get data from codstats.net
            else:
                data = soup.find_all('a', attrs = {'class' : 'white'})
                #get all players info
                scraped_data = get_stat_cdst(data, feature, scraped_data)
            

            #give status update to user every 10 pages
            if num % 10 == 0:
                print(f'Successfully scraped page {num}')
            
            #increase page number and reset retry number
            num += 1
            retry = 1
        
        #protect against errors by saving whatever data has already been collected
        except:
            #we go up to 3 attempts to try and scrape the page
            if retry < 4:
                print(f'Encountered error at page {num}...attempt to re-scrape #{retry}')
                retry += 1
                continue
            else:
                print(f'Encountered error at page {num}...stopped after 3 unsuccessful attempts')
                break 

    print(f'Program ended at page {num} for {feature} on {platform} platform(s)')    
    return scraped_data