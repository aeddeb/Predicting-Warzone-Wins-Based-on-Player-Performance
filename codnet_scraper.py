# -*- coding: utf-8 -*-
"""
Created on Sat Jun 20 03:48:07 2020

@author: ali_e

Goals:
    
1. Extract name, player console and value for metric for 1 page.

2. Figure out where to store the above data.

3. Figure out how to go to the next page.

4. Repeat steps 1-3.

_______________________________________________________________________________

After, need to get other metrics (figure out which ones are needed).

Then, need a way to match the metric to the player and only have 1 instance of their name.
"""

import requests
from bs4 import BeautifulSoup

url = 'https://cod.tracker.gg/warzone/leaderboards/battle-royale/all/WlRatio?page='

#can later use a loop to go through the pages
page_num = str(1)

page = requests.get(url + page_num)

soup = BeautifulSoup(page.content, 'html.parser')

# need to select row and extract console, player name, win % and Matches Played