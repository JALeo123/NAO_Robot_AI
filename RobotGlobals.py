# These top two need to be changed based on the computer
TMP_DATA_DIR = "C:/Users/David Schendt/Desktop/"
REPO_PATH = "C:/Users/David Schendt/Documents/GitHub/NAO_Robot_AI/"

PROCESSED_DIR = TMP_DATA_DIR + "Tmp_Data_Processed/"
RAW_DIR = TMP_DATA_DIR + "Tmp_Data_Raw/"

PROCESSED_EMOTION = PROCESSED_DIR + "emotion.txt"
PROCESSED_AUDIO = PROCESSED_DIR + "audio.txt"
PROCESSED_DONE = PROCESSED_DIR + "processed.done"

ROBOT_DIR = "/home/nao/naoqi/"
ROBOT_AUDIO_FILE = ROBOT_DIR + "response.wav"

PHOTO_FILENAME_BASE = "emotion"
ROBOT_PHOTO_FILENAME = PHOTO_FILENAME_BASE + ".jpg"
ROBOT_PHOTO_FILE_PATH = ROBOT_DIR + ROBOT_PHOTO_FILENAME

LOCAL_AUDIO_FILE = RAW_DIR + "response.wav"
LOCAL_PHOTO_FILE = RAW_DIR + PHOTO_FILENAME_BASE + ".jpg"
RAW_DONE = RAW_DIR + "raw.done"
