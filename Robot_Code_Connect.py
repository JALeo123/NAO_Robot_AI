from naoqi import ALProxy
import time
import os
import scp
import sys
import Robot
import RobotGlobals

res_wait_time = 1
user = "nao"
password = "nao"


def main():
    robot = Robot()

    #Set Up
    client = scp.Client(host=robot.IP, user=user, password=password)

    #Start Main Loop
    robot.say("Hello! Want to begin? Say One for Yes and Zero for No")

    record_transfer(robot, client)
    response = get_processed_response()

    #Main Loop
    if(response == 1):
        check = 1
        ques_txt, ans = get_question()
        while(check == 1):
            robot.say(ques_txt)

            record_transfer(robot, client)
            ans_in = get_processed_response()

            if(ans == ans_in):
                robot.say("Correct!")
                time.sleep(res_wait_time)

                robot.say("Do you want to continue? Say One for Yes and Zero for No")

                record_transfer(robot, client)
                response = get_processed_response()
                if(response == 1):
                    ques_txt, ans = get_question()
                else:
                    check = 0
            else:
                robot.say("Not Correct, Try again.")
                time.sleep(res_wait_time)

            nao_img = robot.get_image()
            image = Image.fromstring("RBG",
                                     (nao_img[IMAGE_WIDTH_IDX], nao_img[IMAGE_HEIGHT_IDX]),
                                     nao_img[IMAGE_DATA_IDX])
            image.save(RAW_DIR + "emotion.jpg", "JPG")

    #End and Cleanup
    robot.say("Thanks! Bye!")

    for file in os.listdir(PROCESSED_DIR):
        os.remove(PROCESSED_DIR + file)

    end_program()

def record_transfer(robot, client):
    robot.record_audio(res_wait_time)
    time.sleep(res_wait_time)
    client.transfer(LOCAL_AUDIO_FILE, ROBOT_AUDIO_FILE)

def get_processed_response():
    #Get Processed Data
    while(len(os.listdir(PROCESSED_DIR)) == 0):
        pass

    file_p = os.listdir(PROCESSED_DIR)[0]
    file = open(PROCESSED_DIR + file_p, "r")
    file_line = file.readlines()
    response = file_line[0]

    # Delete Processed Data
    for file in os.listdir(PROCESSED_DIR):
        os.remove(PROCESSED_DIR + file)

    return response

def end_program():
    file = open(RAW_DIR + "end.txt", "w")
    file.close()

if __name__ == "__main__":
    main()