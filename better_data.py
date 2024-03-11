import numpy as np
import random
import os

positions_filepath = 'large_data/positions.npy'
bonus_data_filepath = 'large_data/metadata.npy'
positions = np.load(positions_filepath)
bonus_data = np.load(bonus_data_filepath)
metadata = np.array([arr[:7] for arr in bonus_data])
results_Y = np.array([arr[7] for arr in bonus_data])
print(np.shape(positions))
print(np.shape(metadata))
print(np.shape(results_Y))

def shuffle_data(pos_array, met_array, res_array):
    print("shuffling")
    inds =[i for i in range(len(res_array))]
    random.shuffle(inds)
    print("copying arrays")
    temp_pos = np.copy(pos_array)
    temp_met = np.copy(met_array)
    temp_res = np.copy(res_array)
    i = 0
    for index in inds:
        if i%10000 == 0:
            print("reassigning: {}/{}".format(i, len(res_array)))
        pos_array[i] = temp_pos[index]
        met_array[i] = temp_met[index]
        res_array[i] = temp_res[index]
        i+=1

def get_ratios(r):
    white_total = 0
    black_total = 0
    draw_total = 0
    total = len(r)
    for i in range(total):
        res = r[i]
        if res == 0:
            draw_total += 1
        if res == -1:
            black_total += 1
        if res == 1:
            white_total += 1
    return white_total, black_total, draw_total, total

shuffle_data(positions, metadata, results_Y)

white_total, black_total, draw_total, total = get_ratios(results_Y)
print("result ratios:\n\t white wins: {}       black wins: {}      draw: {}".format(white_total/total, black_total/total, draw_total/total))

#create even-split dataset
component_length = min(draw_total, black_total, white_total)
white_wins= [[],[],[]]
draws= [[],[],[]]
black_wins= [[],[],[]]
for i in range(len(results_Y)):
    if i%10000 == 0:
        print("{}/{}".format(i, len(results_Y)))
    if results_Y[i] == 0:
        draws[0].append(positions[i])
        draws[1].append(metadata[i])
        draws[2].append(results_Y[i])
    if results_Y[i] == 1:
        white_wins[0].append(positions[i])
        white_wins[1].append(metadata[i])
        white_wins[2].append(results_Y[i])
    if results_Y[i] == -1:
        black_wins[0].append(positions[i])
        black_wins[1].append(metadata[i])
        black_wins[2].append(results_Y[i])
print("making even arrays")
positions_even = np.array(white_wins[0][:component_length] + black_wins[0][:component_length] + draws[0][:component_length])
metadata_even = np.array(white_wins[1][:component_length] + black_wins[1][:component_length] + draws[1][:component_length])
results_Y_even = np.array(white_wins[2][:component_length] + black_wins[2][:component_length] + draws[2][:component_length])
shuffle_data(positions_even, metadata_even, results_Y_even)

white_total, black_total, draw_total, total = get_ratios(results_Y_even)
print("result ratios:\n\t white wins: {}       black wins: {}      draw: {}".format(white_total/total, black_total/total, draw_total/total))

print("length even:" +str(len(results_Y_even)))

def write_files(path, pos, met, res):
    np.save(path+"/positions.npy", pos)
    np.save(path+"/metadata.npy", met)
    np.save(path+"/results_Y.npy", res)
    
# write_files("even_files", positions, metadata, results_Y)
write_files("even_files", positions_even, metadata_even, results_Y_even)
