from tetris.forms.form import Form

class Line(Form):
    def __init(self):
        pass

    def get_color_int(self) -> int:
        #key of PIXEL_MAP in pitch.py
        return 1

    def get_pixel_positions(self):
        if self.rotation == "normal":
            return (self.y_pos, self.x_pos), (self.y_pos, self.x_pos + 1), (self.y_pos, self.x_pos  + 2), (self.y_pos, self.x_pos + 3)
        if self.rotation == "right":
            return (self.y_pos - 1, self.x_pos + 2), (self.y_pos, self.x_pos + 2), (self.y_pos +1, self.x_pos + 2), (
            self.y_pos + 2, self.x_pos + 2)
        if self.rotation == "down":
            return (self.y_pos + 1, self.x_pos), (self.y_pos + 1, self.x_pos + 1), (self.y_pos + 1, self.x_pos + 2), (
            self.y_pos + 1, self.x_pos + 3)
        if self.rotation == "left":
            return (self.y_pos - 1, self.x_pos + 1), (self.y_pos, self.x_pos + 1), (self.y_pos +1, self.x_pos + 1), (
            self.y_pos + 2, self.x_pos + 1)
