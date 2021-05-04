import csv
import numpy as np
import random
import pandas as pd
import glob
# Imports PIL module
from PIL import Image
import tensorflow as tf
from tensorflow import keras

def load_data_fer(height, width):
    imagesDir = r"C:\Users\david\Desktop\FER\train"

    # Labels should be sorted according to the alphanumeric
    # order of the image file paths (obtained via os.walk(directory)
    # in Python).
    # for root, dirs, files in os.walk(imagesDir):
    #     for name in dirs:
    #         print(os.path.join(root, name))

    train = tf.keras.preprocessing.image_dataset_from_directory(
                                                imagesDir,
                                                labels='inferred',
                                                validation_split=0.2,
                                                subset="training",
                                                color_mode='grayscale',
                                                seed=123,
                                                label_mode='categorical',
                                                image_size=(height, width))

    test = tf.keras.preprocessing.image_dataset_from_directory(
                                                imagesDir,
                                                validation_split=0.2,
                                                subset="validation",
                                                color_mode='grayscale',
                                                seed=123,
                                                label_mode='categorical',
                                                image_size=(height, width))

    return train, test

