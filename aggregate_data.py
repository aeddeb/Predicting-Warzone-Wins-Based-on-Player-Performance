# -*- coding: utf-8 -*-
"""
Created on Sat Jul 25 16:32:05 2020

@author: ali_e
"""

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
    #if player already exists in data_dict, add their stats
    if player in data_dict:
        #if from cdst (ie. platform is 'all'), only 1 stat to be added
        if file_platform == 'all':
            data_dict[player][feature] = stat[feature]
        #if from cdtr, 2 stats (feature and mp) need to be added
        else:
            #add feature and mps to player
            data_dict[player][feature] = stat[feature]
            data_dict[player][feature + '_mp'] = stat[feature + '_mp']
    
    #else player is not in the data_dict and needs to be added as a new player
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