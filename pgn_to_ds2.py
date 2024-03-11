import os
from game_info import GameInfo
from read_in_environment import ReadInEnvironment
import csv
import numpy as np
import re
from time import perf_counter

game_results = ["1-0", "0-1", "1/2-1/2", "*"]

class Converter:
    def __init__(self, pgn_folder_name, output_file_name) -> None:
        
        self.output_folder_name = output_file_name
        self.pgn_folder_name = pgn_folder_name
        os.chdir(pgn_folder_name)
        self.pgn_file_names = os.listdir()
        os.chdir('..')

    def convert(self):
        self.prepare_pgns()
        game_infos = self.make_game_infos()
        encodings = self.get_encodings(game_infos)
        positions, metadata = self.split(encodings)
        self.write_to_file(positions, metadata)

    def split(self, encodings):
        positions = np.array([encoding[0] for encoding in encodings])
        metadata = np.array([encoding[1] for encoding in encodings])
        return positions, metadata
            
    def write_to_file(self, positions, metadata):
        try:
            os.mkdir(self.output_folder_name)
        except:
            pass
        os.chdir(self.output_folder_name)
        np.save("positions.npy", positions)
        np.save("metadata.npy", metadata)
        os.chdir("..")
        print("done")

    def time_remaining_string(self, current_reps, total_reps):
        
        current_time = perf_counter()
        time_spent = current_time-self.start_time
        estimated_total_time = (time_spent * total_reps)/current_reps
        remaining_estimate = estimated_total_time-time_spent
        hours = int(remaining_estimate // 3600)
        mins = int(remaining_estimate // 60 - 60 * hours)
        secs = int(remaining_estimate//1 - (60 * mins) - (3600 * hours))
        mins = self.add_zero(mins)
        secs = self.add_zero(secs)
        ou = "{}:{}:{}".format(hours, mins, secs)
        return ou
        
    def add_zero(self, val):
        val = str(val)
        if len(val) < 2:
            val = "0" + val
        return val
    

    def get_encodings(self, game_infos):
        self.start_time = perf_counter()
        all_encodings = []
        start_i = 0
        # game_infos = game_infos[0:-300]
        for i in range(start_i, len(game_infos)):
            game_info = game_infos[i]
            env = ReadInEnvironment(game_info, data_format="3D Numpy")
            game_encodings = env.replay_game()
            all_encodings += game_encodings
            print("game {}/{}     {} positions     ETC: {}".format(i+1, len(game_infos), len(all_encodings), self.time_remaining_string(i+1, len(game_infos))))

        return all_encodings

    def make_game_infos(self):
        os.chdir("prepared_files")
        paths = ["prepared_files/"+name for name in os.listdir()]
        os.chdir("..")
        game_infos = []
        for path in paths:
            f = open(path, "r")
            lines = f.readlines()
            f.close()
            for i in range(0, len(lines), 3):
                moves_string = lines[i]
                result_string = lines[i+1]
                g = GameInfo(moves_string, result_string)
                if len(moves_string) < 5:
                    
                    pass
                elif "*" in result_string:
                    print("result removed")
                    pass
                else:
                    game_infos.append(g)
        return game_infos

    def prepare_pgns(self):
        cleans = []
        for pgn_file_name in self.pgn_file_names:
            path = self.pgn_folder_name+"/"+pgn_file_name
            file = open(path, "r")
            curr = file.read()
            file.close()
            temp = re.sub("[\[].*?[\]]", "", curr)
            temp = re.sub("[0-9]([0-9]+\.|\.)", "", temp)
            split_temp = temp.split()
            for i in range(len(split_temp)):
                if split_temp[i] in game_results:
                    split_temp[i] = "\n" + split_temp[i] + "\n" + "\n"
            temp = ' '.join(split_temp)
            cleans.append(temp)

        try:
            os.mkdir("prepared_files")
        except:
            pass

        
        os.chdir("prepared_files")
        for filename in os.listdir():
            os.remove(filename)
        i = 0
        for pgn_file_name in self.pgn_file_names:
            file = open(pgn_file_name.split(".")[0] + ".txt", "w")
            file.write(cleans[i])
            i += 1
        os.chdir("..")

if __name__ == "__main__":
    c = Converter("pgn_files", "3D Numpy Data")
    c.convert()