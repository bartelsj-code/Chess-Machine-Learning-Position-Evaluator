from gamestate import Gamestate
from gamestate_pieces import GamestatePawn

class Board:
    def __init__(self, file_name, export_file, transform_method):
        self.transform_type = transform_method
        self.position = gamestate_from_file(file_name)
        self.times_visited_dict = {}
        self.increase_visited()
        self.fifty_move_counter = 0
        self.history = [self.position]
        self.export_file = export_file

    def get_position(self):
        return self.position
    
    def increase_visited(self):
        if self.position in self.times_visited_dict:
            self.times_visited_dict[self.position] += 1
        else:
            self.times_visited_dict[self.position] = 1

    def times_visited(self, position):
        if position in self.times_visited_dict:
            return self.times_visited_dict[position]
        return 0
                
    def check_for_endstate(self):
        if self.times_visited(self.position) == 3:
            return "Repetition"
        if self.fifty_move_counter == 50:
            return "50 moves"
        result = self.position.check_if_terminal()
        return result
    
    def made_by_pawn(self, move):
        start_coords = move.coord_pairs[0][0]
        if type(self.position.grid[start_coords[0]][start_coords[1]]) == GamestatePawn:
            return True
        return False
    
    def update_counter(self, move):
        if self.made_by_pawn(move):
            self.fifty_move_counter = 0
        elif "x" in self.position.get_notation(move):
            self.fifty_move_counter = 0
        else:
            self.fifty_move_counter += 1

    def update_history(self):
        self.history.append(self.position)

    def transform(self):
        encoding_list = self.position.transform(self.transform_type)
        return encoding_list

    def execute_move(self, move):
        # self.update_counter(move)
        # print(self.position.get_notation(move))
        self.position = self.position.clone_with_move(move)
        # self.increase_visited()
        # self.update_history()
        # self.export_to_file()

    def export_to_file(self):
        self.position.export_to_file(self.export_file)

        
            
def gamestate_from_file(position_file):
    gs = Gamestate()
    gs.read_in_from_file(position_file)
    return gs
        