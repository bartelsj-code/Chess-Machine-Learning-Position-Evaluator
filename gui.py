from graphics import *
from gui_square import GUISquare
from square_draw_info import SquareDrawInfo
from gamestate import Gamestate
from gui_bishop import GUIBishop
from gui_rook import GUIRook
from gui_pawn import GUIPawn
from gui_queen import GUIQueen
from gui_king import GUIKing
from gui_knight import GUIKnight
from psw import PSW
from gui_empty import GUIEmpty
from time import sleep,perf_counter
from math import floor

class GUI:
    def __init__(self, name, length, view, animation_time):
        self.animation_time = animation_time
        self.fps = 60
        self.view = view
        self.length = length
        self.border_in_squares = 0.7
        self.background_color = color_rgb(30,30,100)
        self.square_length = self.length/(2*self.border_in_squares + 8)
        self.border_width = self.square_length*self.border_in_squares
        self.set_colors()
        self.make_window(name)
        self.squares_list = self.make_squares()
        self.spaces_list = empty_grid()
        self.class_type_dict = {"B": GUIBishop, "R": GUIRook, "P": GUIPawn, "Q": GUIQueen, "K": GUIKing, "N": GUIKnight}

    def make_window(self, name):
        #creates window
        self.win = GraphWin(name, self.length, self.length)
        self.win.setBackground(self.background_color)

    def change_title(self, new_title):
        self.win.changeTitle(new_title)

    def get_square_from_click(self):
        while True:
            point = self.win.getMouse()
            x = point.getX()
            y = point.getY()
            pair = self.get_square_coords_from_coords(x,y)
            if pair[0] <= 7 and pair[0] >= 0 and pair[1] <= 7 and pair[1] >= 0:
                return pair

    def get_square_coords_from_coords(self, x, y):
        sl = self.square_length
        b = self.border_in_squares * self.square_length
        if self.view == "W":
            return (floor((x-b)/sl),7-floor((y-b)/sl))
        else:
            return (7-floor((x-b)/sl),floor((y-b)/sl))


    def set_colors(self):
        #colors for graphic square objects
        self.light_square_color = color_rgb(180,180,180)
        self.light_square_text_color = color_rgb(55,35,35)
        self.light_square_highlight_color = color_rgb(212,212,160) 
        self.dark_square_color = color_rgb(55,35,35)
        self.dark_square_text_color = color_rgb(180,180,180)
        self.dark_square_highlight_color = color_rgb(80,56,30)

    def make_squares(self):
        #creates graphic square objects and adds them to squares list
        names_list = make_names_list()
        squares = empty_grid()
        c = 0
        c2 = 1
        for i in range(8):
            for j in range(8):
                name = names_list[c]
                if c2 % 2 == 0:
                    #square is dark
                    color = self.dark_square_color
                    highlight_color = self.dark_square_highlight_color
                    text_color = self.dark_square_text_color
                else:
                    #square is light
                    color = self.light_square_color
                    highlight_color = self.light_square_highlight_color
                    text_color = self.light_square_text_color
                if self.view == "W":
                    #adjust x/y coords depending on view
                    x = j * self.square_length + self.border_width
                    y = i * self.square_length + self.border_width
                else:
                    window_length = 2*self.border_width + 8*self.square_length
                    x = window_length-(j * self.square_length + self.border_width + self.square_length)
                    y = window_length-(i * self.square_length + self.border_width + self.square_length)
                square_draw_info = SquareDrawInfo(color, text_color, highlight_color, self.square_length, (x,y), self.win)
                square = GUISquare(name, (i,j), square_draw_info)
                square.draw()
                squares[j][7-i] = square
                c += 1
                c2 += 1
            c2 += 1
        return squares
    
    def transition_to_gamestate(self, gamestate):
        self.current_gamestate = gamestate
        gamestate_differences, gui_differences = self.get_differences(gamestate)
        to_delete, to_animate, to_create = self.sort_differences(gamestate_differences, gui_differences)
        self.delete_pieces(to_delete)
        self.create_pieces(to_create)
        self.animate(to_animate)


    def animate(self, to_animate):
        frame_count = round(0.5+( self.fps * self.animation_time))
        frame_time = self.animation_time/self.fps
        for piece in to_animate:
            dsc = piece.destination_square_coords
            piece.set_end_square(self.squares_list[dsc[0]][dsc[1]])
            piece.set_deltas(frame_count)

        for i in range(frame_count):
            p1 = perf_counter()
            for piece in to_animate:
                deltas = piece.deltas[i]
                piece.move(deltas)
            p2 = perf_counter()
            wait_time = max(0, frame_time - (p2-p1))
            sleep(wait_time)

        for piece in to_animate:
            old_coords = piece.coords
            if self.spaces_list[old_coords[0]][old_coords[1]] == piece:
                self.spaces_list[old_coords[0]][old_coords[1]] = GUIEmpty()
            new_coords = piece.destination_square_coords
            self.spaces_list[new_coords[0]][new_coords[1]] = piece
            piece.update_info()

    def create_pieces(self, to_create):
        for piece in to_create:
            str = repr(piece)
            coords = piece.coords
            square = self.squares_list[coords[0]][coords[1]]
            new_gui_piece = self.class_type_dict[str[1]](str[0], square, self.win)
            self.spaces_list[coords[0]][coords[1]] = new_gui_piece
            new_gui_piece.draw()

    def delete_pieces(self, to_delete):
        for piece in to_delete:
            coords = piece.coords
            self.spaces_list[coords[0]][coords[1]] = GUIEmpty()
            piece.undraw()

    def sort_differences(self, gs_differences, gui_differences):
        to_delete = []
        to_animate = []
        to_create = []
        to_be_removed_gs = []
        for piece in gs_differences:
            string = repr(piece)
            to_be_removed_gui = []
            for potential_match in gui_differences:
                pm_string = repr(potential_match)
                if string == pm_string:
                    potential_match.set_destination_square_coords(piece.coords)
                    to_animate.append(potential_match)
                    to_be_removed_gs.append(piece)
                    to_be_removed_gui.append(potential_match)
                    break
            for match in to_be_removed_gui:
                gui_differences.remove(match)
        for piece in to_be_removed_gs:
            gs_differences.remove(piece)
        to_create = gs_differences
        to_delete = gui_differences
        return to_delete, to_animate, to_create

    def get_differences(self, gamestate):
        gamestate_differences = []
        gui_differences = []
        for y in range(8):
            for x in range(8):
                gs_piece = gamestate.grid[x][y]
                gui_piece = self.spaces_list[x][y]
                if repr(gs_piece) != repr(gui_piece):
                    if repr(gs_piece) != "__":
                        gamestate_differences.append(gs_piece)
                    if repr(gui_piece) != "__":
                        gui_piece.set_coords((x,y))
                        gui_differences.append(gui_piece)
        return gamestate_differences, gui_differences
   
    def quick_draw_gamestate(self, gamestate):
        self.current_gamestate = gamestate
        self.spaces_list = empty_grid()
        for x in range(8):
            for y in range(8):
                piece_string = repr(gamestate.grid[x][y])
                if piece_string != "__":
                    class_type = self.class_type_dict[piece_string[1]]
                    gui_piece = class_type(piece_string[0], self.squares_list[x][y], self.win)
                    self.spaces_list[x][y] = gui_piece
                    gui_piece.draw()

    def __repr__(self):
        string = ""
        row = ""
        for y in range(7, -1, -1):
            for x in range(8):
                piece = self.spaces_list[x][y]
                if piece == None:
                    content = "__"
                else:
                    content = repr(piece)
                row += content + ","
            row += "\n"
            string += row
            row = ""
        return string
    
    def get_user_promotion_choice(self):
        psw = PSW(self.current_gamestate.active_player, self.background_color)
        psw.fill()
        type = psw.get_type()
        psw.close()
        return type
    


def make_names_list():
    #generate names for squares on board
    lst = []
    letters = ['a','b','c','d','e','f','g','h']
    for i in range(8,0,-1):
        for j in range(8):
            letter = letters[j]
            number = str(i)
            name = letter + number
            lst.append(name)
    return lst


def empty_grid():
    grid = []
    for i in range(8):
        row = []
        for j in range(8):
            row.append(GUIEmpty())
        grid.append(row)
    return grid

