from time import *
from board import Board
from exhaustive_move_possiblities import emp_dict
from gamestate import Gamestate
from gui import GUI
from human import Human
from bot import Bot
from read_in_bot import ReadInBot
from game_info import GameInfo

color_to_name = {"W": "White", "B": "Black"}

class ReadInEnvironment:
    def __init__(self, game_info, data_format):
        self.data_format = data_format
        # self.gui = GUI("Chess Game", 600, "W", 0.02)
        self.game_info = game_info
        self.result_value = game_info.result
        position_file_name = "position_csv_files/standard_setup.csv"
        exporting_file_name = "position_csv_files/recorder.csv"
        self.board = Board(position_file_name, exporting_file_name, data_format)
        self.white_player = ReadInBot("W", self.board)
        self.black_player = ReadInBot("B", self.board)
        self.players = {"W": self.white_player, "B": self.black_player}
        # self.display_board_gui()

    def replay_game(self):
        encodings = []
        encodings.append(self.board.transform())
        
        for i in range(len(self.game_info.moves)):
            move_string = self.game_info.moves[i]
            player = self.players[self.board.position.active_player]
            error = player.do_turn(move_string)
            if error == "no luck":
                break
            encodings.append(self.board.transform())
            # self.display_board_gui()

        if self.data_format == "3D Numpy":
            for encoding in encodings:
                encoding[1][7] = self.result_value
        else:
            for encoding in encodings:
                encoding.append(self.result_value)
        return encodings

    def display_board_gui(self):
        self.gui.transition_to_gamestate(self.board.get_position())
