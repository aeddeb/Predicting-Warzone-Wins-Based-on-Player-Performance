# -*- coding: utf-8 -*-
"""
Created on Sat Jul 25 16:32:05 2020

@author: ali_e
"""
#libraries
import os
import glob
import pickle
from tqdm import tqdm



# Step 1: getting names of all the data files
os.chdir('./data/')

#creating list with data file names
file_list = [file for file in glob.glob("*.pkl")]



# Step 2: Read in file at a time, add data to master data file

#initiate main data dictionary
df_dict = {}

#for each file...
for file in tqdm(file_list):
    #extracting platform and feature from the file name (needed later)
    platform = file.replace('.pkl','').split('_')[0]
    feature = file.replace('.pkl','').split('_')[1]
    
    #grab data from file 
    with open(file, 'rb') as file:
        data = pickle.load(file)
    
    #if main data dict is empty, then simply add all the data from currently 
    #loaded data
    if bool(df_dict) == False:
        df_dict = data.copy()
    #if not, match players by their name and platform
    else:
        #for each player in the currently loaded data file...
        for player, stat in data.items():
            #...if player is in df_dict and platforms are the same
            if player in df_dict and df_dict[player]['platform'] == data[player]['platform']:
                
                #if from cdst (ie. platform is 'all''), only 1 stat to be added
                if platform == 'all':
                    df_dict[player][feature] = stat[feature]
                #if from cdtr, 2 stats (feature and mp)
                else:
                    #add feature and mps to player
                    df_dict[player][feature] = stat[feature]
                    df_dict[player][feature + '_mp'] = stat[feature + '_mp']
            
            
            #...but if not in df_dict, add them in as a new player 
            #note: that this will lead in missing values which later need to be imputed
            else:
                #if from cdst (ie. platform is 'all''), only 1 stat to be added
                if platform == 'all':
                    df_dict[player] = {'platform': stat['platform'], 
                                       feature: stat[feature]
                                       }
                #if from cdtr, 2 stats (feature and mp)
                else:
                    #add feature and mps to player
                    df_dict[player] = {'platform': stat['platform'], 
                                       feature: stat[feature],
                                       feature + '_mp' : stat[feature + '_mp']
                                       }
    
    
    
    
    
    
    
    
    
