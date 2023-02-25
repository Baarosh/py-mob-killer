from enum import IntEnum
from math import sqrt
import pyautogui
from time import sleep

HIT_POINTS_COLOR = [255,255,255]
class BotState(IntEnum):
    SEARCHING = 0
    ATTACKING = 1


class Bot:
    state = BotState.SEARCHING

    def __init__(self, window_coords):
        self._window_coords = window_coords
        self._state = self.state
        self._target = None

    def action(
        self,
        targets_position,
        player_position,
        hp_pixel_color,
    ):
        if self._state == BotState.SEARCHING:
            if not targets_position and not self._is_target_selected(hp_pixel_color):
                self._state = BotState.SEARCHING
                sleep(0.200)
            elif not targets_position:
                self._state = BotState.ATTACKING
                sleep(0.500)
            else:
                target = self._calculate_closest_target(targets_position)
                self._click_on_target(target)
                self._state = BotState.ATTACKING
                sleep(0.500)
        if self._state == BotState.ATTACKING:
            if not self._is_target_dead(hp_pixel_color):
                self._state = BotState.ATTACKING
                sleep(0.500)
            elif targets_position:
                target = self._calculate_closest_target(targets_position)
                self._click_on_target(target)
                self._state = BotState.ATTACKING
                sleep(0.500)
            else:
                self._state = BotState.SEARCHING

    def _calculate_closest_target(self, targets_position):
        player_position = (self._window_coords['left'] + int(self._window_coords['width']/2), self._window_coords['top'] + int(self._window_coords['height']/2))
        closest_target = (None, None)
        for target_pos in targets_position:
            distance = self._pythagorean_distance(player_position, target_pos)
            if distance > closest_target[1]:
                closest_target = (target_pos, distance)
        return closest_target[0]

    def _is_target_selected(color):
        return color == HIT_POINTS_COLOR

    def _click_on_target(target_pos):
        pyautogui.moveTo(x=target_pos[0], y=target_pos[1])
        sleep(0.350)
        pyautogui.click()

    def _is_target_dead(color):
        return color != HIT_POINTS_COLOR

    @staticmethod
    def _pythagorean_distance(player_pos, target_pos):
            return sqrt((target_pos[0] - player_pos[0])**2 + (target_pos[1] - player_pos[1])**2)
