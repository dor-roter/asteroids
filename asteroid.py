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
import math


def get_radius(size):
    """
    Private utility function to calculate the asteroids radius based on a given
    size.
    :param size: an asteroids size
    :type size: int
    :return: int
    """
    return (size * 10) - 5


class Asteroid(GameObject):
    """
    A class extending GameObject describing an asteroid in our game
    """

    def __init__(self, coordinate, speed_vec, size):
        """
        Constructor method to generate an asteroid
        :param coordinate: a tuple representing the x,y initial coordinates
        :type coordinate: Tuple: (int, int)
        :param speed_vec: a tuple representing the x,y initial speed
        :type speed_vec: Tuple: (int, int)
        :param size: the size of the asteroid (1-3)
        :type size: int
        """
        # todo - validate size 1-3 and int
        self.__size = size
        super().__init__(coordinate, speed_vec, get_radius(size))

    def get_size(self):
        """
        Method to get the size of an asteroid
        :return: int
        """
        return self.__size

    def has_intersection(self, game_object):
        """
        Method to check if a given game object has crashed into this asteroid
        :param game_object: the game object to preform the check against
        :type game_object: GameObject
        :return: bool
        """
        distance = self.__get_distance(game_object)
        return distance <= (self._radius + game_object.get_radius())

    def __get_distance(self, game_object):
        """
        Private function to calculate thr distance of a given object from this
        asteroid.
        :param game_object: a game object on to calculate its distance from this
        :type game_object: GameObject
        :return: float
        """
        obj_x, obj_y = game_object.get_coordinates()
        self_x, self_y = self._coordinates

        inner = (obj_x-self_x)**2 + (obj_y-self_y)**2
        return math.sqrt(inner)

