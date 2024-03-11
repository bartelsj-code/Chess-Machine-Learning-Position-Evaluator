from exhaustive_move_possiblities import emp_dict
from move import Move

class GamestateEmpty:
    def __init__(self):
        pass

    def get_copy(self):
        return GamestateEmpty()

    def __repr__(self):
        return "__"

class GamestatePiece:
    def __init__(self, color):
        self.color = color

    def get_key(self):
        return (self.piece_type, self.coords)

    def get_copy(self):
        return self.own_type(self.color)

    def __repr__(self):
        return "{}{}".format(self.color, self.piece_type)
    
    def get_color(self):
        return self.color
    
    def get_piece_type(self):
        return self.piece_type
    
    def set_coords(self, coords):
        self.coords = coords
        
    def get_moves(self):
        moves = []
        move_coords_list = emp_dict[self.piece_type][self.coords]
        for lst in move_coords_list:
            for coords in lst:
                occupant = self.gs.grid[coords[0]][coords[1]]
                if type(occupant) != GamestateEmpty and occupant.color == self.color:
                    break
                move = Move()
                move.add_component((self.coords, coords))
                moves.append(move)
                if type(occupant) != GamestateEmpty and occupant.color != self.color:
                    break
        return moves
    
class GamestatePawn(GamestatePiece):
    def __init__(self, color):
        super().__init__(color)
        self.piece_type = "P"
        self.own_type = GamestatePawn

    def get_moves(self):
        moves = []
        move_coords_list = emp_dict[self.color+self.piece_type][self.coords]
        for lst in move_coords_list:
            for coords in lst:
                occupant = self.gs.grid[coords[0]][coords[1]]
                if type(occupant) != GamestateEmpty:
                    break
                move = Move()
                move.piece_type = "P"
                move.add_component((self.coords, coords))
                moves.append(move)
        diagonals = {"W":[(1,1),(-1,1)],"B":[(1,-1),(-1,-1)]}
        for delta in diagonals[self.color]:
            coords = add_deltas(self.coords, delta)
            if coords_within_range(coords):
                occupant = self.gs.grid[coords[0]][coords[1]]
                if type(occupant) != GamestateEmpty and occupant.color != self.color:
                    move = Move()
                    move.add_component((self.coords, coords))
                    moves.append(move)
        if (self.color == "W" and self.coords[1] == 6) or (self.color == "B" and self.coords[1] == 1):
            knight = GamestateKnight(self.color)
            bishop = GamestateBishop(self.color)
            rook = GamestateRook(self.color)
            queen = GamestateQueen(self.color)
            replacements = [knight, bishop, rook, queen]
            moves3 = []
            for replacement in replacements:
                moves2 = []
                for move in moves:
                    m = move.clone()
                    m.is_promotion = True
                    m.promotion_piece = replacement
                    moves2.append(m)
                for move in moves2:
                    moves3.append(move)
            return moves3
        if self.check_for_en_passant():
            prev_move = self.gs.previous_move
            pairs = self.get_en_passant_pairs()
            if prev_move.piece_type == "P":
                if prev_move.coord_pairs[0] in pairs:
                    #add actual en passant here
                    if self.color == "W":
                        adjust = 1
                    else:
                        adjust = -1
                    d1 = prev_move.coord_pairs[0][1]
                    m = Move()
                    m.add_component((d1,(d1[0],d1[1]+adjust)))
                    m.add_component((self.coords, (d1[0],d1[1]+adjust)))
                    m.en_passant_identifier()
                    moves.append(m)
        return moves
    
    def check_for_en_passant(self):
        if self.gs.previous_move != None:  
            if ((self.color == "W" and self.coords[1] == 4) or (self.color == "B" and self.coords[1] == 3)):
                return True
        return False
    
    def get_en_passant_pairs(self):
        pairs = []
        if self.color == "W":
            adjust = 2
        else:
            adjust = -2
        for element in [-1, 1]:
            coords = add_deltas(self.coords, (element, adjust))
            coords2 = add_deltas(self.coords, (element, 0))
            if coords_within_range(coords):
                coord_pair = (coords, coords2)
                pairs.append(coord_pair)
        return pairs
    
def add_deltas(loc, delta):
    new_x = loc[0] + delta[0]
    new_y = loc[1] + delta[1]
    return (new_x, new_y)

def coords_within_range(coords):
    for coord in coords:
        if coord < 0 or coord > 7:
            return False
    return True
    
class GamestateKnight(GamestatePiece):
    def __init__(self, color):
        super().__init__(color)
        self.piece_type = "N"
        self.own_type = GamestateKnight

class GamestateBishop(GamestatePiece):
    def __init__(self, color):
        super().__init__(color)
        self.piece_type = "B"
        self.own_type = GamestateBishop

class GamestateRook(GamestatePiece):
    def __init__(self, color):
        super().__init__(color)
        self.piece_type = "R"
        self.own_type = GamestateRook

class GamestateQueen(GamestatePiece):
    def __init__(self, color):
        super().__init__(color)
        self.piece_type = "Q"
        self.own_type = GamestateQueen

class GamestateKing(GamestatePiece):
    def __init__(self, color):
        super().__init__(color)
        self.piece_type = "K"
        self.own_type = GamestateKing
