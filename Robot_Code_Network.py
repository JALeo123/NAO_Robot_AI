from tensorflow import keras
from Robot_Speech import get_question
from Process_Audio import process_audio_input
import EmotionModel
import time
import sys
import os
import cv2
import RobotGlobals

def main():
    os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'

    #Load Models
    audio_model = keras.models.load_model("Saved_Model/Audio_Network.h5")
    emotion_model = EmotionModel()

    print("Finished Opening Models")
    while(1):
        while(len(os.listdir(RAW_DIR)) == 0):
            pass

        file = os.listdir(RAW_DIR)[0]

        #Audio File
        if(file[-4:] == ".wav"):
            response = process_audio_input(audio_model, RAW_DIR+file)
        elif(file[-4:] == ".jpg"):
            response = emotion_model.process_file(RAW_DIR+file)
        elif(file[-4:] == ".txt"):
            print("Closing")
            #Delete Raw Data
            for file in os.listdir(RAW_DIR):
                os.remove(RAW_DIR + file)
            #End Program
            break

        # Write Response
        file_out = open(PROCESSED_DIR + "Tmp_Data_Processed.txt", "w")
        # TODO Need to differentiate responses
        file_out.write(str(response))
        file_out.close()

        #Delete File
        os.remove(RAW_DIR + file)

        print("Data Processed")

if __name__ == "__main__":
    main()