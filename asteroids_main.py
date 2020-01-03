from screen import Screen
from ship import Ship
from asteroid import Asteroid
from torpedo import Torpedo
import sys
import math
import random

DEFAULT_ASTEROIDS_NUM = 5


X = 0
Y = 1


class GameRunner:
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
        self.__screen = Screen()

        self.__screen_max_x = Screen.SCREEN_MAX_X
        self.__screen_max_y = Screen.SCREEN_MAX_Y
        self.__screen_min_x = Screen.SCREEN_MIN_X
        self.__screen_min_y = Screen.SCREEN_MIN_Y

        self.__screen_min = self.__screen_min_x, self.__screen_min_y
        self.__screen_max = self.__screen_max_x, self.__screen_max_x
        self.__screen_dimensions = self.__screen_min, self.__screen_max

        # initiate game objects
        self.__spaceship = self.__get_ship()
        self.__asteroids = self.__get_asteroids(asteroids_amount)
        self.__torpedos = list()

        # initiate game counters
        self.__score = 0
        self.__lives = GameRunner.INIT_LIVES

        # first draws
        self.__draw_ship()
        self.__draw_asteroids()
        self.__draw__torpedos()

    def run(self):
        self._do_loop()
        self.__screen.start_screen()

    def _do_loop(self):
        # You should not to change this method!
        self._game_loop()
        # Set the timer to go off again
        self.__screen.update()
        self.__screen.ontimer(self._do_loop, 5)

    def _game_loop(self):
        """
        per screen update
        :return:
        """
        self.__controls_handler()

        # updates
        self.__spaceship.move(*self.__screen_dimensions)
        self.__move_asteroids()
        self.__move_torpedos()

        # limit life time of torpedos
        self.__torpedos_life_time()

        # collisions
        self.__check_collisions()

        # draw
        self.__draw_ship()
        self.__draw_asteroids()
        self.__draw__torpedos()

        # is game over
        self.__is_finished()

    def __is_finished(self):
        if self.__screen.should_end():
            # pressed exit key
            self.exit_game(*GameRunner.QUITE_ALERT)
        if self.__lives <= 0:
            # out of lives
            self.exit_game(*GameRunner.LOST_ALERT)
        if len(self.__asteroids) == 0:
            # no more asteroids
            self.exit_game(*GameRunner.WIN_ALERT)

    def __torpedos_life_time(self):
        for torpedo in self.__torpedos:
            if not torpedo.time_tick():
                self.__remove_torpedo(torpedo)

    def __check_collisions(self):
        for asteroid in self.__asteroids:
            for torpedo in self.__torpedos:
                if asteroid.has_intersection(torpedo):
                    self.__handle_asteroid_hit(asteroid, torpedo)

                    self.__remove_torpedo(torpedo)
                    self.__update_score(asteroid)

            if asteroid.has_intersection(self.__spaceship):
                self.__remove_life()
                self.__remove_asteroid(asteroid)

    def __remove_life(self):
        if self.__lives > 0:
            self.__screen.show_message(*GameRunner.HIT_WARN)
            self.__screen.remove_life()
            self.__lives -= 1

    def __handle_asteroid_hit(self, asteroid, torpedo):
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

        self.__remove_asteroid(asteroid)

    def __sub_asteroids_speed(self, asteroid, torpedo):
        new_x = self.__asteroid_speed_formula(X, asteroid, torpedo)
        new_y = self.__asteroid_speed_formula(Y, asteroid, torpedo)
        return (new_x, new_y), ((-1*new_x), (-1*new_y))

    def __asteroid_speed_formula(self, axis, asteroid, torpedo):
        old_speed = asteroid.get_speed()
        numerator = torpedo.get_speed()[axis] + old_speed[axis]
        denominator = math.sqrt(old_speed[X]**2 + old_speed[Y]**2)
        return numerator / denominator

    def __update_score(self, hit_asteroid):
        size = hit_asteroid.get_size()
        self.__score += GameRunner.ASTR_HIT_VALS[size]
        self.__screen.set_score(self.__score)

    def __remove_torpedo(self, torpedo):
        self.__screen.unregister_torpedo(torpedo)
        self.__torpedos.remove(torpedo)

    def __remove_asteroid(self, asteroid):
        self.__screen.unregister_asteroid(asteroid)
        self.__asteroids.remove(asteroid)

    def __controls_handler(self):
        if self.__screen.is_left_pressed():
            self.__spaceship.turn_left()
        if self.__screen.is_right_pressed():
            self.__spaceship.turn_right()
        if self.__screen.is_up_pressed():
            self.__spaceship.accelerate()
        if self.__screen.is_space_pressed():
            self.__add_torpedo()

    def __add_torpedo(self):
        # limit amount of torpedos allowed
        if len(self.__torpedos) < GameRunner.MAX_TORPEDOS:
            torpedo = self.__spaceship.fire_torpedo()
            self.__screen.register_torpedo(torpedo)
            self.__torpedos.append(torpedo)

    def __draw_ship(self):
        self.__screen.draw_ship(*self.__spaceship.get_data())

    def __draw_asteroids(self):
        for asteroid in self.__asteroids:
            x, y = asteroid.get_coordinates()
            self.__screen.draw_asteroid(asteroid, x, y)

    def __draw__torpedos(self):
        for torpedo in self.__torpedos:
            self.__screen.draw_torpedo(torpedo, *torpedo.get_data())

    def __random_coordinates(self):
        x = random.randint(self.__screen_min_x, self.__screen_max_x)
        y = random.randint(self.__screen_min_y, self.__screen_max_y)
        return x, y

    def __get_ship(self):
        random_loc = self.__random_coordinates()
        return Ship(random_loc, self.SHIP_INIT_SPEED, self.SHIP_INIT_HEADING)

    def __get_asteroids(self, amount):
        asteroids_list = list()
        for i in range(amount):
            self.__get_asteroid(asteroids_list)
        return asteroids_list

    def __get_asteroid(self, asteroids_list):
        asteroid = self.__create_random_asteroid()
        is_collision = asteroid.has_intersection(self.__spaceship)
        while is_collision:
            asteroid = self.__create_random_asteroid()
            is_collision = asteroid.has_intersection(self.__spaceship)

        self.__screen.register_asteroid(asteroid, asteroid.get_size())
        asteroids_list.append(asteroid)

    def __create_random_asteroid(self):
        random_loc = self.__random_coordinates()
        random_speed_x = random.choice(self.ASTR_SPEEDS)
        random_speed_y = random.choice(self.ASTR_SPEEDS)
        speed = random_speed_x, random_speed_y
        return Asteroid(random_loc, speed, self.ASTR_INT_SIZE)

    def __move_asteroids(self):
        for asteroid in self.__asteroids:
            asteroid.move(*self.__screen_dimensions)

    def __move_torpedos(self):
        for torpedo in self.__torpedos:
            torpedo.move(*self.__screen_dimensions)

    def exit_game(self, title, msg):
        self.__screen.show_message(title, msg)
        self.__screen.end_game()
        sys.exit()


def main(amount):
    runner = GameRunner(amount)
    runner.run()


if __name__ == "__main__":
    if len(sys.argv) > 1:
        main(int(sys.argv[1]))
    else:
        main(DEFAULT_ASTEROIDS_NUM)
