# Literally just to stop tensorflow from complaining about the fact
# that my GPU isn't CUDA compatible...so I don't get ANY warning now
import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'

import tensorflow as tf
from tensorflow import keras
from sklearn import metrics
import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import time
import ImportTrainingData as data
from tensorflow.keras.metrics import Accuracy
from tensorflow.keras.applications.vgg16 import VGG16

start_time = time.time()

imgHeight = 48
imgWidth = 48

# Imports in batches of 32 by default
print("Loading data...")
train, test = data.load_data_fer(imgHeight, imgWidth)
print("Done Loading Data.")

# Normalize Data
normalization_layer = tf.keras.layers.experimental.preprocessing.Rescaling(1. / 255)
train = train.map(lambda a, b: (normalization_layer(a),b))
test = test.map(lambda a, b: (normalization_layer(a), b))

# Build Network
inputLayer = keras.layers.Input(shape=(imgHeight, imgWidth, 1))
# Conv
x = keras.layers.Conv2D(filters=64, kernel_size=(3, 3), padding="same", activation='relu')(inputLayer)
x = keras.layers.Conv2D(filters=64, kernel_size=(3, 3), padding="same", activation='relu')(x)
# Max Pool
x = keras.layers.MaxPool2D(pool_size=(2, 2), strides=(2, 2))(x)
# Conv
x = keras.layers.Conv2D(filters=128, kernel_size=(3, 3), padding="same", activation='relu')(x)
x = keras.layers.Conv2D(filters=128, kernel_size=(3, 3), padding="same", activation='relu')(x)
# Max Pool
x = keras.layers.MaxPool2D(pool_size=(2, 2), strides=(2, 2))(x)
# Flatten
x = keras.layers.Flatten()(x)
# FC 1
x = keras.layers.Dense(256, activation='relu')(x)
#################################################
x = keras.layers.Dropout(0.3)(x)
##################################################
# FC 2
x = keras.layers.Dense(256, activation='relu')(x)
##################################################
x = keras.layers.Dropout(0.3)(x)
##################################################
outputLayer = keras.layers.Dense(7, activation='softmax')(x)

# Define
model = keras.Model(inputs=inputLayer, outputs=outputLayer)

# Define metrics
metrics_list = [Accuracy()]

opt = keras.optimizers.Adam(learning_rate=0.0005)
# Compile model
model.compile(loss='categorical_crossentropy', optimizer=opt, metrics=['accuracy'])

# Summarize Model
model.summary()

# Train Model validation_data=test
history = model.fit(train, validation_data=test, shuffle=True, epochs=10)

model.save('emotion_model')

# test
model.evaluate(test, verbose=2)

print("# Parameters: %s" % model.count_params())

print("Execution Time: %s sec" % (time.time() - start_time))

# Plot history for accuracy
plt.plot(history.history['accuracy'])
plt.plot(history.history['val_accuracy'])
plt.title('Model Accuracy')
plt.ylabel('Accuracy')
plt.xlabel('Epoch')
plt.legend(['train', 'val'], loc='lower right')
plt.show()

# Plot history for loss
plt.plot(history.history['loss'])
plt.plot(history.history['val_loss'])
plt.title('Model Loss')
plt.ylabel('Loss')
plt.xlabel('Epoch')
plt.legend(['train', 'val'], loc='lower right')
plt.show()
