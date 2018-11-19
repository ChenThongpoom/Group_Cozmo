from __future__ import print_function
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
# from renametokensuccess1 import renametoken


# If modifying these scopes, delete the file token.json.
SCOPES = 'https://www.googleapis.com/auth/calendar.readonly'


myclient = pymongo.MongoClient("mongodb://localhost:27017/") 
tokendb = myclient["tokennames2"]
tokenname = tokendb["tokennames2"]
mydb = myclient["eventlist"]
mycol = mydb["eventlist"] 
tokenkey = {}


r = sr.Recognizer()                                                                                   
with sr.Microphone() as source:                                                                       
        print("Speak:")                                                                                   
        audio = r.listen(source)
user = []

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
        system("say hi what can I help you")
        audio = newspeech()
        if "free" in r.recognize_google(audio) and "time" in r.recognize_google(audio):
            return state2
        else:
            return state6

    def state2():
        system ("say okay tell me a username that available for this calendar")
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
        system ("say Are there any one else?")
        audio = newspeech()
        if "yes" in r.recognize_google(audio):
            print("You said " + r.recognize_google(audio))
            return state2
        else:
            return state4

    def state4():
        system("say what day do you want me to find your free time?")
        audio = newspeech()
        print(r.recognize_google(audio)) 
        str = r.recognize_google(audio)
        result= freetime.findSlot(user,re.sub(r"(?<=\d)(st|nd|rd|th)\b", '', str))
        print(result)
        for index, freeDay in enumerate(result):
            if index == 0:
                system('say your freetime is')
            if freeDay['start']['dateTime'][14:16] == '00' and freeDay['end']['dateTime'][14:16] == '00' :
                system('say '+freeDay['start']['dateTime'][11:13]+' Oclock to '+freeDay['end']['dateTime'][11:13]+' Oclock')
            elif freeDay['start']['dateTime'][14:16] == '00':
                system('say '+freeDay['start']['dateTime'][11:13]+' Oclock to '+freeDay['end']['dateTime'][11:13]+' Oclock and '+freeDay['end']['dateTime'][14:16]+' minutes ')
            elif freeDay['end']['dateTime'][14:16] == '00':
                system('say '+freeDay['start']['dateTime'][11:13]+' Oclock and '+freeDay['start']['dateTime'][14:16]+' minutes to '+freeDay['end']['dateTime'][11:13]+' Oclock')
            else:
                system('say '+freeDay['start']['dateTime'][11:13]+' Oclock and '+freeDay['start']['dateTime'][14:16]+' minutes to '+freeDay['end']['dateTime'][11:13]+' Oclock and '+freeDay['end']['dateTime'][14:16]+' minutes ')
            if index != len(result)-1:
                system('say next period is')
        
    def state5():
        system ("say This user is not available do you want me to add more user account?")
        audio = newspeech()
        if "yes" in r.recognize_google(audio):
            return state6
        else:
            return state2

    def state6():
        system("say what username do you want?")
        username = newspeech()
        print (r.recognize_google(username))
        return (renametoken(r.recognize_google(username)))


    def state7():
        system("say Do you want me to find your free time right?")
        audio = newspeech()
        if "yes" in r.recognize_google(audio):
            return state2
        else:
            system("so I cannot do this please try again")
            return state1
    
    def state8():
        system("say Account binded successfully")
        return state2
    
    

    def renametoken(username):

        store = file.Storage('token.json')
        creds = store.get()
        if not creds or creds.invalid:
            flow = client.flow_from_clientsecrets('credentials.json', SCOPES)
            creds = tools.run_flow(flow, store)
        service = build('calendar', 'v3', http=creds.authorize(Http()))

        x = tokenname.find()
        k = len( list(x) ) ##ดึง จน. ข้อมูลจาก db มา วัด
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

        

    state=state2   # initial state
    while state: state=state()  # launch state machine
    print ("Done with states")
            

except sr.UnknownValueError:
        print("Could not understand")
except sr.RequestError as e:
        print("Could not request results; {0}".format(e))

 
