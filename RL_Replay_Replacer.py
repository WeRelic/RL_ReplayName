"""
    Name:
        RL_Replay_Replacer.py
    Author(s):
        Relic, LieAlgebraCow
    Date:
        12/17/2017

    -----------------------------------------------------------------------------
    
    Purpose:    
        Change Rocket League player names using rattletrap.

    Default Behavior:
        After loading the .REPLAY passed as CLI argument;
        This script uses rattletrap to convert that replay to a minified JSON file.
        User is promted for a name for the replay and a name for each player.
        These names are changed in the .REPLAY file so that they appear when viewed in-game.
        
    Usage:
        RL_Replay_Replacer.py <path/to/replay1.replay> <path/to/replay2.replay> ...

    NOTE:
        NameReplacer.py will be deprecated in favor of RL_Replay_Replacer.py
        once a UI and additional functionality has been implemented.
        
"""


import re, os, sys, json, subprocess, ntpath, operator, functools, copy, time

rattlepath = os.path.join( os.getcwd(), "win_rattle.exe" )

# Turn a .replay into a .json using rattletrap
# Takes STR, path to a .replayfile
# Returns STR, path to the decoded .json file for the replay
def ReplayToJSON( replay ):
    """ Convert a replay to JSON using rattletrap. """
    print( "Parsing {} to JSON...".format( replay ) )
    json_name = StripPathToFile(replay).split( "." )[0]
    json_path = os.path.join( "out", "{}.json".format(json_name) )
    os.system( "win_rattle.exe decode {} > {}".format( replay, json_path ) )
    print( "Done..." )
    return json_path

# Turn a .json file back into a .replay file using rattletrap
# Takes STR, path to a .json file, and STR, path to the replay file that we started with
# Returns STR, path to the newly encoded .replay file
def JSONtoReplay( json_path, old_replay_path ):
    """ Re-encode a JSON file to replay using rattletrap. """
    file_name = StripPathToFile( old_replay_path ).split(".")[0] + "_parsed.replay"
    old_path = os.path.split(old_replay_path)[0]
    new_replay_path = os.path.join( old_path, file_name )
    print( "Re-encoding {} to {}...".format( json_path, new_replay_path ) )
    os.system( "win_rattle.exe encode {} > {}".format( json_path, new_replay_path ) )
    print( "Done..." )


# Takes STR, a path
# Returns STR, the ending folder/filename from the path
def StripPathToFile( path ):
    """ Strip a file path down to the last folder/file name. """
    head, tail = ntpath.split(path)
    return tail or ntpath.basename(head)


#Should we be careful if the directory does exist?
def CheckOutputDir():
    """ Ensure that "RL_ReplayName/out" exists. """
    if not os.path.exists( os.path.join( os.getcwd(), "out" ) ):
        os.makedirs( os.path.join( os.getcwd(), "out" ) )

# Finds the primary player name in a decoded replay file
# Takes json object 
# Returns STR, the name of the player who saved the replay
def FindReviewee( jsondata ):
    """ Find the person who is being reviewed's name. """
    return jsondata['header']['properties']['value']['PlayerName']['value']['str_property']


#Takes a json object
#Unnecessary with manual naming, but could be useful in the future.
def FindRevieweeTeam(json_data):
    # Find reviewee's teamID:
    for player in json_data['header']['properties']['value']['PlayerStats']['value']['array_property']:
        player_name = player['value']['Name']['value']['str_property']
        if player_name == FindReviewee(json_data):
            return player['value']['Team']['value']['int_property']

#Takes the team ID for the reviewee - this is unnecessary if using the user input method
#Returns dict, with keys the old player names and values the new player names
#Now takes user input and hopefully works.
def MakeNewnames(json_data):
    player_name_replacements = {}
    #teammate_counter = 1
    #opponent_counter = 1

    for player in json_data['header']['properties']['value']['PlayerStats']['value']['array_property']:
         player_name = player['value']['Name']['value']['str_property']

         #manual naming, ask user for each new name
         player_name_replacements[player_name] = input("Replacement name for " + player_name + "?")

         '''
         automatic naming
        if name == FindReviewee(data):
            newname = "Reviewee"
        else:
            if player['value']['Team']['value']['int_property'] == reviewee_team:
                newname = "Teammate #{}".format( teammate_counter )
                teammate_counter += 1
            else:
                newname = "Opponent #{}".format( opponent_counter )
                opponent_counter += 1
         player_name_replacements[name] = newname
         '''

    return player_name_replacements


