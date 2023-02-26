from enum import IntEnum
from math import sqrt
from time import sleep

import pyautogui


class BotState(IntEnum):
    SEARCHING = 0
    ATTACKING = 1


class Bot:
    _state = BotState.SEARCHING

    def __init__(self, window_coordinates):
        self._window_coords = window_coordinates
        self._object = None

    def make_action(self, objects_positions):
        ...

    def _get_closest_object(self, objects_positions):
        center_x = self._window_coords["left"] + int(self._window_coords["width"] / 2)
        center_y = self._window_coords["top"] + int(self._window_coords["height"] / 2)
        player_position = (center_x, center_y)
        closest_object = None
        closest_distance = None
        for object_pos in objects_positions:
            distance = self._pythagorean_distance(player_position, object_pos)
            if distance < closest_distance:
                closest_object = object_pos
                closest_distance = distance
        return closest_object

    def _click_on_object(object_position):
        pyautogui.moveTo(x=object_position[0], y=object_position[1])
        sleep(0.350)
        pyautogui.click()

    @staticmethod
    def _pythagorean_distance(player_pos, object_pos):
        a2 = (object_pos[0] - player_pos[0]) ** 2
        b2 = (object_pos[1] - player_pos[1]) ** 2
        return sqrt(a2 + b2)
