################################################
# File: torpedo.py
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


class Torpedo(GameObject):
    RADIUS = 4
    LIFE_SPAN = 200

    def __init__(self, coordinate, ship_speed, heading):
        self.__heading = heading
        self.__time_alive = 0

        speed_vec = self.__calc_speed(ship_speed)
        super().__init__(coordinate, speed_vec, Torpedo.RADIUS)

    def __calc_speed(self, ship_speed):
        ship_x, ship_y = ship_speed
        rad_heading = math.radians(self.__heading)
        x_speed = ship_x + 2*math.cos(rad_heading)
        y_speed = ship_y + 2*math.sin(rad_heading)

        return x_speed, y_speed

    def get_heading(self):
        return self.__heading

    def get_data(self):
        x, y = self._coordinates
        return x, y, self.__heading

    def time_tick(self):
        self.__time_alive += 1
        return self.__time_alive <= Torpedo.LIFE_SPAN

