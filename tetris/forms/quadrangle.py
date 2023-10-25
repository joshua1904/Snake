from tetris.forms.form import Form

class Quadrangle(Form):
    def __init(self):
        pass

    def get_color_int(self) -> tuple:
        if self.rotation == "normal":
            return 1, 2, 3, 4
        if self.rotation == "right":
            return 5, 6, 7, 8
        if self.rotation == "down":
            return 9, 10, 11, 12
        if self.rotation == "left":
            return 13, 14, 15, 16

    def get_pixel_positions(self):
        return (self.y_pos, self.x_pos), (self.y_pos, self.x_pos + 1), (self.y_pos +1, self.x_pos), (self.y_pos + 1, self.x_pos + 1)



