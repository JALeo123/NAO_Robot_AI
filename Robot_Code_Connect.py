from naoqi import ALProxy
import time
import os
import scp
import sys
import Robot
import RobotGlobals
import Robot_Speech
from PIL import Image

res_wait_time = 1
user = "nao"
password = "nao"


def main():
    robot = Robot.Robot()

    # Set Up
    client = scp.Client(host=robot.IP, user=user, password=password)

    # Start Main Loop
    robot.say("Hello! Want to begin? Say One for Yes and Zero for No")

    record_data(robot, client)
    emotion, response = get_processed_response()

    # Main Loop
    if response == 1:
        check = 1
        ques_txt, ans = Robot_Speech.get_question()
        while check == 1:
            robot.say(ques_txt)

            record_data(robot, client)
            emotion, ans_in = get_processed_response()

            if ans == ans_in:
                robot.say("Correct!")
                time.sleep(res_wait_time)

                robot.say("Do you want to continue? Say One for Yes and Zero for No")

                record_data(robot, client)
                emotion, response = get_processed_response()
                if response == 1:
                    ques_txt, ans = Robot_Speech.get_question()
                else:
                    check = 0
            elif emotion == "Negative":
                # TODO
                # Just to have feedback
                robot.say("Looks like your upset")
            else:
                robot.say("Not Correct, Try again.")
                time.sleep(res_wait_time)

    # End and Cleanup
    robot.say("Thanks! Bye!")

    for file in os.listdir(RobotGlobals.PROCESSED_DIR):
        os.remove(RobotGlobals.PROCESSED_DIR + file)

    end_program()


def record_data(robot, client):
    record_transfer(robot, client)
    save_image(robot)
    time.sleep(res_wait_time)


def record_transfer(robot, client):
    robot.record_audio(res_wait_time)
    time.sleep(res_wait_time)
    client.transfer(RobotGlobals.LOCAL_AUDIO_FILE, RobotGlobals.ROBOT_AUDIO_FILE)


def save_image(robot):
    nao_img = robot.get_image()
    image = Image.fromstring("RBG",
                             (nao_img[Robot.IMAGE_WIDTH_IDX], nao_img[Robot.IMAGE_HEIGHT_IDX]),
                             str(bytearray(nao_img[Robot.IMAGE_DATA_IDX])))
    image.save(RobotGlobals.RAW_DIR + "emotion.jpg")


def get_processed_response():
    # Get Processed Data
    while len(os.listdir(RobotGlobals.PROCESSED_DIR)) != 2:
        pass

    # Get first file and open
    emotion_file = open(RobotGlobals.PROCESSED_EMOTION, "r")
    audio_file = open(RobotGlobals.PROCESSED_AUDIO, "r")

    # Read data
    emotion = emotion_file.readlines()[0]
    response = audio_file.readlines()[0]

    # Delete Processed Data
    os.remove(RobotGlobals.PROCESSED_AUDIO)
    os.remove(RobotGlobals.PROCESSED_EMOTION)

    return emotion, response


def end_program():
    file = open(RobotGlobals.RAW_DIR + "end.txt", "w")
    file.close()


if __name__ == "__main__":
    main()
