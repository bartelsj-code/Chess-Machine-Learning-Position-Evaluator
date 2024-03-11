from time import *

from board import Board
from exhaustive_move_possiblities import emp_dict
from gamestate import Gamestate
from gui import GUI
from human import Human

color_to_name = {"W": "White", "B": "Black"}

from bot import Bot
from reading_bot import RelayBot

class Game:
    def __init__(self):
        self.gui = GUI("Chess Game", 800, "W", 0.6)
        position_file_name = "position_csv_files/standard_setup.csv"
        exporting_file_name = "position_csv_files/recorder.csv"
        self.board = Board(position_file_name, exporting_file_name)
        self.white_player = RelayBot("W", self.board, self.gui)
        self.black_player = RelayBot("B", self.board, self.gui)
        self.players = {"W": self.white_player, "B": self.black_player}
        self.display_board_gui()
            
    def play(self):
        for i in range(500):
            player = self.players[self.board.position.active_player]
            player.do_turn()
            self.display_board_gui()
            
    def display_board_gui(self):
        self.gui.transition_to_gamestate(self.board.get_position())
        

if __name__ == "__main__":
    game = Game()
    game.play()
    g = input("f")
    

