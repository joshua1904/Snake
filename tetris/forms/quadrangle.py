from tetris.forms.form import Form

class Quadrangle(Form):
    def __init(self):
        pass

    def get_color_int(self) -> int:
        #key of PIXEL_MAP in pitch.py
        return 4

    def get_pixel_positions(self):
        return (self.y_pos, self.x_pos), (self.y_pos, self.x_pos + 1), (self.y_pos +1, self.x_pos), (self.y_pos + 1, self.x_pos + 1)



