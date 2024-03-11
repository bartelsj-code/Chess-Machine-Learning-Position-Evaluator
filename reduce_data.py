import numpy as np
import random
import os

positions_filepath = 'even_files/positions.npy'
metadata_filepath = 'even_files/metadata.npy'
results_filepath = 'even_files/results_Y.npy'
positions = np.load(positions_filepath)
metadata = np.load(metadata_filepath)
labels = np.load(results_filepath)
print(np.shape(positions))
print(np.shape(metadata))
print(np.shape(labels))

def shorten_to_length(array, length):
    array2 = array[:length]
    return array2

position_out = shorten_to_length(positions, 500000)
metadata_out = shorten_to_length(metadata, 500000)
labels_out = shorten_to_length(labels, 500000)

print(np.shape(position_out))
print(np.shape(metadata_out))
print(np.shape(labels_out))

def write_files(path, pos, met, res):
    np.save(path+"/positions.npy", pos)
    np.save(path+"/metadata.npy", met)
    np.save(path+"/results_Y.npy", res)
    
# write_files("even_files", positions, metadata, results_Y)
write_files("even_files_shortened", position_out, metadata_out, labels_out)
