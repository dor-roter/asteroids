################################################
# File: game_object.py
# Writer: Dor Roter 
# ID: 208772251
# Login: dor.roter
# Exercise: ------
# More:
#       Consulted: -----      
#       Internet: 
#       Notes: 
################################################


class GameObject:
    X = 0
    Y = 1

    def __init__(self, coordinate, speed_vec, radius):
        self._coordinates = coordinate
        self._speed_vect = speed_vec
        self._radius = radius

    def set_coordinates(self, x, y):
        self._coordinates = x, y

    def set_speed(self, x, y):
        self._speed_vect = x, y

    def get_speed(self):
        return self._speed_vect

    def get_coordinates(self):
        return self._coordinates

    def get_x(self):
        return self._coordinates[GameObject.X]

    def get_y(self):
        return self._coordinates[GameObject.Y]

    def get_vect_x(self):
        return self._speed_vect[GameObject.X]

    def get_vect_y(self):
        return self._speed_vect[GameObject.Y]

    def move(self, screen_min, screen_max):
        new_x = self.__move(self.X, screen_min, screen_max)
        new_y = self.__move(self.Y, screen_min, screen_max)
        self._coordinates = new_x, new_y

    def __move(self, axis, screen_min, screen_max):
        old = self._coordinates[axis]
        speed = self._speed_vect[axis]
        delta = screen_max[axis] - screen_min[axis]
        return screen_min[axis] + (old + speed - screen_min[axis]) % delta

    def get_radius(self):
        return self._radius

