import speech_recognition as sr
import pyttsx3

import os 
import datetime
import webbrowser
import pywhatkit as wk
import pyautogui
import sys
import requests

import openai
from apikey import api_data
openai.api_key = api_data

#function to convert text to speech 
def SpeakText(command) :
    engine = pyttsx3.init()
    voices = engine.getProperty('voices')
    engine.setProperty(voices[0].id)
    engine.setProperty('rate', 150)
    engine.say(command)
    engine.runAndWait()

def wishMe() :
    hour = int(datetime.datetime.now().hour)
    if hour >= 0 and hour < 12 :
        SpeakText('Good Morning!')
    elif hour >= 12 and hour < 18 :
        SpeakText('Good Afternoon!')
    else :
        SpeakText('Good Evening!')

    SpeakText('Ready to comply. What can I do for you today?')

#initialize the recognizer 
r = sr.Recognizer()

#function to take user voice input
def RecordText() :
    #loop in case of errors
    while(1) :
        try :
            #use the microphone as source for input 
            with sr.Microphone() as source2 :
                #prepare recognizer to receive input
                r.adjust_for_ambient_noise(source2, duration=0.2)
                print("I'm listening...")
                r.pause_threshold = 0.5
                #listens to the user for input 
                audio2 = r.listen(source2)
                #using google to recognize audio 
                MyText = r.recognize_google(audio2, langauge="en-in")

                return MyText

        except sr.RequestError as e :
            print("Could not request results: {0}".format(e))

        except sr.UnknownValueError :
            print("Unknown error occured")

def send_to_chatGPT(messages, model="gpt-3.5-turbo") :
    response = openai.ChatCompletion.create(
        model=model,
        messages=messages,
        max_tokens=100,
        n=1,
        stop=None,
        temperature=0.5,
    )

    message = response.choices[0].message.content
    messages.append(response.choices[0].message)
    return message

if __name__ == '__main__' :
    messages = []               #to keep track of the entire conversation
    while(1) :
        wishMe()
        text = RecordText()

        # desktop assistant functions
        if 'jarvis' in text :
            print("Hello, I am Jarvis AI. How may I assist you?")
            SpeakText("Hello, I am Jarvis A.I. How may I assist you?")

        elif 'just open google' in text :             
                webbrowser.open('https://google.com')

        elif 'just open youtube' in text :             
            webbrowser.open('https://youtube.com')

        elif 'open youtube' in text :              
            ("What would you like to watch?")
            query = RecordText.lower()
            wk.playonyt(f"{query}")
                
        elif 'search on youtube' in text :             
            text = text.replace("search on youtube", "")
            webbrowser.open("www.youtube.com/results?search_text={text}")

        elif 'close browser' in text :             
            os.system("taskfill /f /im chrome.exe")

        elif 'what is my ip address' in text :             
            SpeakText("Checking")
            try :
                ipAdd = requests.get('https://api.ipify.org').text
                print(ipAdd)
                SpeakText("your IP address is")
                SpeakText(ipAdd)
            except Exception as e :
                SpeakText("Network connection interrupted. Please try again later")

        elif 'volume up' in text :             
            pyautogui.press("volumeup")
            pyautogui.press("volumeup")
            pyautogui.press("volumeup")
            pyautogui.press("volumeup")
            pyautogui.press("volumeup")
            pyautogui.press("volumeup")
            pyautogui.press("volumeup")
            pyautogui.press("volumeup")
            pyautogui.press("volumeup")
            pyautogui.press("volumeup")

        elif 'volume down' in text :             
            pyautogui.press("volumedown")
            pyautogui.press("volumedown")
            pyautogui.press("volumedown")
            pyautogui.press("volumedown")
            pyautogui.press("volumedown")
            pyautogui.press("volumedown")
            pyautogui.press("volumedown")
            pyautogui.press("volumedown")
            pyautogui.press("volumedown")
            pyautogui.press("volumedown")

        elif 'mute' or 'unmute' in text :             
            pyautogui.press("volumemute")

        elif 'go to sleep' in text :
            SpeakText("Alright then, I am switching off. Good bye.")
            sys.exit()

        # search text via chatgpt
        messages.append({'role': 'user', 'content' : text})
        response = send_to_chatGPT(messages)
        SpeakText(response)
        print(response)

