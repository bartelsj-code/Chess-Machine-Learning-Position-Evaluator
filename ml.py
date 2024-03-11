from tensorflow import keras
from tensorflow.keras import layers
# Conv2D and MaxPooling2D provide you with convolutions and max pooling
from tensorflow.keras.layers import Conv2D, MaxPooling2D
# Rescaling is used for the data normalization (here, we want it to be in [-1,1])
# RandomFlip and RandomRotation are used for the data augmentation
from tensorflow.keras.layers.experimental.preprocessing import Rescaling, RandomFlip, RandomRotation

# Your network will use the Flatten and Dense layers after any convolutions to
# get to a final output
from tensorflow.keras.layers import Activation, Dropout, Flatten, Dense

# Look back at the lab for how I used SparseCategoricalCrossentropy
from tensorflow.keras.losses import SparseCategoricalCrossentropy
import matplotlib.pyplot as plt
import tensorflow_datasets as tfds
import tensorflow as tf
import numpy as np
import matplotlib.pyplot as plt



positions = np.load("3D Numpy Data/positions.npy")
metadata = np.load("3D Numpy Data/metadata.npy")
















