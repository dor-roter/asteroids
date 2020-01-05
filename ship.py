################################################
# File: ship.py
# # Writer: Asif Kagan, Dor Roter
# # Login: asifka, dor.roter
# # Exercise: ------
# # More:
# #       Consulted: -----
# #       Internet:
# #       Notes:
# ################################################
from game_object import GameObject
from torpedo import Torpedo
import math


class Ship(GameObject):
    """
    A class extending GameObject describing a spaceship in our game
    """

    # public static constants
    RADIUS = 1
    TURN = 7
    MAX_HEADING = 360
    MIN_HEADING = 0

    def __init__(self, coordinate, speed_vec, heading):
        """
        Constructor method to generate a ship
        :param coordinate: a tuple representing the x, y initial coordinates
        :type coordinate: Tuple: (int, int)
        :param speed_vec: a tuple representing the x, y initial speeds
        :type speed_vec: Tuple: (int, int)
        :param heading: the initial heading in degrees of the torpedo
        :type heading: int
        """
        self.__heading = heading
        super().__init__(coordinate, speed_vec, Ship.RADIUS)

    def turn_right(self):
        """
        Method to turn ship right by Ship.TURN degrees
        """
        turn = self.__heading - Ship.TURN
        if turn < Ship.MIN_HEADING:
            turn += Ship.MAX_HEADING
        self.__heading = turn

    def turn_left(self):
        """
        Method to turn ship left by Ship.TURN degrees
        """
        turn = self.__heading + Ship.TURN
        if turn >= Ship.MAX_HEADING:
            turn -= Ship.MAX_HEADING
        self.__heading = turn

    def accelerate(self):
        """
        Method to accelerate the ship
        """
        x_speed = self.__calc_speed(Ship._X)
        y_speed = self.__calc_speed(Ship._Y)
        self._speed_vect = (x_speed, y_speed)

    def fire_torpedo(self):
        """
        Method to fire a torpedo
        :return: Torpedo
        """
        return Torpedo(self)

    def get_draw_data(self):
        """
        Method to get a tuple representing all necessary data for a draw.
        :return: Tuple (int, int, int)
        """
        x, y = self._coordinates
        return x, y, self.__heading

    def get_heading(self):
        """
        Method to get the current ship heading
        :return: int
        """
        return self.__heading

    def __calc_speed(self, axis):
        """
        Private function to calculate and return the new speed of the ship after
        after accelerating.
        :param axis: 0/1 representing x or y axis
        :type axis: int
        :return: float
        """
        old_speed = self._speed_vect[axis]
        radian = math.radians(self.__heading)

        if axis == Ship._X:
            heading_factor = math.cos(radian)
        else:
            # axis == Ship.Y
            heading_factor = math.sin(radian)

        return old_speed + heading_factor
