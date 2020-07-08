# -*- coding: utf-8 -*-
"""
Created on Sat Jun 20 03:48:07 2020

@author: ali_e

To use this scraper, run from the command line and specify the desired platform
and feature.

Example:
   $ python cod_scraper.py psn Wins
"""

#loading libraries
import scraper_functions as sf
import pickle
import sys
#-----------------------------------------------------------------------------
  
#specify platform and feature

#options: 'psn', 'xbl', 'battlenet'
platform = sys.argv[1]

#Refer to notes.txt for feature options
#example: 'Wins'
feature = sys.argv[2]

#getting data
data = sf.scrape_pages(platform, feature,  {}, max_page = 8)

#save data file into data directory
with open("data/"+ platform + "_" + feature + ".pkl", "wb") as file:
    pickle.dump(data, file)
















