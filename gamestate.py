from gamestate_pieces import *
from exhaustive_move_possiblities import emp_dict
from move import Move
import csv
import numpy as np

piece_type_dict = {"P": GamestatePawn, "N": GamestateKnight, "B": GamestateBishop, "R": GamestateRook, "K":GamestateKing, "Q": GamestateQueen}

class Gamestate:
    def __init__(self):
        self.piece_collections = {"all": [],"W": [],"B": [], "WK" : None, "BK": None}
        self.grid = empty_grid()
        self.moved_pieces_dict = {(4,0):self.wkm  ,  (0,0):self.warm  ,  (7,0):self.whrm  ,  (4,7):self.bkm  ,  (0,7):self.barm  ,  (7,7):self.bhrm}
        self.hashing_key = None
        self.possible_moves_calculated = False

    ########################  Gamestate Data  #######################
    '''Data about which pieces have moved, who's turn it is, and what the last move was'''

    def set_data(self, prev_move, active_player, wkm, warm, whrm, bkm, barm, bhrm):
        self.previous_move = prev_move
        self.active_player = active_player
        self.inactive_player = get_opp(active_player)
        self.white_king_moved = wkm
        self.white_A_rook_moved = warm
        self.white_H_rook_moved = whrm
        self.black_king_moved = bkm
        self.black_A_rook_moved = barm
        self.black_H_rook_moved = bhrm

    def wkm(self):
        self.white_king_moved = True

    def bkm(self):
        self.black_king_moved = True

    def warm(self):
        self.white_A_rook_moved = True

    def whrm(self):
        self.white_H_rook_moved = True

    def barm(self):
        self.black_A_rook_moved = True

    def bhrm(self):
        self.black_H_rook_moved = True

    ############################  Move Collection  ##########################
    '''finds the set of moves that can be made from the gamestate'''

    def get_possible_moves(self):
        if not self.possible_moves_calculated:
            moves = self.get_possible_moves_for_color(self.active_player)
            self.possible_moves = self.get_legal_moves(moves)
            self.possible_moves_calculated
        return self.possible_moves
        
    def get_possible_moves_for_color(self, color):
        possible_moves = []
        pieces = self.piece_collections[color]
        for piece in pieces:
            piece_moves = piece.get_moves()
            for move in piece_moves:
                possible_moves.append(move)
        castles = self.find_castles(color)
        for castle in castles:
            possible_moves.append(castle)
        return possible_moves
    
    #############################  Castles  ##############################
    '''Castles rely on a plethora of conditions so they are created separately here'''
    
    def find_castles(self, color):
        #tries to create two move objects for the castling moves
        castles = []
        if color == "W":
            data_list = [0, self.white_king_moved, self.white_A_rook_moved, self.white_H_rook_moved]
        else:
            data_list = [7, self.black_king_moved, self.black_A_rook_moved, self.black_H_rook_moved]
        if data_list[1] == False:
            if self.can_long_castle(data_list, color):
                m = Move()
                m.add_component(((4,data_list[0]),(2,data_list[0])))
                m.add_component(((0,data_list[0]),(3,data_list[0])))
                m.castle_identifier()
                castles.append(m)
            if self.can_short_castle(data_list, color):
                m = Move()
                m.add_component(((4,data_list[0]),(6,data_list[0])))
                m.add_component(((7,data_list[0]),(5,data_list[0])))
                m.castle_identifier()
                castles.append(m)
        return castles

    def can_long_castle(self, data_list, color):
        # checks if long castle is legal
        if data_list[2]:
            return False
        king_square = (4, data_list[0])
        square2 = (3, data_list[0])
        square3 = (2, data_list[0])
        square4 = (1, data_list[0])
        threat_squares = [king_square, square2, square3]
        vacancy_squares = [square2, square3, square4]
        for square in threat_squares:
            if self.coords_threatened(square, color):
                return False
        for square in vacancy_squares:
            if type(self.grid[square[0]][square[1]]) != GamestateEmpty:
                return False
        return True
    
    def can_short_castle(self, data_list, color):
        # checks if short castle is legal
        if data_list[3]:
            return False
        king_square = (4, data_list[0])
        square2 = (5, data_list[0])
        square3 = (6, data_list[0])
        threat_squares = [king_square, square2, square3]
        vacancy_squares = [square2, square3]
        for square in threat_squares:
            if self.coords_threatened(square, color):
                return False
        for square in vacancy_squares:
            if type(self.grid[square[0]][square[1]]) != GamestateEmpty:
                return False
        return True
    
    #########################  Illegal Move Removal #######################
    '''Goes through all possible moves and removes those that leave the king in check'''

    def get_legal_moves(self, moves):
        #add optimization later
        legal_moves = []
        for move in moves:
            g = self.clone_with_move(move)
            if g.is_in_check(g.inactive_player):
                pass
            else:
                legal_moves.append(move)
        return legal_moves

    #######################  Check Detection  ########################
    '''Checking if player is in check'''

    def is_in_check(self, color):
        if color == self.active_player:
            return self.is_in_check_active()
        else:
            return self.is_in_check_inactive()

    def is_in_check_active(self):
        key = self.active_player + "K"
        king = self.piece_collections[key]
        if self.previous_move == None:
            return self.coords_threatened(king.coords, self.active_player)
        self.was_previous_move_check()
        return self.coords_threatened(king.coords, self.active_player)
    
    def was_previous_move_check(self):
        prev = self.previous_move
        end_coords = prev.coord_pairs[-1][1]
        piece_moved = self.piece_at_coords(end_coords)


    def is_in_check_inactive(self):
        key = self.inactive_player + "K"
        king = self.piece_collections[key]
        if self.previous_move == None:
            return self.coords_threatened(king.coords, self.inactive_player)
        return self.coords_threatened(king.coords, self.inactive_player)

    #########################  Terminal  State  Detection  ####################
    '''tests for game-ending positions (does not check for repetiton or 50 move draws)'''

    def check_if_terminal(self):
        if len(self.get_possible_moves()) == 0:
            if self.is_in_check(self.active_player):
                return "Checkmate"
            return "Stalemate"
        # do insufficient material check here
        return None
    
    ##########################  Threat Detection  ########################
    '''Gamestate needs to check whether a square is "under fire"'''
    
    def coords_threatened(self, coords, color):
        threat_color = get_opp(color)
        if self.check_for_knight_threat(coords, threat_color):
            return True
        if self.check_for_diagonal_threat(coords, threat_color):
            return True
        if self.check_for_orthogonal_threat(coords, threat_color):
            return True
        if self.check_for_king_threat(coords, threat_color):
            return True
        if self.check_for_pawn_threat(coords, threat_color):
            return True
        return False

    def check_for_diagonal_threat(self, coords, threat_color):
        threat_coords = emp_dict["B"][coords]
        for coords_list in threat_coords:
            for coords in coords_list:
                occupant = self.grid[coords[0]][coords[1]]
                if type(occupant) != GamestateEmpty:
                    if occupant.color == threat_color:
                        species = type(occupant)
                        if species == GamestateBishop or species == GamestateQueen:
                            return True
                    break
        return False
    
    def check_for_orthogonal_threat(self, coords, threat_color):
        threat_coords = emp_dict["R"][coords]
        for coords_list in threat_coords:
            for coords in coords_list:
                occupant = self.grid[coords[0]][coords[1]]
                if type(occupant) != GamestateEmpty:
                    if occupant.color == threat_color:
                        species = type(occupant)
                        if species == GamestateRook or species == GamestateQueen:
                            return True
                    break
        return False

    def check_for_knight_threat(self, coords, threat_color):
        threat_coords = emp_dict["N"][coords]
        for tc in threat_coords:
            tc = tc[0]
            occupant = self.grid[tc[0]][tc[1]]
            if type(occupant) == GamestateKnight:
                if occupant.color == threat_color:
                    return True
        return False
    
    def check_for_king_threat(self, coords, threat_color):
        threat_coords = emp_dict["K"][coords]
        for tc in threat_coords:
            tc = tc[0]
            occupant = self.grid[tc[0]][tc[1]]
            if type(occupant) == GamestateKing:
                if occupant.color == threat_color:
                    return True
                    
        return False
    
    def check_for_pawn_threat(self, coords, threat_color):
        if threat_color == "W":
            delta_list = [(-1, -1), (1, -1)]
        else:
            delta_list = [(-1, 1), (1, 1)]
        threat_coords = []
        for delta in delta_list:
            real_coord = add_deltas(coords, delta)
            if coords_within_range(real_coord):
                threat_coords.append(real_coord)
        for tc in threat_coords:
            occupant = self.grid[tc[0]][tc[1]]
            if type(occupant) == GamestatePawn:
                if occupant.color == threat_color:
                    return True
        return False

    ############################## Cloning ###############################
    '''Allows a gamestate to make copies of itself and children based on moves'''

    def categorize(self, piece):
        self.piece_collections["all"].append(piece)
        self.piece_collections[piece.color].append(piece)
        if type(piece) == GamestateKing:
            self.piece_collections[repr(piece)] = piece

    def position_clone(self):
        new_gs = Gamestate()
        for y in range(8):
            for x in range(8):
                piece = self.grid[x][y].get_copy()
                piece.coords = (x,y)
                piece.gs = new_gs
                new_gs.grid[x][y] = piece
        return new_gs
    
    def perfect_clone(self):
        new_gs = self.position_clone()
        new_gs.create_collections()
        new_gs.set_data(self.previous_move,\
                        self.active_player,\
                        self.white_king_moved,\
                        self.white_A_rook_moved,\
                        self.white_H_rook_moved,\
                        self.black_king_moved,\
                        self.black_A_rook_moved,\
                        self.black_H_rook_moved)
        return new_gs

    def clone_with_move(self, move):
        new_gs = self.position_clone()
        new_gs.set_data(move,\
                        self.inactive_player,\
                        self.white_king_moved,\
                        self.white_A_rook_moved,\
                        self.white_H_rook_moved,\
                        self.black_king_moved,\
                        self.black_A_rook_moved,\
                        self.black_H_rook_moved)
        new_gs.adjust_for_move(move)
        new_gs.create_collections()
        return new_gs

    def adjust_for_move(self, move):
        coord_pairs = move.coord_pairs
        for pair in coord_pairs:
            sx = pair[0][0]
            sy = pair[0][1]
            dx = pair[1][0]
            dy = pair[1][1]
            self.grid[dx][dy] = self.grid[sx][sy]
            self.grid[sx][sy] = GamestateEmpty()
            if move.is_promotion:
                self.grid[dx][dy] = move.promotion_piece
            self.grid[dx][dy].coords = (dx, dy)
            self.adjust_data_after_pair(pair)

    def create_collections(self):
        for x in range(8):
            for y in range(8):
                piece = self.grid[x][y]
                if type(piece) != GamestateEmpty:
                    self.categorize(piece)

    def adjust_data_after_pair(self, coord_pair):
        if coord_pair[0] in self.moved_pieces_dict:
            self.moved_pieces_dict[coord_pair[0]]()

    ##############################    Move Notation    ################################
    '''takes a move (from this position) and puts it into algebraic notation'''
    
    def get_notation(self, move):
        output = ""
        if len(move.coord_pairs) == 1:
            piece1 = self.piece_at_coords(move.coord_pairs[0][0])
            piece2 = self.piece_at_coords(move.coord_pairs[0][1])
            species = piece1.piece_type
            if species != "P":
                output += species
                if type(piece2) != GamestateEmpty:
                    output += "x"
            elif type(piece2) != GamestateEmpty:
                output += self.name_at_coords(move.coord_pairs[0][0])[0] + "x"
            square_name = self.name_at_coords(move.coord_pairs[0][1])
            output += square_name
            if move.is_promotion:
                output+= "={}".format(repr(move.promotion_piece)[1])
        else:
            if move.is_castle:
                if move.coord_pairs[0][1][0] == 6:
                    output = "O-O"
                else:
                    output = "O-O-O"
            else:
                output += self.name_at_coords(move.coord_pairs[1][0])[0]+"x"
                output += self.name_at_coords(move.coord_pairs[1][1])
        g = self.clone_with_move(move)
        if g.is_in_check(g.active_player):
            if len(g.get_possible_moves()) == 0:
                output += "#"
            else:
                output += "+"
        return output
                
    #########################  Hashing  ##########################
    '''So that gamestate repetition can be easily noticed, two distinct gamestates representing the same position hash to the same value'''

    def __hash__(self):
        if self.hashing_key == None:
            self.make_hashing_key()
        return hash(self.hashing_key)
        
    def __eq__(self, gamestate):
        gamestate.make_hashing_key()
        if gamestate.hashing_key == self.hashing_key:
            return True
        return False

    def make_hashing_key(self):
        if self.hashing_key == None:
            lst = []
            lst.append(self.active_player)
            for piece in self.piece_collections["W"]:
                lst.append(piece.get_key())
            lst.append(0)
            for piece in self.piece_collections["B"]:
                lst.append(piece.get_key())
            key = tuple(lst)
            self.hashing_key = key

    ########################  Importing from File  #######################
    '''Sets up a gamestate in accordance with a CSV file storing a position'''

    def read_in_from_file(self, position_file):
        with open(position_file, 'r') as source_file:
            basic_grid = csv.reader(source_file)
            source_list = []
            for row in basic_grid:
                if len(row) == 8:
                    source_list.append(row)
                else:
                    source_list.append(row[0:8])
                    gamestate_data = row[8:]
            self.import_data(gamestate_data)
            self.make_pieces(source_list)

        source_file.close()
        self.create_collections()

    def import_data(self, gamestate_data):
        self.previous_move = None
        self.active_player = gamestate_data[0]
        self.inactive_player = get_opp(self.active_player)
        self.white_king_moved = (gamestate_data[1] == "1")
        self.white_A_rook_moved = (gamestate_data[2] == "1")
        self.white_H_rook_moved = (gamestate_data[3] == "1")
        self.black_king_moved = (gamestate_data[4] == "1")
        self.black_A_rook_moved = (gamestate_data[5] == "1")
        self.black_H_rook_moved = (gamestate_data[6] == "1")

    def make_pieces(self, source_list):
        for y in range(8):
            for x in range(8):
                shorthand = source_list[y][x]
                if shorthand != '__':
                    color = shorthand[0]
                    type = shorthand[1]
                    piece = piece_type_dict[type](color)
                    piece.coords = (x, 7-y)
                    self.grid[x][7-y] = piece

    ########################  Exporting to CSV File  #######################
    '''Exports to a csv file'''

    def export_to_file(self, file_name):
        with open(file_name, 'w', newline = "") as destination_file:
            writer = csv.writer(destination_file, delimiter=',')
            for y in range(8):
                row = []
                for x in range(8):
                    shorthand = repr(self.grid[x][7-y])
                    row.append(shorthand)
                if y == 7:
                    row += self.gamestate_data_lst()
                writer.writerow(row)
        destination_file.close()

    def gamestate_data_lst(self):
        lst = []
        lst.append(self.active_player)
        lst.append(bool_to_int(self.white_king_moved))
        lst.append(bool_to_int(self.white_A_rook_moved))
        lst.append(bool_to_int(self.white_H_rook_moved))
        lst.append(bool_to_int(self.black_king_moved))
        lst.append(bool_to_int(self.black_A_rook_moved))
        lst.append(bool_to_int(self.black_H_rook_moved))
        return lst
    
    ##################  Make Training Representation  #################
    '''transforms position into row of booleans'''

    def transform(self, type):
        if type == "linear_bool":
            return self.transform_1()
        if type == "3D Numpy":
            return self.transform_2()
    
    def transform_1(self):
        '''Linear Boolean'''
        #[ 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        #[WP,WN,WB,WR,WQ,WK,BP,BN,BB,BR,BQ,BK]
        empty_encoding = [0,0,0,0,0,0,0,0,0,0,0,0]
        encoding_list = []
        formatting_dict = {"WP":0,"WN":1,"WB":2,"WR":3,"WQ":4,"WK":5,"BP":6,"BN":7,"BB":8,"BR":9,"BQ":10,"BK":11}
        position_list = []
        for i in range(8):
            position_list += self.grid[i]
        for occupant in position_list:
            if type(occupant) == GamestateEmpty:
                encoding_list+=empty_encoding
            else:
                current_encoding = empty_encoding[:]
                current_encoding[formatting_dict[repr(occupant)]] = 1
                encoding_list+=current_encoding
        active_int = 1
        if self.active_player == "B":
            active_int = 0
        encoding_list.append(active_int)
        encoding_list.append(bool_to_int(self.white_king_moved))
        encoding_list.append(bool_to_int(self.white_A_rook_moved))
        encoding_list.append(bool_to_int(self.white_H_rook_moved))
        encoding_list.append(bool_to_int(self.black_king_moved))
        encoding_list.append(bool_to_int(self.black_A_rook_moved))
        encoding_list.append(bool_to_int(self.black_H_rook_moved))
        return encoding_list

    def transform_2(self):
        '''3D Numpy'''
        #[ 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        #[WP,WN,WB,WR,WQ,WK,BP,BN,BB,BR,BQ,BK]
        position_array = np.zeros((8,8,12))
        
        formatting_dict = {"WP":0,"WN":1,"WB":2,"WR":3,"WQ":4,"WK":5,"BP":6,"BN":7,"BB":8,"BR":9,"BQ":10,"BK":11}
        for x in range(8):
            for y in range(8):
                occupant = self.grid[x][y]
                if type(occupant) != GamestateEmpty:
                    position_array[x][y][formatting_dict[repr(occupant)]] = 1

        tlst = []
        active_int = 1
        if self.active_player == "B":
            active_int = 0
        tlst.append(active_int)
        tlst.append(bool_to_int(self.white_king_moved))
        tlst.append(bool_to_int(self.white_A_rook_moved))
        tlst.append(bool_to_int(self.white_H_rook_moved))
        tlst.append(bool_to_int(self.black_king_moved))
        tlst.append(bool_to_int(self.black_A_rook_moved))
        tlst.append(bool_to_int(self.black_H_rook_moved))
        tlst.append(0)
        extra_data = np.array(tlst)
        
        return position_array, extra_data











    
    ###############################  Misc  ##############################

    def piece_at_coords(self, coords):
        return self.grid[coords[0]][coords[1]]
    
    def name_at_coords(self, coords):
        letters = ["a", "b", "c", "d", "e", "f", "g", "h"]
        return letters[coords[0]] + str(coords[1]+1)
    
    def __repr__(self):
        # return str(hash(self))
        return self.get_output_string()

    def get_output_string(self):
        string = ""
        row = ""
        for y in range(7, -1, -1):
            for x in range(8):
                piece = self.grid[x][y]
                if piece == None:
                    content = "__"
                else:
                    content = repr(piece)
                row += content + ","
            if y > 0:
                row += "\n"
            string += row
            row = ""
        string += "{},{},{},{},{},{},{}".format(self.active_player,\
                                    bool_to_int(self.white_king_moved),\
                                    bool_to_int(self.white_A_rook_moved),\
                                    bool_to_int(self.white_H_rook_moved),\
                                    bool_to_int(self.black_king_moved),\
                                    bool_to_int(self.black_A_rook_moved),\
                                    bool_to_int(self.black_H_rook_moved))
        
        return string
    
#############################  Helper Functions for Gamestate #########################
    
def get_opp(active):
    if active == "W":
        return "B"
    else:
        return "W"

def bool_to_int(bool):
    if bool:
        return 1
    else:
        return 0

def empty_grid():
    grid = []
    for i in range(8):
        row = []
        for j in range(8):
            row.append(GamestateEmpty())
        grid.append(row)
    return grid

def add_deltas(loc, delta):
    new_x = loc[0] + delta[0]
    new_y = loc[1] + delta[1]
    return (new_x, new_y)

def coords_within_range(coords):
    for coord in coords:
        if coord < 0 or coord > 7:
            return False
    return True