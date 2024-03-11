from bot import Bot
from gamestate import Gamestate
from move import Move

class ReadInBot(Bot):
    def __init__(self, color, board):
        super().__init__(color, board)

    def choose_move(self):
        gamestate = self.board.position.perfect_clone()
        move = self.find_move(gamestate)
        return move

    def find_move(self, gamestate):
        
        goal_move_string = self.move_string
        possible_moves = gamestate.get_possible_moves()
        move_notations_dict = {gamestate.get_notation(move): move for move in possible_moves}
        if goal_move_string in move_notations_dict:
            return move_notations_dict[goal_move_string]
        self.expansions = []
        move = self.disambiguate_moves(gamestate)
        if type(move) == Move:
            return move
        print(gamestate)
        print([gamestate.get_notation(move) for move in possible_moves])
        print(self.expansions)
        print("unrecognized_move {}".format(goal_move_string))
        return None
    
    def disambiguate_moves(self, gamestate):
        goal_move_string = self.move_string
        possible_moves = gamestate.get_possible_moves()
        contenders = []
        for move in possible_moves:
            if gamestate.get_notation(move)[0] == goal_move_string[0]:
                contenders.append(move)
        for move in contenders:
            notation = gamestate.get_notation(move)
            expansions = self.make_expansions(move, notation, gamestate)
            self.expansions.append(expansions)
            if goal_move_string in expansions:
                return move

    def make_expansions(self, move, notation, gamestate):
        start_square = gamestate.name_at_coords(move.coord_pairs[0][0])
        base = notation[0] + "{}" + notation [1:]
        expansion1 = base.format(start_square[0])
        expansion2 = base.format(start_square[1])
        expansion3 = base.format(start_square)
        if notation[-1] == "#":
            expansion4 = notation[:-1] + "+"
            expansion5 = expansion1[:-1] + "+"
            expansion6 = expansion2[:-1] + "+"
            expansion7 = expansion3[:-1] + "+"
            return (expansion1, expansion2, expansion3, expansion4, expansion5, expansion6, expansion7)
        return (expansion1, expansion2, expansion3)
        

    def do_turn(self, move_string):
        self.move_string = move_string
        return super().do_turn()

        