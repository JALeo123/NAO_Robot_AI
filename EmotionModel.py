# Literally just to stop tensorflow from complaining about the fact
# that my GPU isn't CUDA compatible...so I don't get ANY warning now
import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'

from tensorflow import keras
from tensorflow.keras.preprocessing import image
import numpy as np
import glob
import cv2

class Emotion:
    def __init__(self):
        self.emotion_model = keras.models.load_model('emotion_model')
        self.last_result = None
        self.ANGRY = 0
        self.DISGUST = 1
        self.FEAR = 2
        self.HAPPY = 3
        self.NEUTRAL = 4
        self.SAD = 5
        self.SURPRISE = 6

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
        self.last_result = classes[0]
        return self.last_result

    def result_string_raw(self):
        switcher = {
            self.ANGRY:     "Angry",
            self.DISGUST:   "Disgust",
            self.FEAR:      "Fear",
            self.HAPPY:     "Happy",
            self.NEUTRAL:   "Neutral",
            self.SAD:       "Sad",
            self.SURPRISE:  "Surprise",
            None:           "Error",
        }
        return switcher.get(self.last_result)

    def result_string_reduced(self):
        switcher = {
            self.HAPPY:     "Positive",

            self.NEUTRAL:   "Neutral",

            self.ANGRY:     "Negative",
            self.DISGUST:   "Negative",
            self.FEAR:      "Negative",
            self.SAD:       "Negative",
            self.SURPRISE:  "Negative",

            None:           "Error",
        }
        return switcher.get(self.last_result)

    def result_int_reduced(self):
        switcher = {
            self.HAPPY:     1,

            self.NEUTRAL:   0,

            self.ANGRY:     (-1),
            self.DISGUST:   (-1),
            self.FEAR:      (-1),
            self.SAD:       (-1),
            self.SURPRISE:  (-1),

            None:           0,
        }
        return switcher.get(self.last_result)

# Functions not associated with class


def example():
    emotion_class = Emotion()
    img = cv2.imread(r'C:\Users\david\Desktop\FER\train\angry\Training_3908.jpg')
    emotion_class.evaluate(img)
    print(emotion_class.result_string_raw())
    print(emotion_class.result_string_reduced())
    return


def evaluateDirectory():
    positives = 0
    neutrals = 0
    negatives = 0

    emotion_class = Emotion()
    files = glob.glob(r"C:\Users\david\Desktop\FER\test\surprise\*.jpg")
    for file in files:
        # Read the image
        image = cv2.imread(file)
        emotion_class.evaluate(image)
        if emotion_class.result_int_reduced() == 0:
            neutrals += 1
        elif emotion_class.result_int_reduced() == 1:
            positives += 1
        elif emotion_class.result_int_reduced() == -1:
            negatives += 1
    print("Positives: ", positives)
    print("Neutrals: ", neutrals)
    print("Negatives: ", negatives)
    return


#evaluateDirectory()
