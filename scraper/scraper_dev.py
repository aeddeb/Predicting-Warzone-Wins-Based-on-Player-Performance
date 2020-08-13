# -*- coding: utf-8 -*-
"""
Created on Mon Aug 10 17:12:20 2020

@author: ali_e
"""

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup

options = Options()
#run headless (ie. without GUI)
options.headless = True
DRIVER_PATH = 'chromedriver.exe'
driver = webdriver.Chrome(options=options, executable_path=DRIVER_PATH)


driver.get("https://cod.tracker.gg/warzone/profile/xbl/BrownMagicGT/overview")

page = driver.page_source

soup = BeautifulSoup(page, 'html.parser')

driver.quit()


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
SAMPLE OUTPUT:

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


    
    