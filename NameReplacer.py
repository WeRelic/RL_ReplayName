"""
    Name:
        NameReplacer.py
    Author:
        Relic
    Date:
        12/17/2017

    -----------------------------------------------------------------------------
    
    Purpose:    
        Change Rocket League player names using rattletrap.

    Default Behavior:
        After loading the .REPLAY passed as CLI argument;
        This script uses rattletrap to convert that replay to a minified JSON file.

        Changes all player names in a rocket league replay to:
            Reviewee
            Opponent #
            Teammate #
        Where # is an incrementing counter.

        
    Usage:
        NameReplacer.py <path/to/replay1.replay> <path/to/replay2.replay> ...
        
"""


import os, sys, json, subprocess, ntpath, operator, functools, copy, time

rattlepath = os.path.join( os.getcwd(), "win_rattle.exe" )
player_name_replacements = []
paths, path = ([], [])

# Rattletrap Interface:
def ReplayToJSON( replay ):
    """ Convert a replay to JSON using rattletrap. """
    print( "Parsing {} to JSON...".format( replay ) )
    json_name = StripPathToFile(replay).split( "." )[0]
    json_path = os.path.join( os.getcwd(), "out", "{}.json".format(json_name) )
    os.system( "{} decode {} > {}".format( rattlepath, replay, json_path ) )
    print( "Done..." )
    return json_path

def JSONtoReplay( json_path, old_replay_path ):
    """ Re-encode a JSON file to replay using rattletrap. """
    file_name = StripPathToFile( old_replay_path ).split(".")[0] + "_parsed.replay"
    old_path = os.path.split(old_replay_path)[0]
    new_replay_path = os.path.join( old_path, file_name )
    print( "Re-encoding {} to {}...".format( json_path, new_replay_path ) )
    os.system( "{} encode {} > {}".format( rattlepath, json_path, new_replay_path ) )
    print( "Done..." )




# OS Interface:
def StripPathToFile( path ):
    """ Strip a file path down to the last folder/file name. """
    head, tail = ntpath.split(path)
    return tail or ntpath.basename(head)

def CheckOutputDir():
    """ Ensure that "RL_ReplayName/out" exists. """
    if not os.path.exists( os.path.join( os.getcwd(), "out" ) ):
        os.makedirs( os.path.join( os.getcwd(), "out" ) )


def FindReviewee( jsondata ):
    """ Find the person who is being reviewed's name. """
    return jsondata['header']['properties']['value']['PlayerName']['value']['str_property']


def ReplaceNames():
    """ Replace all names with generic names. """
    global player_name_replacements, paths, path, data
    print( "Replacing names..." )
    reviewee_team = None
    teammate_counter = 1
    opponent_counter = 1
    index = 0
    # Find reviewee's teamID:
    for player in data['header']['properties']['value']['PlayerStats']['value']['array_property']:
        name = player['value']['Name']['value']['str_property']
        if name == FindReviewee(data):
            reviewee_team = player['value']['Team']['value']['int_property']
            
    # Iterate names, renaming players based on their team.
    for player in data['header']['properties']['value']['PlayerStats']['value']['array_property']:
        # Get the current player's name. 
        name = player['value']['Name']['value']['str_property']
        
        if name == FindReviewee(data):
            newname = "Reviewee"
        else:
            if player['value']['Team']['value']['int_property'] == reviewee_team:
                newname = "Teammate #{}".format( teammate_counter )
                teammate_counter += 1
            else:
                newname = "Opponent #{}".format( opponent_counter )
                opponent_counter += 1

        print( "{} -> {}".format( name, newname ) )
        player_name_replacements.append( (name, newname) )
        player['value']['Name']['value']['str_property'] = newname
        player['value']['Name']['size'] = len( newname ) + 3
        index += 1

        # Search Goal data for player names...
        for goal in data['header']['properties']['value']['Goals']['value']['array_property']:
            if goal['value']['PlayerName']['value']['str_property'] == name:
                goal['value']['PlayerName']['size'] = len( newname ) + 3
                goal['value']['PlayerName']['value']['str_property'] = newname

    return data





def GetPlayerNames():
    """ Return a list of names for all players present in this replay. """
    global data
    print( "Getting player roster..." )
    return [ key['value']['Name']['value']['str_property'] for key in data['header']['properties']['value']['PlayerStats']['value']['array_property'] ]


def RenameReplay():
    """ Append "_names_fixed" to the replay file's name. """
    global data
    print( "Renaming replay from '{0}' to '{0}_parsed'...".format( data['header']['properties']['value']['ReplayName']['value']['str_property'] ) )
    name = data['header']['properties']['value']['ReplayName']['value']['str_property']
    data['header']['properties']['value']['ReplayName']['value']['str_property'] = "{}_parsed".format( name )
    return data
    
if __name__ == "__main__":
    args = sys.argv[1:]
    if len( args ) < 1:
        raise SyntaxError( "There must be at least one argument. None passed." )
    CheckOutputDir()
    for arg in args:
        json_file = ReplayToJSON( arg )
        with open( json_file, 'r' ) as f:
            data = json.load( f )
        
        #data = RenameReplay()
        data = ReplaceNames()

        # Here there be hackish code:
        with open( json_file, 'w' ) as f:
            json.dump( data, f )

        with open( json_file, 'r' ) as f:
            jdata = f.read()
            for i in player_name_replacements:
                jdata = jdata.replace( i[0], i[1] )
        with open( json_file, 'w' ) as f:
            f.write( jdata )

            
        JSONtoReplay( json_file, arg )
        
