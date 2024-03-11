from player import Player
from move import Move
import random

class Bot(Player):
    def __init__(self, color, board):
        super().__init__(color, board)

    def choose_move(self):
        #Random move selection
        gamestate = self.board.position.perfect_clone()
        moves = gamestate.get_possible_moves()
        random.shuffle(moves)
        return moves[0]
    
    def do_turn(self):
        return super().do_turn()
