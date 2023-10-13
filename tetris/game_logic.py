import random
from typing import Union

from tetris.pitch import Pitch
from tetris.forms.quadrangle import Quadrangle
from tetris.forms.left_l import LeftL
from tetris.forms.right_l import RighttL
from tetris.forms.red_stair import RedStair
from tetris.forms.t_form import TForm
from tetris.forms.green_stair import GreenStair
from tetris.forms.line import Line
import copy

SCORE_PER_ROW = [40, 100, 300, 1200]

FRAMES_PER_CELL = [48, 43, 38, 33, 28, 23, 18, 13, 8, 6, 5, 5, 5, 4, 4, 4]
class GameLogic:
    def __init__(self):
        self.pitch = Pitch()
        self.pitch.next_form = self.get_random_form()
        self.pitch.add_moving_form(self.get_random_form())
        self.score = 0
        self.complete_rows_cleared = 0
        self.level = 0

    def check_form_collision(self, last_form_pos):
        for pixel in self.pitch.moving_form.get_pixel_positions():
            if pixel[0] >= len(self.pitch.pitch_list):
                self.pitch.moving_form = last_form_pos
                return True
            if self.pitch.pitch_list[pixel[0]][pixel[1]] != 0:
                self.pitch.moving_form = last_form_pos
                return True
        return False

    def game_round(self) -> bool:
        last_form_pos = copy.deepcopy(self.pitch.moving_form)
        self.pitch.moving_form.move_down()
        reached_ground = self.check_form_collision(last_form_pos)
        if reached_ground:
            self.pitch.add_form_to_pitch()
            self.pitch.add_moving_form(self.get_random_form())
            self.score += self.calculate_score(self.pitch.destroy_row_if_full())
            self.level = self.get_level()
            if self.check_form_collision(last_form_pos):
                return False
        return True

    def move_right(self):
        last_form_pos = copy.deepcopy(self.pitch.moving_form)
        self.pitch.moving_form.move_right()
        for pixel in self.pitch.moving_form.get_pixel_positions():
            if pixel[1] >= self.pitch.width:
                self.pitch.moving_form = last_form_pos
                return
            if self.pitch.pitch_list[pixel[0]][pixel[1]]:
                self.pitch.moving_form = last_form_pos
                return

    def move_left(self):
        last_form_pos = copy.deepcopy(self.pitch.moving_form)
        self.pitch.moving_form.move_left()
        for pixel in self.pitch.moving_form.get_pixel_positions():
            if pixel[1] < 0:
                self.pitch.moving_form = last_form_pos
                return
            if self.pitch.pitch_list[pixel[0]][pixel[1]]:
                self.pitch.moving_form = last_form_pos
                return

    def get_random_form(self):
        random_number = random.randint(0, 6)
        if random_number == 0:
            return Quadrangle(2, 0, "normal")
        if random_number == 1:
            return Line(2, 0, "normal")
        if random_number == 2:
            return RedStair(2, 0, "normal")
        if random_number == 3:
            return GreenStair(2, 0, "normal")
        if random_number == 4:
            return TForm(2, 0, "normal")
        if random_number == 5:
            return LeftL(2, 0, "normal")
        if random_number == 6:
            return RighttL(2, 0, "normal")

    def is_valid_move(self) -> bool:
        for pixel in self.pitch.moving_form.get_pixel_positions():
            if pixel[0] < 0:
                return False
            if pixel[0] >= self.pitch.height:
                return False
            if pixel[1] >= self.pitch.width:
                return False
            if pixel[1] < 0:
                return False
            if self.pitch.pitch_list[pixel[0]][pixel[1]] != 0:
                return False
        return True
    def rotate(self, instruction):
        last_form_pos = copy.deepcopy(self.pitch.moving_form)
        self.pitch.moving_form.rotate(instruction)
        if not self.is_valid_move():
            self.pitch.moving_form = last_form_pos

    def get_goal_position(self) -> Union[Quadrangle, Line, LeftL, RighttL, RedStair, GreenStair, TForm]:
        fake_form = copy.deepcopy(self.pitch.moving_form)
        while True:
            last_position = copy.deepcopy(fake_form)
            fake_form.move_down()
            for pixel in fake_form.get_pixel_positions():
                if pixel[0] >= self.pitch.height:
                    return last_position
                if self.pitch.pitch_list[pixel[0]][pixel[1]] != 0:
                    return last_position

    def change_form(self):
        last_form = copy.deepcopy(self.pitch.moving_form)
        last_saved_form = copy.deepcopy(self.pitch.change_form)
        change_form = self.pitch.change_form
        self.pitch.change_form = copy.deepcopy(self.pitch.moving_form)
        x, y = self.pitch.moving_form.get_pos()
        if not change_form:
            self.pitch.add_moving_form(self.get_random_form())
        else:
            self.pitch.moving_form = change_form
        self.pitch.moving_form.set_pos(x, y)
        if not self.is_valid_move():
            self.pitch.moving_form = last_form
            self.pitch.change_form = last_saved_form
        return change_form

    def calculate_score(self, cleared_rows: int):
        if cleared_rows:
            self.complete_rows_cleared += cleared_rows
            return SCORE_PER_ROW[cleared_rows - 1] * (self.get_level() + 1)
        return 0

    def get_level(self):
        level = int(self.complete_rows_cleared / 10)
        if level <= 15:
            return level
        return 15

    def get_speed(self):
        return FRAMES_PER_CELL[self.level]
    #def get_speed()
    def down_boost(self):
        x, y = self.get_goal_position().get_pos()
        self.pitch.moving_form.set_pos(x, y)

