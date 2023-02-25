from enum import IntEnum


class BotState(IntEnum):
    SEARCHING = 0
    MOVING = 1
    ATTACKING = 2


class Bot:
    state = BotState.SEARCHING

    def __init__(self, window_coords):
        self._window_coords = window_coords
        self._state = self.state

    def action(
        self,
        monsters_position,
        player_position,
        hp_pixel_color,
    ):
        pass
