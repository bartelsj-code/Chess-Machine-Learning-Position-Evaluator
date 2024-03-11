class Move:
    def __init__(self):
        self.coord_pairs = []
        self.is_promotion = False
        self.is_castle = False
        self.piece_type = None
        self.notation = ""

    def add_component(self, pair):
        self.coord_pairs.append(pair)
        self.set_identifier_pair()
    
    def clone(self):
        m = Move()
        m.coord_pairs = self.coord_pairs
        m.identifier_pair = self.identifier_pair
        m.is_promotion = self.is_promotion
        return m

    def set_promotion(self):
        self.is_promotion == True

    def en_passant_identifier(self):
        self.identifier_pair = (self.coord_pairs[1][0],self.coord_pairs[1][1])

    def castle_identifier(self):
        self.identifier_pair = self.coord_pairs[0]
        self.is_castle = True

    def set_identifier_pair(self):
        #if not a castle or a peasant, is just the main coord_pair.
        if len(self.coord_pairs) == 1:
            self.identifier_pair = self.coord_pairs[0]
