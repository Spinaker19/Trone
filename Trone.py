import RPi.GPIO as GPIO
import cv2
import pygame
import os
from ffpyplayer.player import MediaPlayer

blue_button = 11
green_button = 13
red_button = 15
white_button = 29 
yellow_button = 31 
buzzer = 16
led = 18



def read_vid(Source, frameRate):
    path = "/home/pi/Trone/Source/Test/"
    file_name = path + Source
    window_name = "window"
    interframe_wait_ms = frameRate

    cap = cv2.VideoCapture(file_name)
    cap.open(file_name)
    player = MediaPlayer(file_name)
    if not cap.isOpened():
        print("Error: Could not open video.")
        exit()

    cv2.namedWindow(window_name, cv2.WND_PROP_FULLSCREEN)
    cv2.setWindowProperty(window_name, cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)
    os.system('sudo pkill fbi')
    while (True):
        ret, frame = cap.read()
        audio_frame, val = player.get_frame()
        if not ret:
            print("Reached end of video, exiting.")
            break

        cv2.imshow(window_name, frame)
        if cv2.waitKey(interframe_wait_ms) & 0x7F == ord('q'):
            print("Exit requested.")
            break
        
        if val != 'eof' and audio_frame is not None:
            #audio
            img, t = audio_frame

    cap.release()
    cv2.destroyAllWindows()
    os.system('sudo fbi -T 1 Background.jpg')

def play_sound(source):
    os.system('sudo pkill fbi')
    #os.system('sudo fbi -T 1 Test.jpg')
    path = "/home/pi/Trone/Source/Sono/"
    file_name = path + source
    pygame.mixer.init()
    pygame.mixer.load(file_name)
    pygame.mixer.set_volume(1.0)
    pygame.mixer.music.play()
    while pygame.mixer.music.get_busy():
        pass
    print("Son joue")
    #os.system('sudo pkill fbi')
    os.system('sudo fbi -T 1 Background.jpg')

def mainloop():
    GPIO.setmode(GPIO.BOARD)
    GPIO.setwarnings(False)
    GPIO.setup(blue_button, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
    GPIO.setup(green_button, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
    GPIO.setup(red_button, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
    GPIO.setup(white_button, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
    GPIO.setup(yellow_button, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
    GPIO.setup(buzzer, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
    GPIO.setup(led, GPIO.OUT)
    GPIO.setup(36, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
    
    while True:
        if GPIO.input (blue_button) :
            read_vid("TestBlanc.mp4", 25)
        elif GPIO.input (green_button) :
            read_vid("TestBleue.mp4", 25)
        elif GPIO.input (red_button) :
            read_vid("TestJaune.mp4", 25)
        elif GPIO.input (white_button) :
            read_vid("TestRouge.mp4", 25)
        elif GPIO.input (yellow_button) :
            read_vid("TestVerte.mp4", 25)
        elif GPIO.input (buzzer) :
            GPIO.output (led, GPIO.HIGH)
            play_sound("Alarm_boat.mp3")
            #read_vid("TestBuzzer.mp4", 25)
            GPIO.output (led, GPIO.LOW)
        elif GPIO.input (36):
            os.system('sudo pkill fbi')
            break

os.system('sudo fbi -T 1 Background.jpg')
mainloop()