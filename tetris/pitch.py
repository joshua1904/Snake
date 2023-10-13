import copy
from collections import deque
from tetris.forms.form import Form
from tetris.forms.quadrangle import Quadrangle
from tetris.tetris_assets import clear_row
PIXEL_MAP = {0: "grey", 1: "red", 2: "blue", 3: "green", 4: "yellow", 5: "violet"}


class Pitch:
    def __init__(self):
        self.width = 10
        self.height = 20
        pitch_list = [[0] * self.width, [0] * self.width, [0] * self.width, [0] * self.width, [0] * self.width,
                      [0] * self.width, [0] * self.width, [0] * self.width, [0] * self.width, [0] * self.width,
                      [0] * self.width, [0] * self.width, [0] * self.width, [0] * self.width, [0] * self.width,
                      [0] * self.width, [0] * self.width, [0] * self.width, [0] * self.width, [0] * self.width]
        self.pitch_list = deque(pitch_list)
        self.moving_form: Form | Quadrangle = None
        self.next_form = None
        self.change_form = None

    def add_form_to_pitch(self):
        color_int = self.moving_form.get_color_int()
        for pos in self.moving_form.get_pixel_positions():
            self.pitch_list[pos[0]][pos[1]] = color_int

    def delete_form_from_pitch(self, pixel_positions: list):
        for pos in pixel_positions:
            self.pitch_list[pos[0]][pos[1]] = 0

    def add_moving_form(self, next_form):
        self.moving_form = self.next_form
        self.next_form = next_form

    def destroy_row_if_full(self) -> int:
        rows_to_clear = 0
        for counter, row in enumerate(self.pitch_list):
            if 0 not in row:
                self.pitch_list[counter] = [0] * self.width
                rows_to_clear +=1
        if rows_to_clear == 0:
            return
        changed = False
        while True:
            for counter, row in enumerate(self.pitch_list):
                if counter < len(self.pitch_list) - 1:
                    if sum([1 for i in row if i != 0]) > 0 and self.pitch_list[counter + 1].count(0) == self.width:
                        self.pitch_list[counter] = [0] * self.width
                        self.pitch_list[counter + 1] = copy.deepcopy(row)
                        changed = True
                        clear_row.play()
            if not changed:
                break
            changed = False
        return rows_to_clear

