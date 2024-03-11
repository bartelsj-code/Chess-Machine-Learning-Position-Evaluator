from psw_square import PSWsquare
from gui_bishop import GUIBishop
from gui_rook import GUIRook
from gui_queen import GUIQueen
from gui_knight import GUIKnight
from graphics import GraphWin

class PSW:
    def __init__(self, color, color2):
        self.fill_color = color2
        self.color = color
        self.length = 300
        self.height = 100
        self.win = GraphWin("Promotion Piece Selection", self.length, self.height)
        self.types_dict = {0:"N",1:"B",2:"R",3:"Q"}

    def make_pieces(self):
        square_length = self.length//4
        square_height = self.height
        square_list = []
        pieces = []
        for i in range(4):
            square_list.append(PSWsquare(i, square_length, square_height))
        knight = GUIKnight(self.color, square_list[0], self.win)
        pieces.append(knight)
        bishop = GUIBishop(self.color, square_list[1], self.win)
        pieces.append(bishop)
        rook = GUIRook(self.color, square_list[2], self.win)
        pieces.append(rook)
        queen = GUIQueen(self.color, square_list[3], self.win)
        pieces.append(queen)
        return pieces

    def fill(self):
        self.win.setBackground(self.fill_color)
        pieces = self.make_pieces()
        for piece in pieces:
            piece.draw()

    def get_type(self):
        option = self.win.getMouse().getX()//(self.length/4)
        return self.types_dict[option]
    
    def close(self):
        self.win.close()
        