from tensorflow import keras
#from naoqi import ALProxy
from Robot_Speech import get_question
from Process_Audio import process_audio_input
import time
import sys
import os

def main():
    os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'

    #Code to Control Robot
    robot_ip = "192.168.0.22"
    port = 9559
    res_wait_time = 1

    #Load Models
    audio_model = keras.models.load_model("Saved_Model/Audio_Network.h5")

    #Connect Robot Proxies
    text_to_speech = ALProxy("ALTextToSpeech", robot_ip, port)
    record = ALProxy("ALAudioRecorder", robot_ip, port)

    #Start Main Loop
    text_to_speech.say("Hello! Want to begin? Say One for Yes and Zero for No")
    record.startMicrophonesRecording("Tmp_Recordings/Response/response.wav", 'wav', 16000, (0, 0, 1, 0))
    time.sleep(res_wait_time)
    record.stopMicrophonesRecording()

    response = process_audio_input(audio_model, "Tmp_Recordings/Response/response.wav")
    time.sleep(3)

    #Main Loop
    if(response == 1):
        check = 1
        ques_txt, ans = get_question()
        while(check == 1):
            text_to_speech.say(ques_txt)
            record.startMicrophonesRecording("Tmp_Recordings/Answer/ans.wav", 'wav', 16000, (0, 0, 1, 0))
            time.sleep(res_wait_time)
            record.stopMicrophonesRecording()

            ans_in = process_audio_input(audio_model, "Tmp_Recordings/Answer/ans.wav")

            if(ans == ans_in):
                text_to_speech.say("Correct!")
                time.sleep(res_wait_time)

                text_to_speech.say("Do you want to continue? Say One for Yes and Zero for No")
                record.startMicrophonesRecording("Tmp_Recordings/Response/response.wav", 'wav', 16000, (0, 0, 1, 0))
                time.sleep(res_wait_time)
                record.stopMicrophonesRecording()

                response = process_audio_input(audio_model, "Tmp_Recordings/Response/response.wav")
                if(response == 1):
                    ques_txt, ans = get_question()
                else:
                    check = 0
            else:
                text_to_speech.say("Not Correct, Try again.")
                time.sleep(res_wait_time)

    #End and Cleanup
    text_to_speech.say("Thanks! Bye!")

    for file in os.listdir("Tmp_Recordings/Response"):
        os.remove("Tmp_Recordings/Response/" + file)

    for file in os.listdir("Tmp_Recordings/Answer"):
        os.remove("Tmp_Recordings/Answer/" + file)

if __name__ == "__main__":
    main()