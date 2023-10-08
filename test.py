import requests
import speech_recognition as sp
import pyttsx3
import pymongo
import keyboard
import serial
import time
import sys
from termcolor import colored   
rasa_server_url = "http://localhost:5005" 
conversation_id = "default"  
engine = pyttsx3.init()
recognizer = sp.Recognizer()
client = pymongo.MongoClient("mongodb://localhost:27017")
DataBase = client['BotRush2k23']
v_coll = DataBase["VoiceMode"]
ardDat = serial.Serial('com6',115200)
voice_mode = False
while True:
    
    if(voice_mode):
        with sp.Microphone() as src:
            recognizer.adjust_for_ambient_noise(src,duration = 2)
            try:
                engine.say("Listening")
                engine.runAndWait()
                audio = recognizer.listen(src,timeout = 3)
                user_message = recognizer.recognize_google(audio)
                user_message.lower()
                if(user_message == "stop" or user_message == "deactivate"):
                     engine.say("Deactivating voice assistant mode")
                     engine.runAndWait()
                     voice_mode = not voice_mode
                elif user_message == "light on" or user_message=="led on":
                     ardDat.write(str("1").encode())
                     message = "Turning on LED....\n"
                     engine.say(message.strip("....\n"))
                     engine.runAndWait()
                     coloured_message = colored(message,"yellow")
                     for i in coloured_message:
                          sys.stdout.write(i)
                          time.sleep(0.04)
                          sys.stdout.flush()
                     
                     time.sleep(5.4)
                elif user_message == "light off" or user_message == "led off":
                     ardDat.write(str("0").encode())
                     message = "Turning off LED....\n"
                     engine.say(message.strip("....\n"))
                     engine.runAndWait()
                     coloured_message = colored(message,"yellow")
                     for i in coloured_message:
                          sys.stdout.write(i)
                          time.sleep(0.04)
                          sys.stdout.flush()
                   
                     time.sleep(5.4)
                else:
                    user_input_url = f"{rasa_server_url}/webhooks/rest/webhook"
                    payload = {
                        "sender": conversation_id,
                        "message": user_message
                    }

                    response = requests.post(user_input_url, json=payload)
                    bot_responses = response.json()
                    print("Bot Responses:")
                    for bot_response in bot_responses:
                        print(bot_response['text'])
                        
                        engine.say(bot_response['text'])
                        engine.runAndWait()
            except sp.UnknownValueError:
                engine.say("Sorry, couldn't catch that")
            except sp.WaitTimeoutError:
                pass
    else:
                print(colored("Your input->","blue"))
                user_message = input()
                user_message.lower()
                if user_message == "vwqy":
                     engine.say("Activating Voice assistant Mode")
                     engine.runAndWait()
                     voice_mode = not voice_mode
                elif user_message == "light on" or user_message=="led on":
                     ardDat.write(str("1").encode())
                     message = "Turning on LED....\n"
                     coloured_message = colored(message,"yellow")
                     for i in coloured_message:
                          sys.stdout.write(i)
                          time.sleep(0.04)
                          sys.stdout.flush()
                     
                     time.sleep(5.4)
                elif user_message == "light off" or user_message == "led off":
                     ardDat.write(str("0").encode())
                     message = "Turning off LED....\n"
                     coloured_message = colored(message,"yellow")
                     for i in coloured_message:
                          sys.stdout.write(i)
                          time.sleep(0.04)
                          sys.stdout.flush()
                   
                     time.sleep(5.4)
                else:
                    user_input_url = f"{rasa_server_url}/webhooks/rest/webhook"
                    payload = {
                        "sender": conversation_id,
                        "message": user_message
                    }

                    response = requests.post(user_input_url, json=payload)
                    bot_responses = response.json()
                    print(colored("RASA->","green"))
                    for bot_response in bot_responses:
                        bot_response['text'] = bot_response['text'] + "\n"
                        for i in bot_response['text']:
                             sys.stdout.write(i)
                             time.sleep(0.04)
                             sys.stdout.flush()

