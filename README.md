# RL_ReplayName

    Purpose:    
        Change Rocket League player names using rattletrap.

    Default Behavior:
        After loading the .REPLAY passed as CLI argument;
        This script uses rattletrap to convert that replay to a minified JSON file.

        Changes all player names in a rocket league replay to:
            Reviewee
            Opponent #
            Teammate #
        Where # is followed by an incrementing counter value.

        
    Usage:
        NameReplacer.py <path/to/replay1.replay> <path/to/replay2.replay> ...
        
    Rattletrap found here:
        https://github.com/tfausak/rattletrap
        
    