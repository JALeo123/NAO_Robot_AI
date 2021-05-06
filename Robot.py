from naoqi import ALProxy
import time
import RobotGlobals

IMAGE_WIDTH_IDX = 0
IMAGE_HEIGHT_IDX = 1
IMAGE_DATA_IDX = 6

class Robot:
    def __init__(self):
        self.IP = "169.254.218.180"
        self.PORT = 9559

        # Audio Configuration
        self.audio_path = RobotGlobals.ROBOT_AUDIO_FILE

        # Video Configuration
        self.name_id = "edu_bot"
        self.resolution = 1 #QVGA i.e. 320x240
        self.color_space = 9 #kYUV422InterlacedColorSpace
        self.fps = 5

        print("Initializing Proxies...")

        # ALProxies
        self.text_to_speech = ALProxy("ALTextToSpeech", self.IP, self.PORT)
        time.sleep(2)
        self.audio_recorder = ALProxy("ALAudioRecorder", self.IP, self.PORT)
        time.sleep(2)
        self.photo_capture = ALProxy("ALPhotoCapture", self.IP, self.PORT)
        #self.video_device = ALProxy("ALVideoDevice", self.IP, self.PORT)
        time.sleep(2)

        # Subscribe
        self.photo_capture.setResolution(2)
        self.photo_capture.setPictureFormat("jpg")
        #self.image_client = \
        #    self.video_device.subscribe(self.name_id, self.resolution, self.color_space, self.fps)

        print("Robot initialized...")
        return

    # def __del__(self):
    #     self.video_device.unsubscribe(self.image_client)

    def say(self, text):
        self.text_to_speech.say(text)
        return

    def stop_rec(self):
        self.audio_recorder.stopMicrophonesRecording()
        return

    def record_audio(self, sleep_seconds):
        self.audio_recorder.startMicrophonesRecording(self.audio_path, 'wav', 16000, (0, 0, 1, 0))
        time.sleep(sleep_seconds)
        self.audio_recorder.stopMicrophonesRecording()
        return

    def get_image(self):
        self.photo_capture.takePictures(1, RobotGlobals.ROBOT_DIR, RobotGlobals.PHOTO_FILENAME_BASE)
        #return self.photo_capture.getImageRemote(self.image_client)
