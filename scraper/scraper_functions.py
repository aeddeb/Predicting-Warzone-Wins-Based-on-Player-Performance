# -*- coding: utf-8 -*-
"""
Created on Mon Aug 10 03:56:17 2020

@author: ali_e
"""

#lIBRARIES
#------------------------------------------------------------------------------
from bs4 import BeautifulSoup
#------------------------------------------------------------------------------


def get_players(scraped_page, platform):
    '''
    Return the names of the players from a scraped page.

    PARAMETERS
    ----------
    scraped_page : raw html from selenium page_source.

    platform: string
        Contains the name of the platform the players play on.

    OUTPUT
    ------
    usernames : dictionary of usernames as keys with their url equivalent as values

    Note: url equivalent is only different from username if the platform is battlenet
    -url uses % instead of #
    '''
    #create beautifulsoup object
    soup = BeautifulSoup(scraped_page, 'html.parser')

    #grab all players
    players = soup.find_all('td', attrs = {'class' : 'username'})


    #instantiate dictionary to save player usernames and corresponding url equivalent (only varies if platform is battlenet)
    usernames = {}

    #for each player on the page...
    for player in range(len(players)):
        
        #Checking if the player is on battlenet or not...
        #...if not...
        if platform != 'battlenet':
            #get username
            username = players[player].find('span', attrs = {'class':'trn-ign__username'}).text
            #...add player to usernames dict
            usernames[username] = username

        #...otherwise, we need to add the special player id onto the username to get the full battlenet id
        else:
            #get player name
            name = players[player].find('span', attrs = {'class':'trn-ign__username'}).text 
            #get player id, if exists
            try:
                player_id = players[player].find('span', attrs = {'class':'trn-ign__discriminator'}).text
                username = name + player_id
                #get the url equivalent of the username
                url_username = name + player_id.replace('#', '%')
            #otherwise the player id is already embedded in the username
            except:
                username = name
                #get the url equivalent of the username
                url_username = name.replace('#', '%')
            #put the username and url_username into the usernames dict
            usernames[username] = url_username

    return usernames



def scrape_overview():
    '''
    '''
    