from graphics import *
from square_draw_info import SquareDrawInfo
import math

class GUISquare:
    def __init__(self, name, coords, sdi):
        self.name = name
        self.coords = coords
        self.sdi = sdi
        self.win = sdi.get_win()
        self.center_coords = (0,0)
        self.rect = self.make_rect(sdi)
        self.text = self.make_text(sdi)
        self.occupant = None

    def get_center_coords(self):
        return self.center_coords
    
    def get_scaling_unit(self):
        return self.size

    def set_occupant(self, occupant):
        self.occupant = occupant

    def make_rect(self, sdi):
        #create rectange graphic object
        location = sdi.get_location()
        self.size = sdi.get_size()
        color = sdi.get_color()
        x1, y1 = location[0], location[1]
        x2, y2 = x1 + self.size, y1 + self.size
        self.center_coords = ((x1+(x2-x1)/2),(y1+(y2-y1)/2))
        p1 = Point(x1,y1)
        p2 = Point(x2,y2)
        rect = Rectangle(p1, p2)
        rect.setFill(color)
        rect.setWidth(0)
        return rect
    
    def make_text(self, sdi):
        #create grpahic object for square text identifier
        location = sdi.get_location()
        self.size = sdi.get_size()
        color = sdi.get_text_color()
        x1, y1 = location[0]+ 0.12*self.size, location[1] + 0.88*self.size
        p1 = Point(x1,y1)
        text = Text(p1, self.name)
        text.setSize(int(self.size)//7)
        text.setTextColor(color)
        return text
    
    def get_center_coords(self):
        return self.center_coords

    def draw(self):
        self.rect.draw(self.win)
        self.text.draw(self.win)

    def highlight(self):
        self.rect.setFill(self.sdi.get_highlight_color())

    def normalize(self):
        self.rect.setFill(self.sdi.get_color())
