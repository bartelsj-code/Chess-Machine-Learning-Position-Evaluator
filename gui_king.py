from gui_piece import GUIPiece
from graphics import *

class GUIKing(GUIPiece):
    def __init__(self, color, square, win):
        super().__init__(color, square, win)
        self.piece_type = "K"

    def make_shape(self):
        x, y, s = self.get_location_and_scale()
        #body
        p2 = Point(x + 0.02*s, y  -0.3*s)
        p3 = Point(x + 0.02*s, y -0.26*s)
        p4 = Point(x + 0.06*s, y -0.26*s)
        p5 = Point(x + 0.06*s, y -0.22*s)
        p6 = Point(x + 0.02*s, y -0.22*s)
        p7 = Point(x + 0.02*s, y -0.18*s)
        p8 = Point(x + 0.15*s, y - 0.16*s)
        p9 = Point(x+0.04*s, y-0.0*s)
        p10 = Point(x-0.04*s, y-0.0*s)
        p11 = Point(x - 0.15*s, y - 0.16*s)
        p12 = Point(x - 0.02*s, y -0.18*s)
        p13 = Point(x - 0.02*s, y -0.22*s)
        p14 = Point(x - 0.06*s, y -0.22*s)
        p15 = Point(x - 0.06*s, y -0.26*s)
        p16 = Point(x - 0.02*s, y -0.26*s)
        p1 = Point(x - 0.02*s, y  -0.3*s)
        
        self.shape.append(Polygon(p1,p2,p3,p4,p5,p6,p7,p8,p9,p10,p11,p12,p13,p14,p15,p16))
        #body

        y -= 0.05*s
        p1 = Point(x - 0.04*s, y + 0*s)
        p2 = Point(x + 0.04*s, y + 0*s)
        p3 = Point(x + 0.06*s, y + 0.25*s) 
        p4 = Point(x + 0.14*s, y + 0.28*s) 
        p5 = Point(x + 0.16*s, y + 0.32*s) 
        p6 = Point(x + 0.16*s, y + 0.35*s) 
        p7 = Point(x - 0.16*s, y + 0.35*s) 
        p8 = Point(x - 0.16*s, y + 0.32*s) 
        p9 = Point(x - 0.14*s, y + 0.28*s) 
        p10 = Point(x - 0.06*s, y + 0.25*s)
        self.shape.append(Polygon(p1, p2, p3, p4, p5, p6, p7, p8, p9, p10))
        #neck
        y += 0.04*s
        p1 = Point(x, y - 0.08*s)
        p2 = Point(x-0.13*s, y - 0.05*s)
        p3 = Point(x-0.13*s, y - 0.02*s)
        p4 = Point(x, y + 0.01*s)
        p5 = Point(x+0.13*s, y - 0.02*s)
        p6 = Point(x+0.13*s, y - 0.05*s)
        self.shape.append(Polygon(p1, p2, p3,p4,p5,p6))
        
        
