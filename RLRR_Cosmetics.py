"""
    Name:
        RLRR_Cosmetics.py
    Author:
        Relic
    Date:
        12/27/2017

    -----------------------------------------------------------------------------

    Purpose:
        Provides class storage for cosmetic information about a given player.

"""

import json, os
from enum import Enum

class CosmeticItemType( Enum ):
    BOOST            = ( 0, "Boost"         )
    WHEELS           = ( 1, "Wheel"         )
    ANTENNA          = ( 2, "Antenna"       )
    TRAIL            = ( 3, "Trail"         )
    TOPPER           = ( 4, "Topper"        )
    GOAL_EXPLOSION   = ( 5, "GoalExplosion" )
    ENGINE_SOUND     = ( 6, "EngineSound"   )
    CAR_BODY         = ( 7, "CarBody"       )

with open( os.path.join( os.getcwd(), r"\data\rldatabase.rldb" ) ) as f:
    cosmetic_data = json.load( f )

    




class CarBody( object ):
    car_data = cosmetic_data['CarBodies']
    def __init__( self, name, paint_color = None ):
        if name not in self.__class__.GetCarNames():
            raise ValueError( "CarBody initialized with invalid name. {} passed.".format( name ) )
        else:
            self.name   = name

        if self.__class__.IsPaintable( self.name ):
            self.paintable   = self.__class__.IsPaintable( self.name )
            if paint_color in self.__class__.GetValidPaintColors( paint_color ):
                self.paint_color = paint_color


        self.hitbox_type = hitbox

    def IsPainted( self ):
        return self.paint_color != None

    @classmethod
    def GetCarNames( cls ):
        return [ x for x in car_data.keys() ]


    @classmethod
    def GetRattletrapID( cls, car_name ):
        return car_data[ car_name ]["rattletrap_value"]


    @classmethod
    def GetValidPaintColors( cls, car_name ):
        return cls.car_data[car_name]["valid_paint_colors"]


    @classmethod
    def CarIsPaintable( cls, car_name ):
        return cls.car_data[car_name]["paintable"]


class PlayerCosmetics( object ):
    def __init__( self,
                carbody = CarBody("Octane"),
                wheels = None,
                boost = None,
                trail = None,
                decal = None,
                paint_colors = ( None, None ),
                paint_types = ( None, None ) ):
        self.primary_paint   = paint_types[0]
        self.secondary_paint = paint_types[1]

        self.primary_color   = paint_colors[0]
        self.secondary_color = paint_colors[1]
        
        self.carbody = carbody
        self.decal = decal
        self.boost = boost
        self.trail = trail
        self.wheels = wheels
