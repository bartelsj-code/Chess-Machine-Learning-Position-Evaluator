import random
from move import Move


class Player:
    def __init__(self, color, board) -> None:
        self.color = color
        self.board = board

    def choose_move(self):
        pass
        
    def do_turn(self):
        move = self.choose_move()
        try:
            self.board.execute_move(move)
        except:
            return "no luck"
