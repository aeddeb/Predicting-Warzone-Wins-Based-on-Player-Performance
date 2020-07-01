# -*- coding: utf-8 -*-
"""
Created on Sat Jun 20 03:48:07 2020

@author: ali_e

"""

#loading libraries
import scraper_functions as sf
import pickle
#-----------------------------------------------------------------------------
  
'''
Options:
platform : 'psn', 'xbl', 'battlenet'
feature : Refer to notes.txt
'''
#grabbing data
test_data = sf.scrape_pages('psn', 'Wins', 7, {})

a_file = open("data/test_data.pkl", "wb")
pickle.dump(test_data, a_file)
a_file.close()

















