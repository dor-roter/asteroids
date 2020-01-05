################################################
# File: torpedo.py
# Writer: Asif Kagan, Dor Roter
# Login: asifka, dor.roter
# Exercise: ------
# More:
#       Consulted: -----
#       Internet:
#       Notes:
################################################
from game_object import GameObject
import math


class Torpedo(GameObject):
    """
    A class extending GameObject describing a torpedo in our game
    """

    # public static constants
    RADIUS = 4
    LIFE_SPAN = 200

    def __init__(self, ship):
        """
        Constructor method to generate a torpedo
        :param ship: the launching ship
        :type ship: Ship
        """
        self.__heading = ship.get_heading()
        speed_vec = self.__calc_speed(ship.get_speed())
        super().__init__(ship.get_coordinates(), speed_vec, Torpedo.RADIUS)
        self.__time_alive = 0

    def get_heading(self):
        """
        Method to get the torpedos heading
        :return: int
        """
        return self.__heading

    def get_draw_data(self):
        """
        Method to get a tuple representing all necessary data for a draw.
        :return: Tuple (int, int, int)
        """
        x, y = self._coordinates
        return x, y, self.__heading

    def time_tick(self):
        """
        Method to count the torpedos time alive.
        :return: bool
            True - still alive
            False - timer ran out, the torpedo blew up
        """
        self.__time_alive += 1
        return self.__time_alive <= Torpedo.LIFE_SPAN

    def __calc_speed(self, ship_speed):
        """
        Private util function to calculate the torpedos speed based on the
        launching ship speed.
        :param ship_speed: a tuple representing the launching ships x,y
        initial speed
        :type ship_speed: Tuple: (int, int)
        :return: Tuple: (int, int)
        """
        ship_x, ship_y = ship_speed
        rad_heading = math.radians(self.__heading)
        x_speed = ship_x + 2*math.cos(rad_heading)
        y_speed = ship_y + 2*math.sin(rad_heading)

        return x_speed, y_speed

