class GameInfo:
    def __init__(self, moves_string, result_string) -> None:
        self.moves = self.make_list(moves_string)
        self.result = self.convert_result(result_string)
        

    def make_list(self, move_string):
        move_string = move_string.strip()
        move_list = move_string.split(" ")
        return move_list
    
    def convert_result(self, result_string):
        result_string = result_string.strip()
        if result_string == "1-0":
            return 1
        if result_string == "0-1":
            return -1
        if result_string == "1/2-1/2":
            return 0
        else:
            print("incorrect result format: {}".format(result_string))
        