#Takes json object
#Returns None and writes to json_file
#Replaces player names in header individually, then str.replace() for the rest of the instances
def ReplaceNames(json_data):
    print( "Replacing names..." )

    #reviewee_team = FindRevieweeTeam(data)
    player_name_replacements = MakeNewnames(json_data)

    # Replace all player names in header
    for player in json_data['header']['properties']['value']['PlayerStats']['value']['array_property']:
        player_name = player['value']['Name']['value']['str_property']
        print( player_name + '->' + player_name_replacements[player_name] )
        player['value']['Name']['value']['str_property'] = player_name_replacements[player_name]
        player['value']['Name']['size'] = len( player_name_replacements[player_name] ) + 3

        # Search Goal data for player names...
        for goal in json_data['header']['properties']['value']['Goals']['value']['array_property']:
            if goal['value']['PlayerName']['value']['str_property'] == player:
                goal['value']['PlayerName']['size'] = len( player_name_replacements[player_name] ) + 3
                goal['value']['PlayerName']['value']['str_property'] = player_name_replacements[player_name]

                
    #json to string
    string_data = json.dumps( json_data )

    # str.replace() the rest
    for player_name in player_name_replacements:
        string_data = string_data.replace( player_name, player_name_replacements[player_name] )


    #string to json - this is slow and probably unnecessary, but possibly preferable for adding functionality.  Look into this once we get more stuff working
    json_data = json.loads( string_data )
    return json_data



#Change player camera settings.
#Takes json object
#Returns json object
#Right now this will change all players' camera settings to the user inputted settings.
#Once we figure out where these are in the json we can do it individually.
def ChangeCameras(json_data):
    string_data = json.dumps(json_data)

    new_fov = input("Change FOV to:")
    new_height = input("Change camera height to:")
    new_angle = input("Change camera angle to:")
    new_distance = input("Change camera distance to:")
    new_stiffness = input("Change camera stiffness to:")
    new_swivel_speed = input("Change camera swivel speed to:")

    string_data = re.sub( r"\"fov\": \d*",  "\"fov\": " + new_fov , string_data)
    string_data = re.sub( r"\"height\": \d*",  "\"height\": " + new_height , string_data)
    string_data = re.sub( r"\"angle\": -?\d*",  "\"angle\": " + new_angle, string_data)
    string_data = re.sub( r"\"distance\": \d*",  "\"distance\": " + new_distance, string_data)
    string_data = re.sub( r"\"stiffness\": \d\.?\d*",  "\"stiffness\": " + new_stiffness , string_data)
    string_data = re.sub( r"\"swivel_speed\": \d*\.?\d*",  "\"swivel_speed\": " + new_swivel_speed, string_data)

    json_data = json.loads(string_data)
    return json_data





'''
def GetPlayerNames(json_data):
    """ Return a list of names for all players present in this replay. """
    print( "Getting player roster..." )
    return [ key['value']['Name']['value']['str_property'] for key in json_data['header']['properties']['value']['PlayerStats']['value']['array_property'] ]
'''

#Changes the in-game replay name to a user provided value
#Takes json object
#Returns json object
def RenameReplay(json_data):
    new_replay_name = input("New name for replay?")
    replay_name = json_data['header']['properties']['value']['ReplayName']['value']['str_property']
    print( "Renaming replay from \"" + replay_name + "\" to \"" + new_replay_name + "\"..." )
    json_data['header']['properties']['value']['ReplayName']['value']['str_property'] = new_replay_name
    return json_data

    
if __name__ == "__main__":
    args = sys.argv[1:]
    if len( args ) < 1:
        raise SyntaxError( "There must be at least one argument. None passed." )
    CheckOutputDir()
    for arg in args:
        json_file = ReplayToJSON( arg )
        with open( json_file, 'r' ) as f:
            json_data = json.load( f )
        
        json_data = RenameReplay(json_data)
        json_data = ReplaceNames(json_data)
        json_data = ChangeCameras(json_data)

        with open( json_file, 'w' ) as f:
            json.dump( json_data, f )
            
        JSONtoReplay( json_file, arg )
        
