from tensorflow import keras
from Robot_Speech import get_question
from Process_Audio import process_audio_input
import EmotionModel
import time
import sys
import os
import RobotGlobals


def main():
    os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'

    # Load Models
    audio_model = keras.models.load_model("Saved_Model/Audio_Network.h5")
    emotion_model = EmotionModel.EmotionModel()

    print("Finished Opening Models")
    while True:
        while len(os.listdir(RobotGlobals.RAW_DIR)) == 0:
            pass

        file = os.listdir(RobotGlobals.RAW_DIR)[0]
        file_ext = file[-4:]

        response = None
        file_out = None

        if file_ext == ".wav":
            response = process_audio_input(audio_model, RobotGlobals.RAW_DIR+file)
            file_out = RobotGlobals.PROCESSED_AUDIO
        elif file_ext == ".jpg":
            response = emotion_model.process_file(RobotGlobals.RAW_DIR+file)
            file_out = RobotGlobals.PROCESSED_EMOTION
        elif file_ext == ".txt":
            print("Closing")
            # Delete Raw Data
            for file in os.listdir(RobotGlobals.RAW_DIR):
                os.remove(RobotGlobals.RAW_DIR + file)
            # End Program
            break

        if response is not None and file_out is not None:
            write_response_to_file(file_out, response)

        # Delete File
        os.remove(RobotGlobals.RAW_DIR + file)

        print("Data Processed")


def write_response_to_file(file, response):
    file_out = open(file, "w")
    file_out.write(str(response))
    file_out.close()


if __name__ == "__main__":
    main()
