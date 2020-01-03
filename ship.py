################################################
# File: ship.py
# Writer: Dor Roter 
# ID: 208772251
# Login: dor.roter
# Exercise: ------
# More:
#       Consulted: -----      
#       Internet: 
#       Notes: 
################################################
from game_object import GameObject
from torpedo import Torpedo
import math


class Ship(GameObject):
    RADIUS = 1
    TURN = 7
    MAX_HEADING = 360
    MIN_HEADING = 0

    def __init__(self, coordinate, speed_vec, heading):
        super().__init__(coordinate, speed_vec, Ship.RADIUS)

        self.__heading = heading

    def get_heading(self):
        return self.__heading

    def turn_right(self):
        turn = self.__heading - Ship.TURN
        if turn < Ship.MIN_HEADING:
            turn += Ship.MAX_HEADING
        self.__heading = turn

    def turn_left(self):
        turn = self.__heading + Ship.TURN
        if turn >= Ship.MAX_HEADING:
            turn -= Ship.MAX_HEADING
        self.__heading = turn

    def accelerate(self):
        x_speed = self.__calc_speed(Ship.X)
        y_speed = self.__calc_speed(Ship.Y)
        self.set_speed(x_speed, y_speed)

    def __calc_speed(self, axis):
        old_speed = self.get_speed()[axis]
        radian = math.radians(self.__heading)

        if axis == Ship.X:
            heading_factor = math.cos(radian)
        else:
            # axis == Ship.Y
            heading_factor = math.sin(radian)

        return old_speed + heading_factor

    def fire_torpedo(self):
        return Torpedo(self._coordinates, self._speed_vect, self.__heading)

    def get_data(self):
        x, y = self._coordinates
        return x, y, self.__heading
