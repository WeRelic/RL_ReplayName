"""
    Name:
        RL_Replay_ReplacerUI.py
    Author:
        Relic
    Date:
        12/27/2017

    -----------------------------------------------------------------------------
    
    Purpose:    
        Provides a UI front end for RL_Replay_Replacer.py

    Developer Notes:
        Look into 'Notebook' widget for tabbed pages. Found in ttk.
"""
import tkinter, ttk




class ReplayFile( object ):
    def __init__( self, path_to_replay, output_path = None ):
        self.replay_name = replay_name
        self.paths       = ( path_to_replay, output_path )
        self.json_data   = {}

    def Decode(self):
        """
            Decode the .REPLAY file into a JSON dict.
        """
        

    def Encode(self):
        """
            Encode the JSON dict stored in this class to a .REPLAY file.
        """
        



class Player( object ):
    player_id_counter = 0
    def __init__( self, original_name, new_name = None ):
        self.names = ( original_name, new_name )
        self.player_id = self.__class__.player_id_counter
        self.__class__.player_id_counter += 1



class CarBody( object ):
    def __init__( self, name, paint_color = None ):
        self.name = name
        self.paint_color = paint_color

    def IsPainted( self ):
        return self.paint_color != None
    







                  
class PlayerStats( object ):
    pass

class PlayerCamera( object ):
    """
        Displays and allows modification of a specific player's camera settings.
    """
    fov_range = ( 0, 110 )
    
    pass
