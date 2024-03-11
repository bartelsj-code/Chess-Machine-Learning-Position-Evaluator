class PSWsquare:
    def __init__(self, x, square_length, square_height):
        self.x = x*square_length
        self.scale = square_height
        self.square_height = square_height
        self.square_length = square_length
        self.coords = (0,0)

    def get_center_coords(self):
        middle_x = self.x + self.square_length / 2
        y = self.square_height / 2
        return (middle_x, y)
    
    def get_scaling_unit(self):
        return self.scale
    