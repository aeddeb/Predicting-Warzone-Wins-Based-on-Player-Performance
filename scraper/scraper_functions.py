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
    '''
    #create beautifulsoup object
    soup = BeautifulSoup(scraped_page, 'html.parser')

    #grab all players
    players = soup.find_all('td', attrs = {'class' : 'username'})


    #instantiate dictionary to save player usernames and corresponding url equivalent if platform is battlenet
    if platform == 'battlenet':
        usernames = {}
    #otherwise, save the player usernames in a list
    else:
        usernames = []


    #for each player on the page...
    for player in range(len(players)):
        
        #Checking if the player is on battlenet or not...
        #...if not...
        if platform != 'battlenet':
            username = data[player].find('span', attrs = {'class':'trn-ign__username'}).text
            #...add player to usernames list
            usernames.append(username)

        #...otherwise, we need to add the special player id onto the username to get the full battlenet id
        else:
            name = data[player].find('span', attrs = {'class':'trn-ign__username'}).text 
            try:
                player_id = data[player].find('span', attrs = {'class':'trn-ign__discriminator'}).text
                username = name + player_id
                url_username = name + player_id.replace('#', '%')
                usernames[username] = url_username
            except:
                username = name
                url_username = name.replace('#', '%')

    return usernames