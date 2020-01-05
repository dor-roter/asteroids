################################################
# File: game_object.py
# Writer: Asif Kagan, Dor Roter
# Login: asifka, dor.roter
# Exercise: ------
# More:
#       Consulted: -----      
#       Internet: 
#       Notes: 
################################################


class GameObject:
    """
    Base class for all game objects on the screen, each object in the game that
    is moving has it's properties and is able to move based on the specified
    formula.
    """
    # private static constants
    _X = 0
    _Y = 1

    def __init__(self, coordinate, speed_vec, radius):
        """
        Constructor method for a basic GameObject, contains its initial
        coordinates, initial speed vectors, and its radius
        :param coordinate: a tuple representing the x,y initial coordinates
        :type coordinate: Tuple: (int, int)
        :param speed_vec: a tuple representing the x,y initial speed
        :type speed_vec: Tuple: (int, int)
        :param radius: the radius of the object
        :type radius: int
        """
        self._coordinates = coordinate
        self._speed_vect = speed_vec
        self._radius = radius

    def get_speed(self):
        """
        Method to return the x,y speed vectors of the game object
        :return: Tuple: (int, int)
        """
        return self._speed_vect

    def get_coordinates(self):
        """
        Method to return the x,y coordinates of the game object
        :return: Tuple: (int, int)
        """
        return self._coordinates

    def move(self, screen_min, screen_max):
        """
        A method to move the game object a single "step" on the screen
        :param screen_min: a tuple representing the x,y min screen coordinates
        :type screen_min: Tuple: (int, int)
        :param screen_max: a tuple representing the x,y max screen coordinates
        :type screen_max: Tuple: (int, int)
        """
        new_x = self.__move(self._X, screen_min, screen_max)
        new_y = self.__move(self._Y, screen_min, screen_max)
        self._coordinates = new_x, new_y

    def __move(self, axis, screen_min, screen_max):
        """
        Helper function to calculate using the provided formula the x or y axis
        new position
        :param axis: Should X or Y axis new position should be calculated
        :type axis: int
        :param screen_min: a tuple representing the x,y min screen coordinates
        :type screen_min: Tuple: (int, int)
        :param screen_max: a tuple representing the x,y max screen coordinates
        :type screen_max: Tuple: (int, int)
        :return: int
        """
        old = self._coordinates[axis]
        speed = self._speed_vect[axis]
        delta = screen_max[axis] - screen_min[axis]
        return screen_min[axis] + (old + speed - screen_min[axis]) % delta

    def get_radius(self):
        """
        Method for getting the radius of the game object
        :return: int
        """
        return self._radius
