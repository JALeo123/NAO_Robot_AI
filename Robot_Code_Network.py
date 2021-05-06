from tensorflow import keras
from Robot_Speech import get_question
from Process_Audio import process_audio_input
import EmotionModel
import time
import sys
import os
import RobotGlobals

os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'

def main():
    # Load Models
    audio_model = keras.models.load_model(RobotGlobals.REPO_PATH + "Saved_Model/Audio_Network.h5")
    emotion_model = EmotionModel.EmotionModel()

    print("Finished Opening Models")
    while True:
        while len(os.listdir(RobotGlobals.RAW_DIR)) < 2:
            pass

        done = False
        file_list = os.listdir(RobotGlobals.RAW_DIR)
        for f in file_list:
            if f == "raw.done":
                done = True
                time.sleep(0.1)
                os.remove(RobotGlobals.RAW_DONE)
                break
            if f == "end.txt":
                print("Closing")
                end = True
                # Delete Raw Data
                for file in os.listdir(RobotGlobals.RAW_DIR):
                    os.remove(RobotGlobals.RAW_DIR + file)
                return

        if not done:
            continue

        for file in file_list:
            file_ext = file[-4:]

            response = None
            file_out = None

            if file_ext == ".wav":
                response = process_audio_input(audio_model, RobotGlobals.RAW_DIR+file)
                file_out = RobotGlobals.PROCESSED_AUDIO
            elif file_ext == ".jpg":
                response = emotion_model.process_file(RobotGlobals.RAW_DIR+file)
                file_out = RobotGlobals.PROCESSED_EMOTION

            if response is not None and file_out is not None:
                write_response_to_file(file_out, response)

        # Delete File
        os.remove(RobotGlobals.RAW_DIR + file)

        print("Data Processed")

        done_file = open(RobotGlobals.PROCESSED_DONE, "w")
        done_file.close()


def write_response_to_file(file, response):
    file_out = open(file, "w")
    file_out.write(str(response))
    file_out.close()


if __name__ == "__main__":
    main()
