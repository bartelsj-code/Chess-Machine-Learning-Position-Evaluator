from player import Player
from gui import GUI
from psw import PSW
from move import Move
import random

class Human(Player):
    def __init__(self, color, board, gui):
        super().__init__(color, board)
        self.gui = gui

    def choose_move(self): 
        gamestate = self.board.position.perfect_clone()
        moves = gamestate.get_possible_moves()
        return self.get_user_move(moves)
    
    def get_user_move(self, moves):
        d = {}
        d2 = {}
        for move in moves:
            d[move.identifier_pair] = move
            if move.is_promotion:
                d2[(move.identifier_pair, repr(move.promotion_piece)[1])] = move
        coords1 = None
        coords2 = None
        while True:
            coords1 = coords2
            coords2 = self.gui.get_square_from_click()
            if (coords1,coords2) in d:
                if d[(coords1,coords2)].is_promotion == False:
                    return d[(coords1,coords2)]
                else:
                    while True:
                        g = self.gui.get_user_promotion_choice()
                        if ((coords1, coords2), g) in d2:
                            return d2[((coords1, coords2), g)]