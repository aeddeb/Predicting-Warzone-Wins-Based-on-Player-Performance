# -*- coding: utf-8 -*-
"""
Created on Sat Jun 20 03:48:07 2020

@author: ali_e

To use this scraper, run from the command line and specify the website, feature
and platform (only needed for cdtr website).

Example:
   $ python cod_scraper.py cdtr Wins psn
"""

#loading libraries
import scraper_functions as sf
import pickle
import sys

#-----------------------------------------------------------------------------
  
#Specify website, feature, and platform (only needed if website is cdtr) max page

#website
website = sys.argv[1]

#Refer to notes.txt for feature options
#example: 'Wins'
feature = sys.argv[2]

#options for 'cdtr': 'psn', 'xbl', 'battlenet'
if website == 'cdtr':
    platform = sys.argv[3]
else:
    platform = 'all'

#getting data (starting with empty dictionary)
data = sf.scrape_pages(website, feature, {}, platform=platform)

#save data file into data directory
with open(f"data/{platform}_{feature}.pkl", "wb") as file:
    pickle.dump(data, file)
















