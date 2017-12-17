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


import os, sys, json, subprocess, ntpath

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
    if not os.path.exists( os.path.join( os.getcwd(), "out" ) )
        os.makedirs( os.path.join( os.getcwd(), "out" ) )
    

def ReplaceNames( data ):
    """ Replace all names with generic names. """
    print( "Replacing names..." )
    reviewee_team = None
    teammate_counter = 1
    opponent_counter = 1
    
    # Find reviewee's teamID:
    for player in data['header']['properties']['value']['PlayerStats']['value']['array_property']:
        name = player['value']['Name']['value']['str_property']
        if name == FindReviewee(data):
            reviewee_team = player['value']['Team']['value']['int_property']
            
    # Iterate names, renaming players based on their team.
    for player in data['header']['properties']['value']['PlayerStats']['value']['array_property']:
        name = player['value']['Name']['value']['str_property']
        if name == FindReviewee(data):
            print( "{} -> {}".format( name, "Reviewee" ) )
            player['value']['Name']['value']['str_property'] = "Reviewee"
        else:
            if player['value']['Team']['value']['int_property'] == reviewee_team:
                print( "{} -> {}".format( name, "Teammate #{}".format( teammate_counter ) ) )
                player['value']['Name']['value']['str_property'] = "Teammate #{}".format( teammate_counter )
                teammate_counter += 1
            else:
                print( "{} -> {}".format( name, "Opponent #{}".format( opponent_counter ) ) )
                player['value']['Name']['value']['str_property'] = "Opponent #{}".format( opponent_counter )
                opponent_counter += 1
    return data
    

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
    with open( json_path, 'w' ) as f:
        f.write( json.dumps( data ) )
    os.system( "{} encode {} > {}".format( rattlepath, json_path, new_replay_path ) )
    print( "Done..." )



def GetPlayerNames( data ):
    """ Return a list of names for all players present in this replay. """
    print( "Getting player roster..." )
    return [ key['value']['Name']['value']['str_property'] for key in data['header']['properties']['value']['PlayerStats']['value']['array_property'] ]


def RenameReplay( data ):
    """ Append "_names_fixed" to the replay file's name. """
    print( "Renaming replay from '{0}' to '{0}_names_fixed'...".format( data['header']['properties']['value']['ReplayName']['value']['str_property'] ) )
    name = data['header']['properties']['value']['ReplayName']['value']['str_property']
    data['header']['properties']['value']['ReplayName']['value']['str_property'] = "{}_names_fixed".format( name )
    return data
    
def ParseArgs():
    """ Parse the command line arguments. """
    args = sys.argv[1:]
    if len( args ) < 1:
        raise SyntaxError( "There must be at least one argument. None passed." )
    CheckOutputDir()
    for arg in args:
        json_file = ReplayToJSON( arg )
        with open( json_file, 'r' ) as f:
            json_data = json.load(f)
            json_data = ReplaceNames( json_data )
            json_data = RenameReplay( json_data )
            JSONtoReplay( json_data, json_file, arg )
    
if __name__ == "__main__":
    ParseArgs()
##    replay_path = r"C:\Relic\Portfolio\RL_ReplayExtractor\Testing\AirTackleReplay.replay"
##
##    # Parsing .REPLAY to .JSON
##    ReplayToJSON( replay_path )
##
##    print( "Loading decoded JSON file..." )
##    with open( os.path.join( os.getcwd(), 'out', StripPathToFile( replay_path ).split(".")[0] + ".json" ) ) as f:
##        data = json.load( f )
##
##
##    print( FindReviewee( data ) )
##    print( GetPlayerNames( data ) )
##    ReplaceNames( data )
##    print( GetPlayerNames( data ) )
##    print( "Original Name: {}".format( data['header']['properties']['value']['ReplayName']['value']['str_property'] ) )
##    RenameReplay( data )
##    print( "New Replay Name: {}".format( data['header']['properties']['value']['ReplayName']['value']['str_property'] ) )
##    pass

    
