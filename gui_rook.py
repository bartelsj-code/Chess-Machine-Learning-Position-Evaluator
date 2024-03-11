from gui_piece import GUIPiece
from graphics import *

class GUIRook(GUIPiece):
    def __init__(self, color, square, win):
        super().__init__(color, square, win)
        self.piece_type = "R"

    def make_shape(self):
        x, y, s = self.get_location_and_scale()
        #body
        y -= 0.05*s
        p1 = Point(x - 0.04*s, y - 0.1*s)
        p2 = Point(x + 0.04*s, y - 0.1*s)
        p3 = Point(x + 0.06*s, y + 0.25*s) 
        p4 = Point(x + 0.14*s, y + 0.28*s) 
        p5 = Point(x + 0.16*s, y + 0.32*s) 
        p6 = Point(x + 0.16*s, y + 0.35*s) 
        p7 = Point(x - 0.16*s, y + 0.35*s) 
        p8 = Point(x - 0.16*s, y + 0.32*s) 
        p9 = Point(x - 0.14*s, y + 0.28*s) 
        p10 = Point(x - 0.06*s, y + 0.25*s)
        self.shape.append(Polygon(p1, p2, p3, p4, p5, p6, p7, p8, p9, p10))
        #head
        y += 0.01*s
        p1 = Point(x-0.09*s, y - 0.19*s)
        p2 = Point(x-0.13*s, y - 0.19*s)
        p3 = Point(x-0.13*s, y - 0.05*s)
        p4 = Point(x-0.10*s, y - 0.02*s)
        p5 = Point(x+0.1*s,  y-0.02*s)
        p6 = Point(x+0.13*s, y - 0.05*s)
        p7 = Point(x+0.13*s, y - 0.19*s)
        p8 = Point(x+0.09*s, y - 0.19*s)
        p9 = Point(x+0.09*s, y - 0.14*s)
        p10= Point(x+0.03*s, y - 0.14*s)
        p11 = Point(x+0.03*s, y - 0.19*s)
        p12 = Point(x-0.03*s, y - 0.19*s)
        p13 = Point(x-0.03*s, y - 0.14*s)
        p14 = Point(x-0.09*s, y - 0.14*s)
        self.shape.append(Polygon(p1, p2, p3,p4,p5,p6,p7,p8,p9,p10,p11,p12,p13,p14))

        