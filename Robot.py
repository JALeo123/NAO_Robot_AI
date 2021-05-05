from naoqi import ALProxy
import time

IMAGE_WIDTH_IDX = 0
IMAGE_HEIGHT_IDX = 1
IMAGE_DATA_IDX = 6

class Robot:
    def __init__(self):
        self.IP = "169.254.167.47"
        self.PORT = 9559

        # Audio Configuration
        self.audio_path = "Tmp_Data/response.wav"

        # Video Configuration
        self.name_id = "edu_bot"
        self.resolution = 1 #QVGA i.e. 320x240
        self.color_space = 9 #kYUV422InterlacedColorSpace
        self.fps = 5

        # ALProxies
        self.test_to_speech = ALProxy("ALTextToSpeech", self.IP, self.PORT)
        self.audio_recorder = ALProxy("ALAudioRecorder", self.IP, self.PORT)
        self.video_device = ALProxy("ALVideoDevice", self.IP, self.PORT)

        # Subscribe
        self.image_client = \
            self.video_device.subscribe(self.name_id, self.resolution, self.color_space, self.fps)

        return

    def __del__(self):
        self.video_device.unsubscribe(self.image_client)

    def say(self, text):
        self.test_to_speech.say(text)
        return

    def record_audio(self, sleep_seconds):
        self.audio_recorder.startMicrophonesRecording(self.audio_path, 'wav', 16000, (0, 0, 1, 0))
        time.sleep(sleep_seconds)
        self.audio_recorder.stopMicrophonesRecording()
        return

    def get_image(self):
        return self.video_device.getImageRemote(self.image_client)
