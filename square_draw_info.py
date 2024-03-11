class SquareDrawInfo:
    def __init__(self, color, text_color, highlight_color, size, location, window):
        self.color = color
        self.text_color = text_color
        self.highlight_color = highlight_color
        self.size = size
        self.location = location
        self.win = window

    def get_location(self):
        return self.location
    
    def get_size(self):
        return self.size
    
    def get_color(self):
        return self.color

    def get_win(self):
        return self.win

    def get_text_color(self):
        return self.text_color

    def get_highlight_color(self):
        return self.highlight_color