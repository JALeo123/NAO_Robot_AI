# Literally just to stop tensorflow from complaining about the fact
# that my GPU isn't CUDA compatible...so I don't get ANY warning now
import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'
from tensorflow import keras
from tensorflow.keras.preprocessing import image
import numpy as np
import cv2

class Emotion:
    def __init__(self):
        self.emotion_model = keras.models.load_model('emotion_model')

    def evaluate(self, input):
        # Convert to grey scale
        gray = cv2.cvtColor(input, cv2.COLOR_BGR2GRAY)
        # Resize to 48x48
        r_gray = cv2.resize(gray, (48, 48), interpolation=cv2.INTER_LINEAR)
        # Convert to array of images
        img_arr = image.img_to_array(r_gray)
        # Convert array to batch
        img_batch = np.expand_dims(img_arr, axis=0)
        # Get prediction (in one hot form)
        prediction = self.emotion_model(img_batch)
        # Convert prediction to label index
        classes = np.argmax(prediction, axis=1)
        #print(classes[0])
        # Return label index of prediction
        return classes[0]

emotion_class = Emotion()
img = cv2.imread(r'C:\Users\david\Desktop\FER\train\angry\Training_3908.jpg')
emotion_class.evaluate(img)
