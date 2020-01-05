################################################
# File: asteroids_main.py
# Writer: Asif Kagan, Dor Roter
# Login: asifka, dor.roter
# Exercise: ------
# More:
#       Consulted: -----
#       Internet:
#       Notes:
################################################
from screen import Screen
from ship import Ship
from asteroid import Asteroid
import sys
import math
import random


DEFAULT_ASTEROIDS_NUM = 5


class GameRunner:
    """
    A class running an asteroids game using Screen class to handle graphics
    """
    # private static constants
    __X = 0
    __Y = 1

    # games public static constants
    ASTR_SPEEDS = list(range(-4, -1)) + list(range(1, 4))
    ASTR_INT_SIZE = 3
    SHIP_INIT_SPEED = (0, 0)
    SHIP_INIT_HEADING = 0
    ASTR_HIT_VALS = {3: 20, 2: 50, 1: 100}
    MAX_TORPEDOS = 10
    INIT_LIVES = 3

    HIT_TITLE = "Watch out!"
    HIT_MSG = "You have been hit by an asteroid."
    HIT_WARN = HIT_TITLE, HIT_MSG
    LOST_TITLE = "Game Over!"
    LOST_MSG = "You have no more lives left."
    LOST_ALERT = LOST_TITLE, LOST_MSG
    WIN_TITLE = "You Won!"
    WIN_MSG = "You destroyed all asteroids."
    WIN_ALERT = WIN_TITLE, WIN_MSG
    QUITE_TITLE = "Closing Game"
    QUITE_MSG = "Hope to see you again!"
    QUITE_ALERT = QUITE_TITLE, QUITE_MSG

    def __init__(self, asteroids_amount):
        """
        Constructor method, sets up all parameters needed before starting a
        game
        :param asteroids_amount: the amount of asteroid to start the game with
        :type asteroids_amount: int
        """
        self.__screen = Screen()

        self.__screen_max_x = Screen.SCREEN_MAX_X
        self.__screen_max_y = Screen.SCREEN_MAX_Y
        self.__screen_min_x = Screen.SCREEN_MIN_X
        self.__screen_min_y = Screen.SCREEN_MIN_Y

        self.__screen_min = self.__screen_min_x, self.__screen_min_y
        self.__screen_max = self.__screen_max_x, self.__screen_max_x
        self.__screen_dimensions = self.__screen_min, self.__screen_max

        # initiate game objects
        self.__spaceship = self._create_ship()
        self.__asteroids = self._get_asteroids(asteroids_amount)
        self.__torpedos = list()

        # initiate game counters
        self.__score = 0
        self.__lives = GameRunner.INIT_LIVES

        # first draws
        self._draw_ship()
        self._draw_asteroids()
        self._draw__torpedos()

    def run(self):
        """
        Method to run the game
        """
        self._do_loop()
        self.__screen.start_screen()

    def _do_loop(self):
        """
        Private game set up method
        """
        # You should not to change this method!
        self._game_loop()
        # Set the timer to go off again
        self.__screen.update()
        self.__screen.ontimer(self._do_loop, 5)

    def _game_loop(self):
        """
        per screen update
        """
        self._controls_handler()

        # updates
        self.__spaceship.move(*self.__screen_dimensions)
        self._move_asteroids()
        self._move_torpedos()

        # limit life time of torpedos
        self._torpedos_life_time()

        # collisions
        self._check_collisions()

        # draw
        self._draw_ship()
        self._draw_asteroids()
        self._draw__torpedos()

        # is game over
        self._is_finished()

    def _is_finished(self):
        """
        A method to check and handle a finished game
        """
        if self.__screen.should_end():
            # pressed exit key
            self.exit_game(*GameRunner.QUITE_ALERT)
        if self.__lives <= 0:
            # out of lives
            self.exit_game(*GameRunner.LOST_ALERT)
        if len(self.__asteroids) == 0:
            # no more asteroids
            self.exit_game(*GameRunner.WIN_ALERT)

    def _torpedos_life_time(self):
        """
        A method to update and check all torpedos life time and remove
        any blown up torpedos
        """
        for torpedo in self.__torpedos:
            if not torpedo.time_tick():
                self._remove_torpedo(torpedo)

    def _check_collisions(self):
        """
        A method to check and treat any collisions of torpedos or the
        ship with any of the asteroids.
        """
        for asteroid in self.__asteroids:
            if asteroid.has_intersection(self.__spaceship):
                self._remove_life()
                self._remove_asteroid(asteroid)
                # asteroid removed - continue to next
                continue
            else:
                for torpedo in self.__torpedos:
                    if asteroid.has_intersection(torpedo):
                        self._handle_asteroid_hit(asteroid, torpedo)

                        self._remove_torpedo(torpedo)
                        self._update_score(asteroid)
                        # asteroid removed - continue to next
                        break

    def _remove_life(self):
        """
        A method to remove a life from the user
        """
        if self.__lives > 0:
            self.__screen.show_message(*GameRunner.HIT_WARN)
            self.__screen.remove_life()
            self.__lives -= 1

    def _handle_asteroid_hit(self, asteroid, torpedo):
        """
        Private function to handle an asteroid hit by a torpedo
        :param asteroid: the asteroid that got hit
        :type asteroid: Asteroid
        :param torpedo: the hitting torpedo
        :type torpedo: Torpedo
        """
        size = asteroid.get_size()

        if size > 1:
            new_size = size - 1
            new_speeds = self.__sub_asteroids_speed(asteroid, torpedo)
            coordinates = asteroid.get_coordinates()
            sub_astr_1 = Asteroid(coordinates, new_speeds[0], new_size)
            sub_astr_2 = Asteroid(coordinates, new_speeds[1], new_size)

            self.__screen.register_asteroid(sub_astr_1, new_size)
            self.__asteroids.append(sub_astr_1)
            self.__screen.register_asteroid(sub_astr_2, new_size)
            self.__asteroids.append(sub_astr_2)

        self._remove_asteroid(asteroid)

    def __sub_asteroids_speed(self, asteroid, torpedo):
        """
        Private function to calculate the new sub asteroids speeds
        :param asteroid:
        :param torpedo:
        :return: Tuple: (float, float)
        """
        new_x = self.__asteroid_speed_formula(GameRunner.__X, asteroid, torpedo)
        new_y = self.__asteroid_speed_formula(GameRunner.__Y, asteroid, torpedo)
        return (new_x, new_y), ((-1*new_x), (-1*new_y))

    def __asteroid_speed_formula(self, axis, asteroid, torpedo):
        """
        Private function to preform the new asteroid speed calculations per
        axis
        :param axis: the required axis (x=X/y=Y)
        :type axis: int
        :param asteroid: the asteroid of which we are creating sub asteroids
        :type asteroid: Asteroid
        :param torpedo: the hitting torpedo
        :type torpedo: Torpedo
        :return: float
        """
        old_speed = asteroid.get_speed()
        numerator = torpedo.get_speed()[axis] + old_speed[axis]
        denominator = math.sqrt(old_speed[GameRunner.__X] ** 2 +
                                old_speed[GameRunner.__Y] ** 2)
        return numerator / denominator

    def _update_score(self, hit_asteroid):
        """
        A method to update the score based on a asteroid hit
        :param hit_asteroid: the asteroid destroyed by a torpedo
        :return:
        """
        size = hit_asteroid.get_size()
        self.__score += GameRunner.ASTR_HIT_VALS[size]
        self.__screen.set_score(self.__score)

    def _remove_torpedo(self, torpedo):
        """
        A method to remove a torpedo from the game
        :param torpedo: the torpedo to be removed
        :type torpedo: Torpedo
        """
        self.__screen.unregister_torpedo(torpedo)
        self.__torpedos.remove(torpedo)

    def _remove_asteroid(self, asteroid):
        """
        A method to remove an asteroid from the game
        :param asteroid: the asteroid to be removed
        :type asteroid: Asteroid
        """
        self.__screen.unregister_asteroid(asteroid)
        self.__asteroids.remove(asteroid)

    def _controls_handler(self):
        """
        Private method to handle the users controls for the spaceship
        """
        if self.__screen.is_left_pressed():
            self.__spaceship.turn_left()
        if self.__screen.is_right_pressed():
            self.__spaceship.turn_right()
        if self.__screen.is_up_pressed():
            self.__spaceship.accelerate()
        if self.__screen.is_space_pressed():
            self._fire_torpedo()

    def _fire_torpedo(self):
        """
        A method to shoot torpedo following the game limits
        """
        # limit amount of torpedos allowed
        if len(self.__torpedos) < GameRunner.MAX_TORPEDOS:
            torpedo = self.__spaceship.fire_torpedo()
            self.__screen.register_torpedo(torpedo)
            self.__torpedos.append(torpedo)

    def _draw_ship(self):
        """
        A method to draw the spaceship to the screen using Screen
        """
        self.__screen.draw_ship(*self.__spaceship.get_draw_data())

    def _draw_asteroids(self):
        """
        A method to draw all asteroids to the screen using Screen
        """
        for asteroid in self.__asteroids:
            x, y = asteroid.get_coordinates()
            self.__screen.draw_asteroid(asteroid, x, y)

    def _draw__torpedos(self):
        """
        A method to draw all torpedos to the screen using Screen
        """
        for torpedo in self.__torpedos:
            self.__screen.draw_torpedo(torpedo, *torpedo.get_draw_data())

    def __random_coordinates(self):
        """
        Private function to choose random coordinates on the screen
        :return: Tuple: (int, int)
        """
        x = random.randint(self.__screen_min_x, self.__screen_max_x)
        y = random.randint(self.__screen_min_y, self.__screen_max_y)
        return x, y

    def _create_ship(self):
        """
        A method to create a new ship on random coordinates on the screen
        :return: Ship
        """
        random_loc = self.__random_coordinates()
        return Ship(random_loc, self.SHIP_INIT_SPEED, self.SHIP_INIT_HEADING)

    def _get_asteroids(self, amount):
        """
        A method to create a number of random asteroids as specified by amount,
        making sure none of the intersect with the ship
        :param amount: the amount of asteroids to be created
        :type amount: int
        :return: List: Asteroid
        """
        asteroids_list = list()
        for i in range(amount):
            self.__get_asteroid(asteroids_list)
        return asteroids_list

    def __get_asteroid(self, asteroids_list):
        """
        Private function to add a single random asteroid to a List
        :param asteroids_list: the list to append the asteroid to
        :type asteroids_list: List
        """
        asteroid = self.__create_random_asteroid()
        is_collision = asteroid.has_intersection(self.__spaceship)
        while is_collision:
            asteroid = self.__create_random_asteroid()
            is_collision = asteroid.has_intersection(self.__spaceship)

        self.__screen.register_asteroid(asteroid, asteroid.get_size())
        asteroids_list.append(asteroid)

    def __create_random_asteroid(self):
        """
        Private function to create a random asteroid
        :return: Asteroid
        """
        random_loc = self.__random_coordinates()
        random_speed_x = random.choice(self.ASTR_SPEEDS)
        random_speed_y = random.choice(self.ASTR_SPEEDS)
        speed = random_speed_x, random_speed_y
        return Asteroid(random_loc, speed, self.ASTR_INT_SIZE)

    def _move_asteroids(self):
        """
        A method to move all asteroids according to their properties as game
        objects.
        """
        for asteroid in self.__asteroids:
            asteroid.move(*self.__screen_dimensions)

    def _move_torpedos(self):
        """
        A method to move all torpedos according to their properties as game
        objects.
        """
        for torpedo in self.__torpedos:
            torpedo.move(*self.__screen_dimensions)

    def exit_game(self, title, msg):
        """
        A method to exit the game with a "goodbye" alert
        :param title: the title of the alert box
        :type title: str
        :param msg: the message for the alert box
        :type msg: str
        """
        self.__screen.show_message(title, msg)
        self.__screen.end_game()
        sys.exit()


def main(amount):
    """
    Run the game
    :param amount: amount of asteroids to start the game with
    :type amount: int
    """
    runner = GameRunner(amount)
    runner.run()


if __name__ == "__main__":
    if len(sys.argv) > 1:
        main(int(sys.argv[1]))
    else:
        main(DEFAULT_ASTEROIDS_NUM)
