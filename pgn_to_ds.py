import os
from game_info import GameInfo
from read_in_environment import ReadInEnvironment
import csv


class Converter:
    def __init__(self, pgn_folder_name, output_file_name) -> None:
        self.output_file_name = output_file_name
        self.pgn_folder_name = pgn_folder_name
        os.chdir(pgn_folder_name)
        self.pgn_file_names = os.listdir()
        os.chdir('..')

    def convert(self):
        self.prepare_pgns()
        game_infos = self.make_game_infos()
        encodings = self.get_encodings(game_infos)
        self.write_to_csv(encodings)
    
    def write_to_csv(self, encodings):
        file = open(self.output_file_name, 'w', newline='')
        writer = csv.writer(file)
        for encoding in encodings:
            writer.writerow(encoding)
        file.close()
        print("done")






    def get_encodings(self, game_infos):
        all_encodings = []
        for i in range(0, len(game_infos)):
            game_info = game_infos[i]
            print("game {}/{}      {} positions encoded".format(i+1, len(game_infos), len(all_encodings)))
            env = ReadInEnvironment(game_info, data_format="linear_bool")
            game_encodings = env.replay_game()
            all_encodings += game_encodings
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
                game_infos.append(g)
        return game_infos

    def prepare_pgns(self):
        cleans = []
        for pgn_file_name in self.pgn_file_names:
            path = self.pgn_folder_name+"/"+pgn_file_name
            file = open(path, "r")
            cleaned = self.clean_pgn(file)
            cleans.append(cleaned)
            file.close()
        try:
            os.mkdir("prepared_files")
        except:
            pass
        os.chdir("prepared_files")
        i = 0
        for pgn_file_name in self.pgn_file_names:
            file = open(pgn_file_name.split(".")[0] + ".txt", "w")
            file.write(cleans[i])
            i += 1
        os.chdir("..")
        
    def clean_pgn(self, pgn_file):
        lines = pgn_file.readlines()
        lines = self.remove_brackets(lines)
        lines = self.remove_newlines(lines)
        lines = self.remove_turn_numbers(lines)
        separator = ""
        out_string = separator.join(lines)
        out_string = self.separate_result(out_string)
        return out_string
        
    def remove_brackets(self, lines):
        new_lines = []
        for line in lines:
            if line[0] != "[":
                new_lines.append(line)
        return new_lines
    
    def remove_newlines(self, lines):
        new_lines = []
        for line in lines:
            if line[0] != "\n":
                line = line.strip()
            new_lines.append(line)
        return new_lines

    def remove_turn_numbers(self, lines):
        space = " "
        new_lines = []
        for line in lines:
            line_list = line.split(".")
            if len(line_list) > 1:
                line_list = line_list[1:]
                chunks = []
                for chunk in line_list[:-1]:
                    chunk_list = chunk.split(" ")[:-1]
                    chunk = space.join(chunk_list)
                    chunks.append(chunk)
                chunks.append(line_list[-1])
                line = space.join(chunks) + " "
            new_lines.append(line)
        return new_lines

    def separate_result(self, out_string):
        out_list = out_string.split("  ")
        out_string = "\n".join(out_list)
        out_string = out_string.replace(" \n", "\n")
        return out_string[1:-1] + "\n"

if __name__ == "__main__":
    c = Converter("pgn_files", "linear_bool_dataset.csv")
    c.convert()