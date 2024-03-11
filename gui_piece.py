from gui_square import GUISquare

class GUIPiece:
    def __init__(self, color, square, win):
        self.color = color
        self.shape = []
        self.center_coords = square.get_center_coords()
        self.square_coords = square.coords
        self.scaling_unit = square.get_scaling_unit()
        self.win = win
        self.make_shape()     

    def set_deltas(self, frame_count):
        self.deltas = []
        start_coords = self.center_coords
        end_coords = self.end_square.get_center_coords()
        total_x_change = end_coords[0] - start_coords[0]
        total_y_change = end_coords[1] - start_coords[1]

        delta_x_change = total_x_change/frame_count 
        delta_y_change = total_y_change/frame_count 
        for i in range(frame_count):
            self.deltas.append((delta_x_change, delta_y_change))
        
    def move(self, deltas):
        delta_x = deltas[0]
        delta_y = deltas[1]
        for part in self.shape:
            part.move(delta_x, delta_y)

    def update_info(self):
        self.center_coords = self.end_square.get_center_coords()

    def set_end_square(self, end_square):
        self.end_square = end_square

    def set_destination_square_coords(self, coords):
        self.destination_square_coords = coords

    def get_location_and_scale(self):
        x = self.center_coords[0]
        y = self.center_coords[1]
        s = self.scaling_unit
        return x, y, s
    
    def get_color_pair(self):
        if self.color == "W":
            return "white", "black"
        else:
            return "black", "white"
    
    def draw(self):
        for part in self.shape:
            color, outline = self.get_color_pair()
            part.setOutline(outline)
            part.setFill(color)
            part.draw(self.win)

    def undraw(self):
        for part in self.shape:
            part.undraw()
            
    def __repr__(self):
        return "{}{}".format(self.color, self.piece_type)
    
    def set_coords(self, coords):
        self.coords = coords