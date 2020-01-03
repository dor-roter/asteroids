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
import math


def get_radius(size):
    return (size * 10) - 5


class Asteroid(GameObject):
    def __init__(self, coordinate, speed_vec, size):
        # todo - validate size 1-3 and int
        super().__init__(coordinate, speed_vec, get_radius(size))
        self.__size = size

    def get_size(self):
        return self.__size

    def has_intersection(self, game_object):
        distance = self.__get_distance(game_object)
        return distance <= (self._radius + game_object.get_radius())

    def __get_distance(self, game_object):
        obj_x, obj_y = game_object.get_coordinates()
        self_x, self_y = self._coordinates

        inner = (obj_x-self_x)**2 + (obj_y-self_y)**2
        return math.sqrt(inner)

