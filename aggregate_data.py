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

#------------------------------------------------------------------------------

#function for adding player info to dictionary of choice
def add_player_info(data_dict, file_platform, feature, player, stat, player_platform):
    '''
    Adds a player's info into selected dictionary (ie. data_dict).    

    Parameters
    ----------
    data_dict : dictionary to which player info is added

    file_platform : string from these options: 'all', 'psn', 'xbl' or 'battlenet'.
        Used to specify which website the data is coming from.
        'all' indicates data is coming from the cdst website.
        The other 3 options indicate data is coming from the cdtr website.
    
    feature :  string
        Used to specify the feature associated with the player data.
    
    player : string
        The player's username.
    
    stat : dictionary of the player's stats (to be extracted).

    player_platform : string indicating the player's platform
        Options are 'psn', 'xbl' or 'battlenet'. 

    Output
    ------
    data_dict : dictionary with player's info added
    
    '''
    #if player already in the data_dict, add their stats
    if player in data_dict:
        #if from cdst (ie. platform is 'all'), only 1 stat to be added
        if file_platform == 'all':
            data_dict[player][feature] = stat[feature]
        #if from cdtr, 2 stats (feature and mp) need to be added
        else:
            #add feature and mps to player
            data_dict[player][feature] = stat[feature]
            data_dict[player][feature + '_mp'] = stat[feature + '_mp']
    
    #else player is not in the data_dict and need to be added as a new player
    else:
        #if from cdst (ie. platform is 'all'), only 1 stat to be added
        if file_platform == 'all':
            data_dict[player] = {'platform': player_platform, 
                               feature: stat[feature]
                               }
        #if from cdtr, 2 stats (feature and mp)
        else:
            #add feature and mps to player
            data_dict[player] = {'platform': player_platform, 
                               feature: stat[feature],
                               feature + '_mp' : stat[feature + '_mp']
                               }
            
    return data_dict
    
    
#------------------------------------------------------------------------------


# Step 1: getting names of all the data files
os.chdir('./data/')

#creating list with data file names
file_list = [file for file in glob.glob("*.pkl")]



# Step 2: Read in file at a time, add data to master data file per platform

#initiate main data dictionaries for each platform (ie. psn, xbl, battlenet)
psn_dict = {}
xbl_dict = {}
battlenet_dict = {}

#for each file...
for file_name in tqdm(file_list):
    
    #extracting platform and feature from the file name (needed later)
    file_platform = file_name.replace('.pkl','').split('_')[0]
    feature = file_name.replace('.pkl','').split('_')[1]
    
    #grab data from file 
    with open(file_name, 'rb') as file:
        data = pickle.load(file)
    
    #need to add player info to appropriate dict based on their platform 
    
    #for each player in the currently loaded data file...
    for player, stat in tqdm(data.items()):
        
        #get the player's platform
        player_platform = stat['platform']
        
        #if player plays on playstation, add their info to psn_dict
        if player_platform == 'psn':
            psn_dict = add_player_info(psn_dict, file_platform, feature, player,
                                       stat, player_platform)
        elif player_platform == 'xbl':
            xbl_dict = add_player_info(xbl_dict, file_platform, feature, player,
                           stat, player_platform)
            
        elif player_platform == 'battlenet':
            battlenet_dict = add_player_info(battlenet_dict, file_platform, feature, player,
               stat, player_platform)
            
        else:
            print(f"For player {player} in file {file_name}, {f{player_platform} is an invalid platform.")
            
            
            
            

    
    
    
    
    
    
    
    
