from naoqi import ALProxy
import time
import os
import scp
import paramiko
import sys
import Robot
import RobotGlobals
import Robot_Speech
from PIL import Image

os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'

res_wait_time = 0.5
user = "nao"
password = "nao"


def main():
    robot = Robot.Robot()

    # Set Up
    ssh_client = paramiko.SSHClient()
    ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh_client.connect(hostname=robot.IP, username=user, password=password)
    client = scp.SCPClient(ssh_client.get_transport())

    # Start Main Loop
    robot.say("Hello! Want to begin? Say One for Yes and Zero for No")

    record_data(robot, client)
    emotion, response = get_processed_response()

    print(response)
    # Main Loop
    if response != 0:
        check = 1
        ques_txt, ans = Robot_Speech.get_question()
        while check == 1:
            robot.say(ques_txt)

            time.sleep(0.5)
            record_data(robot, client)
            emotion, ans_in = get_processed_response()

            print("Read Emotion: " + emotion)
            print("Read Answer: " + ans_in)
            print("Expected Answer: " + str(ans))

            if str(ans) == ans_in:
                robot.say("Correct!")
                time.sleep(res_wait_time)

                robot.say("Do you want to continue? Say One for Yes and Zero for No")

                record_data(robot, client)
                emotion, response = get_processed_response()
                if response != "0":
                    ques_txt, ans = Robot_Speech.get_question()
                else:
                    check = 0
            elif ans_in == "10":
                # Do nothing
                continue
            else:
                robot.say("Not Correct.")

                if emotion == "Negative":
                    # Just to have feedback
                    robot.say("Looks like your upset.")
                    robot.say("Keep trying, buddy.")

    # End and Cleanup
    robot.say("Thanks! Bye!")

    for file in os.listdir(RobotGlobals.PROCESSED_DIR):
        os.remove(RobotGlobals.PROCESSED_DIR + file)

    end_program()


def record_data(robot, client):
    record_transfer(robot, client)
    save_image(robot, client)
    # File indicating we are done
    done_file = open(RobotGlobals.RAW_DONE, "w")
    done_file.close()


def record_transfer(robot, client):
    robot.record_audio(2)
    time.sleep(res_wait_time)
    client.get(RobotGlobals.ROBOT_AUDIO_FILE, RobotGlobals.LOCAL_AUDIO_FILE)
    #client.put(RobotGlobals.LOCAL_AUDIO_FILE, RobotGlobals.ROBOT_AUDIO_FILE)


def save_image(robot, client):
    robot.get_image()
    client.get(RobotGlobals.ROBOT_PHOTO_FILE_PATH, RobotGlobals.LOCAL_PHOTO_FILE)
    # image = Image.fromstring("RBG",
    #                          (nao_img[Robot.IMAGE_WIDTH_IDX], nao_img[Robot.IMAGE_HEIGHT_IDX]),
    #                          str(bytearray(nao_img[Robot.IMAGE_DATA_IDX])))
    #image.save(RobotGlobals.RAW_DIR + "emotion.jpg")


def get_processed_response():
    while True:
        # Get Processed Data
        while len(os.listdir(RobotGlobals.PROCESSED_DIR)) < 2:
            pass

        done = False
        file_list = os.listdir(RobotGlobals.PROCESSED_DIR)
        for f in file_list:
            if f == "processed.done":
                done = True
                time.sleep(0.1)
                os.remove(RobotGlobals.PROCESSED_DONE)
                break

        if done:
            break

    emotion_file = open(RobotGlobals.PROCESSED_EMOTION, "r")
    emotion = emotion_file.readlines()[0]
    emotion_file.close()

    audio_file = open(RobotGlobals.PROCESSED_AUDIO, "r")
    response = audio_file.readlines()[0]
    audio_file.close()

    # Delete Processed Data
    os.remove(RobotGlobals.PROCESSED_AUDIO)
    os.remove(RobotGlobals.PROCESSED_EMOTION)

    return emotion, response


def end_program():
    file = open(RobotGlobals.RAW_DIR + "end.txt", "w")
    file.close()


if __name__ == "__main__":
    main()
