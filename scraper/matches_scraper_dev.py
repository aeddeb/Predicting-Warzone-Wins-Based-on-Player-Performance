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
from bs4 import BeautifulSoup
from datetime import date

#------------------------------------------------------------------------------

#setting up selenium options and drivers
options = Options()
#run headless (ie. without GUI)
options.headless = True
DRIVER_PATH = 'chromedriver.exe'
driver = webdriver.Chrome(options=options, executable_path=DRIVER_PATH)

#assign url
player = "humpy1"
platform = "psn"
url = "https://cod.tracker.gg/warzone/profile/{psn}}/{player}/overview"

#get page source html
driver.get(url)
page = driver.page_source

#create soup object
soup = BeautifulSoup(page, 'html.parser')

#------------------------------------------------------------------------------

#Compare date and only get match data for matches in a specific month (e.g. July)

#finding all the matches under each date
match_dates = soup.find_all('div', attrs = {'class' : 'trn-gamereport-list__group'})

#getting today's date
today = date.today()


for match_date in match_dates:

    date = match_date.find('h3', attrs = {'class' : 'trn-gamereport-list__title'}).text
    #deal with case of 'Matches Today' - convert to date
    if date == "Matches Today ":
        date = today
    else:
        #need to see if date is within specified month
        #if yes, go through the matches and get the players data
        pass
        #if no, skip this date and go onto the next

#Note: need to ensure that once the specified month is passed, the loop stops
