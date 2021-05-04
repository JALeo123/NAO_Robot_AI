from naoqi import ALProxy
import time
import os
import scp
import sys

def main():
    # Code to Control Robot
    robot_ip = "192.168.0.22"
    port = 9559
    res_wait_time = 1
    robot_audio_path = "Tmp_Data/response.wav"
    pc_audio_path = "Tmp_Data/Tmp_Data_Raw/response.wav"
    user = "nao"
    password = "nao"



    #Connect Robot Proxies
    text_to_speech = ALProxy("ALTextToSpeech", robot_ip, port)
    record = ALProxy("ALAudioRecorder", robot_ip, port)

    #Set Up
    client = scp.Client(host=robot_ip, user=user, password=password)

    #Start Main Loop
    text_to_speech.say("Hello! Want to begin? Say One for Yes and Zero for No")

    record_transfer(record, client, robot_audio_path, pc_audio_path, res_wait_time)
    response = get_processed_response()

    #Main Loop
    if(response == 1):
        check = 1
        ques_txt, ans = get_question()
        while(check == 1):
            text_to_speech.say(ques_txt)

            record_transfer(record, client, robot_audio_path, pc_audio_path, res_wait_time)
            ans_in = get_processed_response()

            if(ans == ans_in):
                text_to_speech.say("Correct!")
                time.sleep(res_wait_time)

                text_to_speech.say("Do you want to continue? Say One for Yes and Zero for No")

                record_transfer(record, client, robot_audio_path, pc_audio_path, res_wait_time)
                response = get_processed_response()
                if(response == 1):
                    ques_txt, ans = get_question()
                else:
                    check = 0
            else:
                text_to_speech.say("Not Correct, Try again.")
                time.sleep(res_wait_time)

    #End and Cleanup
    text_to_speech.say("Thanks! Bye!")

    for file in os.listdir("Tmp_Data_Raw/Tmp_Data_Processed"):
        os.remove("Tmp_Data_Raw/Tmp_Data_Processed/" + file)

    end_program()

def record_transfer(record, client, robot_audio_path, pc_audio_path, res_wait_time):
    record.startMicrophonesRecording(robot_audio_path, 'wav', 16000, (0, 0, 1, 0))
    time.sleep(res_wait_time)
    record.stopMicrophonesRecording()
    time.sleep(res_wait_time)

    client.transfer(pc_audio_path, robot_audio_path)

def get_processed_response():
    #Get Processed Data
    while(len(os.listdir("Tmp_Data/Tmp_Data_Processed")) == 0):
        pass

    file_p = os.listdir("Tmp_Data/Tmp_Data_Processed")[0]
    file = open("Tmp_Data/Tmp_Data_Processed/"+file_p, "r")
    file_line = file.readlines()
    response = file_line[0]

    # Delete Processed Data
    for file in os.listdir("Tmp_Data/Tmp_Data_Processed"):
        os.remove("Tmp_Data/Tmp_Data_Processed/" + file)

    return response

def end_program():
    file = open("Tmp_Data/Tmp_Data_Raw/end.txt", "w")
    file.close()

if __name__ == "__main__":
    main()