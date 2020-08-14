# -*- coding: utf-8 -*-
"""
Created on Mon Aug 10 17:12:20 2020

@author: ali_e
"""

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import time

options = Options()
#run headless (ie. without GUI)
options.headless = True
DRIVER_PATH = 'chromedriver.exe'
driver = webdriver.Chrome(options=options, executable_path=DRIVER_PATH)

url = "https://cod.tracker.gg/warzone/profile/psn/gamergirlsence/overview"
print("fetching webpage")
#get html for player
driver.get(url)
print('webpage fetched')

page = driver.page_source

soup = BeautifulSoup(page, 'html.parser')

#driver.quit()


#------------------------------------------------------------------------------
#Finding Elements

# 1. Overview

# 1.1. Overview  - overall BR stats

#getting the overview
for parent in soup.find('h2', text = 'Battle Royale').parents:
    if parent.name == 'div' and parent.has_attr("class"):
        if parent['class'] == ['segment-stats', 'card', 'bordered', 'responsive']:
            overview = parent
            break
        
#now parse out all the info that is needed

#creating a dictionary to save all the data points
player_data = {}

#get time and matches played
time_played = overview.find('span', attrs =  {'class' : "playtime"}).text.replace('\n','').replace(' Play Time', '').strip()
matches_played = int(overview.find('span', attrs =  {'class' : "matches"}).text.replace('\n','').replace(' Matches', '').replace(',','').strip())
#add to player_data dict
player_data['time_played'] = time_played
player_data['matches_played'] = matches_played

#the remaining data points are containepla within divs with class = numbers
stats = overview.find_all('div', attrs =  {'class' : "numbers"})

#for every stat, add to dict; key = stat name and value = value of stat
for stat in stats:
    #get stat name
    name = stat.find('span', attrs =  {'class' : "name"}).text
    #get stat value
    value = stat.find('span', attrs =  {'class' : "value"}).text
    #add player stat to player_data
    player_data[name] = value
    
'''
SAMPLE OUTPUT (player_data):

Wins : 1
Top 5 : 7
Top 10 : 19
Top 25 : 45
Kills : 201
Deaths : 325
K/D Ratio : 0.62
Downs : 178
Avg. Life : 05m 47s
Score : 193,180
Score/min : 102.70
Score/game : 1,370.07
Contracts : 105
Win % : 0.7%

'''



# 2. Weekly Stats

'''
Tasks for modes page:
    
1. Get stats

2. Identify which game modes player has played in past week
    - if player has not played a certain game mode, matches played = 0 and 
    corresponding stats will be null
    
3. Check for "This player has not played Warzone in the past week."

'''

#navigate to 'modes' page for player
link = driver.find_element_by_link_text('Modes')
link.click()
time.sleep(2)
#get page source (ie. raw html)
modes_page = driver.page_source

#create soup onject for modes page
soup_modes = BeautifulSoup(modes_page, 'html.parser')

#get the game modes 
game_modes = soup_modes.find_all('div', attrs = {'class' : 'segment-stats card bordered responsive'})
#list of game types (of interest)
game_types = ['BR Quads', 'BR Trios', 'BR Duos', 'BR Solos']

#saving weekly data in another dict
weekly_player_stats = {}

#get weekly stats
for game_mode in game_modes:
    
     game_type = game_mode.find('div', attrs = {'class' : 'title'}).find('h2').text
     if game_type in game_types:
         
         #get matches played
         mp = game_mode.find('span', attrs = {'class' : 'matches'}).text.replace('Matches','').strip()
         weekly_player_stats[game_type] = {'Matches Played' : mp}
         
         #get all the other weekly stats for the game type
         for stat in game_mode.find_all('div', attrs ={'class' : 'numbers'}):
             name = stat.find('span', attrs = {'class' : 'name'}).text
             value = stat.find('span', attrs = {'class' : 'value'}).text
             weekly_player_stats[game_type][name] = value
     else:
         continue

#if a player did not play a game mode, assign matches played for that mode to 0
for game_type in game_types:
    if game_type not in weekly_player_stats:
        weekly_player_stats[game_type] = {'Matches Played' : 0}




driver.quit()
