import sys
import time
import logging
from pyautogui import *
import pyautogui
from moviepy.editor import VideoFileClip
import os
import random
import requests as r
import glob
import keyboard
from obswebsocket import obsws, requests  # noqa: E402
from winotify import Notification, audio
import pytesseract as tess 
from pytesseract import *
import cv2
logging.basicConfig(level=logging.INFO)
sys.path.append('../')

"""
OBS WEB SOCKET CONFIG:
"""
host = "localhost" # DONT CHANGE
port = 4445 # Enter OBS Web Socket Port
password = "" # Enter Auth PWD
"""
API CONFIG
"""
RLCLIP_API_TOKEN = '' # Input Your API Key 
RLCLIP_USERNAME = '' # Enter your Username
RLCLIP_API_URL = 'https://rlclip.xyz/api/v1/clips/'

ws = obsws(host, port, password)
ws.connect()

recording = True # DONT CHANGE
api_request = False # DONT CHANGE
y = True # DONT CHANGE

try:
    path_of_the_directory= 'videos'
    for filename in os.listdir(path_of_the_directory):
        f = os.path.join(path_of_the_directory,filename)
        if os.path.isfile(f):
            time.sleep(1)
            os.remove(f)
    path_of_the_directory= 'clips'
    for filename in os.listdir(path_of_the_directory):
        f = os.path.join(path_of_the_directory,filename)
        if os.path.isfile(f):
            time.sleep(1)
            os.remove(f)
    while y != False:
        if recording == True:
            ws.call(requests.StartRecording())
        """
        Start of Manuel Clipping (F9) Key
        """
        while True:
            if keyboard.is_pressed("F9"):
                notification_alert = Notification(app_id="RLClip",title="Your clip is being Processed!",msg="You will receive another notification when your clip is ready!",duration="short",icon="")
                notification_alert.set_audio(audio.Mail, loop=False)
                notification_alert.show()                
                ws.call(requests.StopRecording())
                time.sleep(0.5)
                recording = False
                time.sleep(2)
                folder_path = r'videos'
                file_type = r'\*.mp4'
                files = glob.glob(folder_path + file_type)
                latest_video = max(files, key=os.path.getctime)
                clip = VideoFileClip(latest_video)
                if clip.duration > 15:
                    print("File over 15 seconds")
                    clip = clip.subclip(clip.duration-15, clip.duration)
                else:
                    print("nope")
                    clip = VideoFileClip(latest_video)
                clip.write_videofile("clips/{}.mp4".format(random.randint(1, 1930183912434131)))

                time.sleep(5)
                api_request = True
                if api_request == True:
                    folder_path = r'clips'
                    file_type = r'\*.mp4'
                    files = glob.glob(folder_path + file_type)
                    newest_clip = max(files, key=os.path.getctime)
                    data = {'user': '{}'.format(RLCLIP_USERNAME)}
                    headers = {'Authorization': 'Token {}'.format(RLCLIP_API_TOKEN)}
                    files = { 'video_file': open(newest_clip, 'rb')}
                    r.post(RLCLIP_API_URL, headers=headers , data=data, files=files)
                    recording = True
                    notification_alert = Notification(app_id="RLClip",title="New RLClip has been saved!",msg="Your clip is now ready at rlclip.xyz!",duration="short",icon="")
                    notification_alert.add_actions(label="Take me to my clip!", launch="https://rlclip.xyz/media/clips/{}".format(newest_clip.replace("clips\\","")))
                    notification_alert.show()
                    api_request = False
                break
        """
        END of Manuel Clipping (F8) Key
        """
        #-------------------------------------------------------------------------------------------------------------
        """
        Start Of Flip Reset Image Rec
        """

        # if pyautogui.locateOnScreen('Screenshot_615.png',  confidence=0.4) or pyautogui.locateOnScreen('Screenshot_616.png',  confidence=0.4) != None:
        #     print("Yesss, Flip Reset Yesss")
        #     end_time = time.time() + 12
        #     while True:
        #         if pyautogui.locateOnScreen('Screenshot_617.png', confidence=0.5) != None:
        #             ws.call(requests.StopRecording())
        #             time.sleep(0.5)
        #             recording = False
        #             time.sleep(2)
        #             folder_path = r'videos'
        #             file_type = r'\*.mp4'
        #             files = glob.glob(folder_path + file_type)
        #             latest_video = max(files, key=os.path.getctime)
        #             clip = VideoFileClip(latest_video)
        #             if clip.duration > 15:
        #                 print("File over 15 seconds")
        #                 clip = clip.subclip(clip.duration-15, clip.duration)
        #             else:
        #                 clip = VideoFileClip(latest_video)
        #             clip.write_videofile("clips/{}.mp4".format(random.randint(1, 1930183912434131)))
        #             time.sleep(5)
        #             api_request = True
        #             if api_request == True:
        #                 folder_path = r'clips'
        #                 file_type = r'\*.mp4'
        #                 files = glob.glob(folder_path + file_type)
        #                 newest_clip = max(files, key=os.path.getctime)
        #                 data = {'user': '{}'.format(RLCLIP_USERNAME)}
        #                 headers = {'Authorization': 'Token {}'.format(RLCLIP_API_TOKEN)}
        #                 files = { 'video_file': open(newest_clip, 'rb')}
        #                 r.post(RLCLIP_API_URL, headers=headers , data=data, files=files)
        #                 recording = True
        #                 api_request = False

        #         if time.time() > end_time:
        #             print("Timer ended.")
        #             break

        """
        End Of Flip Reset Image Rec
        """
except KeyboardInterrupt:
    ws.call(requests.StopRecording())
    pass

time.sleep(99999)
ws.disconnect()