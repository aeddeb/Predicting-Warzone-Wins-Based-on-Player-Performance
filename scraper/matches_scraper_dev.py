# -*- coding: utf-8 -*-
"""
Created on Fri Aug 21 18:45:23 2020

@author: ali_e
"""

#------------------------------------------------------------------------------
#Import Libraries

import requests
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import datetime as dt

#------------------------------------------------------------------------------

#setting up selenium options and drivers
options = Options()
#run headless (ie. without GUI)
options.headless = True
DRIVER_PATH = 'chromedriver.exe'
driver = webdriver.Chrome(options=options, executable_path=DRIVER_PATH)

#specify player and platform they play on
player = "humpy1"
platform = "psn"
player_id = platform + '-' + player
#assign url for matches page for specified player
url = f"https://cod.tracker.gg/warzone/profile/{platform}/{player}/matches"

#get page source html
driver.get(url)
#need to wait until page is loaded
WebDriverWait(driver,10).until(EC.presence_of_element_located((By.CLASS_NAME,'trn-gamereport-list__group')))
#save html to variable
page = driver.page_source

#create soup object
soup = BeautifulSoup(page, 'html.parser')

#------------------------------------------------------------------------------

#Compare date and only get match data for matches in a specific month (e.g. July)
#Note!!! for dev purposes, I will aim to just get matches from today's date 

#finding all the matches under each date
match_dates = soup.find_all('div', attrs = {'class' : 'trn-gamereport-list__group'})
print('match dates: ', len(match_dates))
#getting today's date
today = dt.date.today()

year = '2020'

#creating dict to save data
player_match_data = {}
#assigning match counter
match_counter = 0

#specifying relevant match types
match_types = ['BR Solos', 'BR Duos', 'BR Trios', 'BR Quads']

for match_date in match_dates:

    date = match_date.find('h3', attrs = {'class' : 'trn-gamereport-list__title'}).text
    print('date: ',date)
    #deal with case of 'Matches Today' - convert to date
    if date == "Matches Today ":
       
        #get all the matches
        matches = match_date.find_all('div', attrs = {
            'class' : ['card bordered responsive match match--lost',
            'card bordered responsive match match--won']}
            )

        #for all the matches in a specific day...
        for match in matches:
            
            #determine match type
            match_type = match.find('span', attrs = {'class' : 'match__name'}).text
            print('type: ', match_type)
            #determine if match type is one of the 4 relevant match types
            if match_type in match_types:

                #...get the match url,
                match_url = match.find('a', attrs = {'class' : 'match__link'})['href']
                print('url: ', match_url)
                
                #and time
                match_time = match.find('span', attrs = {'class' : 'match__time'})
                print('time: ', match_time)

                #add player data
                player_match_data[date] = {match_counter : {
                    'mode' : match_type,
                    'time' : match_time,
                    'url' : match_url
                }}
                #increment match counter
                match_counter += 1

            #if not, skip the match and move to the next one
            else:
                continue

    #otherwise, break from loop
    else:
        break


print(player_match_data)
'''
for match_date in match_dates:

    date = match_date.find('h3', attrs = {'class' : 'trn-gamereport-list__title'}).text
    #deal with case of 'Matches Today' - convert to date
    if date == "Matches Today ":
        date = today
    #otherwise, just add the year to the date
    else:
        date = date + year


    #need to see if date is within specified month (e.g. July)
    if date == 7:
        #if yes, go through the matches and get the players data
        pass
        driver.execute_script("window.open('http://google.com', 'new_window')")

    #if no and the match date is in a later month, skip this date and go onto the next    
    elif date.month > 7:
        #if no, skip this date and go onto the next
        continue

    #else the match date is now before the specified month so break the loop
    else:
        break
'''