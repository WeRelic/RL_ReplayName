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


import os, sys, json, subprocess, ntpath, re

rattlepath = os.path.join( os.getcwd(), "win_rattle.exe" )

def StripPathToFile( path ):
    """ Strip a file path down to the last folder/file name. """
    head, tail = ntpath.split(path)
    return tail or ntpath.basename(head)

def FindReviewee( jsonfile_data ):
    """ Find the person who is being reviewed's name. """
    return jsonfile_data['header']['properties']['value']['PlayerName']['value']['str_property']


def CheckOutputDir():
    """ Ensure that "RL_ReplayName/out" exists. """
    if not os.path.exists( os.path.join( os.getcwd(), "out" ) ):
        os.makedirs( os.path.join( os.getcwd(), "out" ) )
    

def ReplaceNames( data, json_datafile ):
    """ Replace all names with generic names. """
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

        # Problem is in this block!
        #json_datafile = ReplaceName( json_datafile, name, newname )
        replacement = "{'kind': 'StrProperty', 'size': " + str( len( newname ) + 5 )
        replacement = replacement + ", 'value': {'str_property': '" + newname + "'}}"
        print( str(player['value']['Name']) + " gets replaced by " + replacement )
        json_datafile = json_datafile.replace( str(player['value']['Name']), replacement )

        
        index += 1
    return (data, json_datafile)
    

def ReplayToJSON( replay ):
    """ Convert a replay to JSON using rattletrap. """
    print( "Parsing {} to JSON...".format( replay ) )
    json_name = StripPathToFile(replay).split( "." )[0]
    json_path = os.path.join( os.getcwd(), "out", "{}.json".format(json_name) )
    os.system( "{} decode {} > {}".format( rattlepath, replay, json_path ) )
    print( "Done..." )
    return json_path


def JSONtoReplay( data, json_path, old_replay_path ):
    """ Re-encode a JSON file to replay using rattletrap. """
    file_name = StripPathToFile( old_replay_path ).split(".")[0] + "_parsed.replay"
    old_path = os.path.split(old_replay_path)[0]
    new_replay_path = os.path.join( old_path, file_name )
    print( "Re-encoding {} to {}...".format( json_path, new_replay_path ) )
    os.system( "{} encode {} > {}".format( rattlepath, json_path, new_replay_path ) )
    print( "Done..." )



def GetPlayerNames( data ):
    """ Return a list of names for all players present in this replay. """
    print( "Getting player roster..." )
    return [ key['value']['Name']['value']['str_property'] for key in data['header']['properties']['value']['PlayerStats']['value']['array_property'] ]


def RenameReplay( data, datafile ):
    """ Append "_names_fixed" to the replay file's name. """
    print( "Renaming replay from '{0}' to '{0}_names_fixed'...".format( data['header']['properties']['value']['ReplayName']['value']['str_property'] ) )
    name = data['header']['properties']['value']['ReplayName']['value']['str_property']
    datafile = datafile.replace( name, "{}_names_fixed".format( name ) )
    return (data, datafile)
    
    
if __name__ == "__main__":
    args = sys.argv[1:]
    if len( args ) < 1:
        raise SyntaxError( "There must be at least one argument. None passed." )
    CheckOutputDir()
    for arg in args:
        json_file = ReplayToJSON( arg )
        with open( json_file, 'r' ) as f:
            json_datafile = f.read()
        json_data = json.loads(json_datafile)
        json_data, json_datafile = ReplaceNames( json_data, json_datafile )
        json_data, json_datafile = RenameReplay( json_data, json_datafile )
        JSONtoReplay( json_data, json_file, arg )
        

    
    with open( json_file ) as f:
        filedata = json.load(f)
    for i in [ key['value']['Name']['value']['str_property'] for key in filedata['header']['properties']['value']['PlayerStats']['value']['array_property'] ]:
        print( i )
        
