from time import *

from board import Board
from exhaustive_move_possiblities import emp_dict
from gamestate import Gamestate
from gui import GUI
from human import Human

color_to_name = {"W": "White", "B": "Black"}

from bot import Bot


class Game:
    def __init__(self):
        self.is_game_over = False
        self.gui = GUI("Chess Game", 800, "W", 0.6)
        position_file_name = "position_csv_files/standard_setup.csv"
        # position_file_name = "position_csv_files/test_position.csv"
        # position_file_name = "position_csv_files/endgame_depth_test.csv"
        # position_file_name = "position_csv_files/morphy_zugszwang_mate_in 3.csv"
        # position_file_name = "position_csv_files/an_test.csv"
        exporting_file_name = "position_csv_files/recorder.csv"
        self.board = Board(position_file_name, exporting_file_name)
        self.white_player = Human("W", self.board, self.gui)
        self.black_player = Human("B", self.board, self.gui)
        self.players = {"W": self.white_player, "B": self.black_player}
        self.display_board_gui()

    def turn_end_checks(self, player):
        result = self.board.check_for_endstate()
        if result != None:
            if result == "Checkmate":
                string = "{} wins by Checkmate".format(color_to_name[player.color])
            elif result == "Stalemate":
                string = "Draw by Stalemate"
            elif result == "Repetition":
                string = "Draw by Repetition"
            elif result == "50 Moves":
                string = "Draw by 50 Move Rule"
            elif result == "Insufficient Material":
                string = "Draw by Insufficient Material"
            self.gui.change_title(string)
            print(string)
            self.is_game_over = True
            

    def play(self):
        for i in range(500):
            player = self.players[self.board.position.active_player]
            player.do_turn()
            self.display_board_gui()
            self.turn_end_checks(player)
            if self.is_game_over:
                break
            
    def display_board_gui(self):
        self.gui.transition_to_gamestate(self.board.get_position())
        

if __name__ == "__main__":
    game = Game()
    game.play()
    g = input("f")
    

