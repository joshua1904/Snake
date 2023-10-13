from collections import deque

SPINS = ["normal", "right", "down", "left"]

class Form:
    def __init__(self, x_pos: int, y_pos, rotation="normal"):
        self.y_pos = y_pos
        self.x_pos = x_pos
        self.rotation = rotation
    def move_down(self):
            self.y_pos += 1

    def move_right(self):
        self.x_pos += 1

    def move_left(self):
        self.x_pos -= 1

    def rotate(self, instruction):
        if instruction == "up":
            current_spin_index = SPINS.index(self.rotation)
            if current_spin_index < 3:
                self.rotation = SPINS[current_spin_index + 1]
            else:
                self.rotation = SPINS[0]
        if instruction == "down":
            current_spin_index = SPINS.index(self.rotation)
            if current_spin_index >= 0:
                self.rotation = SPINS[current_spin_index - 1]
            else:
                self.rotation = SPINS[0]
    def get_pos(self) -> tuple:
        return self.x_pos, self.y_pos

    def set_pos(self, x: int, y: int):
        self.y_pos = y
        self.x_pos = x
