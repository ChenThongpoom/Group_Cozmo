from __future__ import print_function
import cozmo
import speech_recognition as sr           
import freetime
import re 
import calendar    
from datetime import datetime 
import three
import datetime
from googleapiclient.discovery import build
from httplib2 import Http
from oauth2client import file, client, tools
from shutil import move
import os.path
import pymongo
from httplib2 import Http

# If modifying these scopes, delete the file token.json.
SCOPES = 'https://www.googleapis.com/auth/calendar.readonly'


myclient = pymongo.MongoClient("mongodb://localhost:27017/") 
tokendb = myclient["tokennames2"]
tokenname = tokendb["tokennames2"]
mydb = myclient["eventlist"]
mycol = mydb["eventlist"] 
tokenkey = {}
user = []

def cozmo_program(robot: cozmo.robot.Robot):
    r = sr.Recognizer()                                                                                   
    with sr.Microphone() as source:                                                                       
        print("Speak:")                                                                                   
        audio = r.listen(source)
    # user = []

    try:
        from os import system
        from pymongo import MongoClient
        client2 = MongoClient('localhost', 27017)
        db = client2.event
        collection = db.user 
        print("You said " + r.recognize_google(audio))

        def newspeech():
            r = sr.Recognizer()                                                                                   
            with sr.Microphone() as source:                                                                       
                print("Speak:")                                                                                   
                audio = r.listen(source)
            return audio

        def state0():
            if r.recognize_google(audio) == "hi":
                return state1
            else:
                return state1
        def state1():
            robot.say_text("hi what can I help you?").wait_for_completed()
            audio = newspeech()                                                                                
            print (r.recognize_google(audio))
            if "free" in r.recognize_google(audio) and "time" in r.recognize_google(audio):
                return state2
            else:
                return state7

        def state2():
            robot.say_text("okay tell me an username that available with this calendar ").wait_for_completed()
            audio = newspeech()
            global user
            a = r.recognize_google(audio)
            print (r.recognize_google(audio))
            if  tokenname.find_one({"username": a}):
                user.append(a)
                return state3
            else:
                return state5

        def state3():
            robot.say_text("Are there any one else?").wait_for_completed()
            audio = newspeech()
            if "yes" in r.recognize_google(audio):
                print("You said " + r.recognize_google(audio))
                return state2
            else:
                return state4

        def state4():
            robot.say_text("on what day do you want to find your free time?").wait_for_completed()
            audio = newspeech()
            print(r.recognize_google(audio)) 
            str = r.recognize_google(audio)
            result= freetime.findSlot(user,re.sub(r"(?<=\d)(st|nd|rd|th)\b", '', str))
            for index, freeDay in enumerate(result):
                if index == 0:
                    robot.say_text('your freetime is').wait_for_completed()
                if freeDay['start']['dateTime'][14:16] == '00' and freeDay['end']['dateTime'][14:16] == '00' :
                    robot.say_text(freeDay['start']['dateTime'][11:13]+' Oclock to '+freeDay['end']['dateTime'][11:13]+' Oclock').wait_for_completed()
                elif freeDay['start']['dateTime'][14:16] == '00':
                    robot.say_text(freeDay['start']['dateTime'][11:13]+' Oclock to '+freeDay['end']['dateTime'][11:13]+' Oclock and '+freeDay['end']['dateTime'][14:16]+' minutes ').wait_for_completed()
                elif freeDay['end']['dateTime'][14:16] == '00':
                    robot.say_text(freeDay['start']['dateTime'][11:13]+' Oclock and '+freeDay['start']['dateTime'][14:16]+' minutes to '+freeDay['end']['dateTime'][11:13]+' Oclock').wait_for_completed()
                else:
                    robot.say_text(freeDay['start']['dateTime'][11:13]+' Oclock and '+freeDay['start']['dateTime'][14:16]+' minutes to '+freeDay['end']['dateTime'][11:13]+' Oclock and '+freeDay['end']['dateTime'][14:16]+' minutes ').wait_for_completed()
                if index != len(result)-1:
                    robot.say_text('next period is').wait_for_completed()
            return state9

        def state5():
            robot.say_text("This user is not available do you want me to add more?").wait_for_completed()
            audio = newspeech()
            if "yes" in r.recognize_google(audio):
                print("You said " + r.recognize_google(audio))
                return state6
            else:
                return state2

        def state6():
            robot.say_text("please tell your username and register").wait_for_completed()
            username = newspeech()
            print (r.recognize_google(username))
            return (renametoken(r.recognize_google(username)))


        def state7():
            robot.say_text("Do you want me to find your free time right?").wait_for_completed()
            audio = newspeech()
            if "yes" in r.recognize_google(audio):
                return state2
            else:
                robot.say_text("so I cannot do this please try again").wait_for_completed()
                return state1
    
        def state8():
            robot.say_text("Account binded successfully").wait_for_completed()
            return state2

        
        def renametoken(username):
            store = file.Storage('token.json')
            creds = store.get()
            if not creds or creds.invalid:
                flow = client.flow_from_clientsecrets('credentials.json', SCOPES)
                creds = tools.run_flow(flow, store)
            service = build('calendar', 'v3', http=creds.authorize(Http()))

            x = tokenname.find()
            k = len( list(x) ) 
            token = 'token' + str(k) + '.json'
            rename = str('/Users/srboomc/Documents/fundamentals of programming/project'+token)
            move('/Users/srboomc/Documents/fundamentals of programming/project/token.json', str(rename))
            # print(token)
            username = str(username)
            tokenkey = { 'username' : username ,
                        'token' : token }
            # print(tokenkey)
            tokenname.insert_one(tokenkey)
            return state8  

        def state9():
            robot.say_text("thats all for your free time").wait_for_completed()
            

        state=state0   # initial state
        while state: state=state()  # launch state machine
        print ("Done with states")
            

    except sr.UnknownValueError:
        robot.say_text("Could not understand").wait_for_completed
    except sr.RequestError as e:
        print("Could not request results; {0}".format(e))
cozmo.run_program(cozmo_program)