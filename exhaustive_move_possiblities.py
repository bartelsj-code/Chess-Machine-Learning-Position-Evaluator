
class EMPmaker:
    #exhaustive move possibilities
    def __init__(self):
        
        self.species_list = {EMPWpawn:"WP", EMPBpawn:"BP", EMPknight:"N", EMPbishop:"B", EMProok:"R", EMPqueen:"Q", EMPking:"K"}
        self.collection = {"WP":{},"BP":{},"N":{},"B":{},"R":{},"Q":{},"K":{}}
    
    def make_dict(self):
        for species in self.species_list:
            for x in range(8):
                for y in range(8):
                    g = species((x,y))
                    moves = g.get_moves()
                    self.collection[self.species_list[species]][(x,y)] = moves
        return self.collection

class EMPpiece:
    def __init__(self, loc_coords):
        self.coords = loc_coords

    def get_directional_moves(self):
        lst = []
        for deltas in self.deltas_list:
            g = self.follow_direction(deltas)
            if g != []:
                lst.append(g)
        return lst

    def follow_direction(self, deltas):
        coords = self.coords
        lst = []
        while True:
            coords = add_deltas(coords, deltas)
            if not coords_within_range(coords):
                break
            lst.append(coords)
        return lst

class EMPWpawn(EMPpiece):
    def __init__(self, loc_coords):
        super().__init__(loc_coords)
        self.deltas1 = (0,1)
        self.deltas2 = (0,2)

    def get_moves(self):
        lst1 = []
        lst2 = []
        if self.coords[1] < 7:
            if coords_within_range(add_deltas(self.coords, self.deltas1)):
                lst2.append(add_deltas(self.coords, self.deltas1))
                if self.coords[1] == 1:
                    if coords_within_range(add_deltas(self.coords, self.deltas2)):
                        lst2.append(add_deltas(self.coords, self.deltas2))
        if lst2 != []:
            lst1.append(lst2)
        return lst1

class EMPBpawn(EMPpiece):
    def __init__(self, loc_coords):
        super().__init__(loc_coords)
        self.deltas1 = (0,-1)
        self.deltas2 = (0,-2)

    def get_moves(self):
        lst1 = []
        lst2 = []
        if self.coords[1] > 0:
            if coords_within_range(add_deltas(self.coords, self.deltas1)):
                lst2.append(add_deltas(self.coords, self.deltas1))
                if self.coords[1] == 6:
                    if coords_within_range(add_deltas(self.coords, self.deltas2)):
                        lst2.append(add_deltas(self.coords, self.deltas2))
        if lst2 != []:
            lst1.append(lst2)
        return lst1

class EMPknight(EMPpiece):
    def __init__(self, loc_coords):
        super().__init__(loc_coords)
        self.deltas_list = [(2,-1),(2,1),(-2,-1),(-2,1),(-1,2),(1,2),(-1,-2),(1,-2)]

    def get_moves(self):
        lst1=[]
        for deltas in self.deltas_list:
            lst2 = []
            move_coords = add_deltas(self.coords, deltas)
            if coords_within_range(move_coords):
                lst2.append(move_coords)
            if lst2 != []:
                lst1.append(lst2)
        return lst1


class EMPbishop(EMPpiece):
    def __init__(self, loc_coords):
        super().__init__(loc_coords)
        self.deltas_list = [(-1,-1),(1,1),(1,-1),(-1,1)]

    def get_moves(self):
        return self.get_directional_moves()


class EMProok(EMPpiece):
    def __init__(self, loc_coords):
        super().__init__(loc_coords)
        self.deltas_list = [(-1,0),(0,1),(1,0),(0,-1)]

    def get_moves(self):
        return self.get_directional_moves()

class EMPqueen(EMPpiece):
    def __init__(self, loc_coords):
        super().__init__(loc_coords)
        self.deltas_list = [(-1,0),(0,1),(1,0),(0,-1),(-1,-1),(1,1),(1,-1),(-1,1)]

    def get_moves(self):
        return self.get_directional_moves()

class EMPking(EMPpiece):
    def __init__(self, loc_coords):
        super().__init__(loc_coords)
        self.deltas_list = [(-1,0),(0,1),(1,0),(0,-1),(-1,-1),(1,1),(1,-1),(-1,1)]

    def get_moves(self):
        lst1=[]
        for deltas in self.deltas_list:
            lst2 = []
            move_coords = add_deltas(self.coords, deltas)
            if coords_within_range(move_coords):
                lst2.append(move_coords)
            if lst2 != []:
                lst1.append(lst2)
        return lst1


def coords_within_range(coords):
    for coord in coords:
        if coord < 0 or coord > 7:
            return False
    return True

def add_deltas(loc, delta):
    new_x = loc[0] + delta[0]
    new_y = loc[1] + delta[1]
    return (new_x, new_y)

p = EMPmaker()
emp_dict = p.make_dict()