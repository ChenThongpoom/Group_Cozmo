from __future__ import print_function
import datetime
from googleapiclient.discovery import build
from httplib2 import Http
from oauth2client import file, client, tools
from shutil import move
import os.path
import pymongo ##first code that I modified ##It is use to import the code from the pymongo library



myclient = pymongo.MongoClient("mongodb://localhost:27017/") 
tokendb = myclient["tokennames2"]
tokenname = tokendb["tokennames2"]
mydb = myclient["eventlist"]
mycol = mydb["eventlist"] ##these lines are use to start and choose the database that are use to append these information
listoftoken = []
tokenkey = {}             

# If modifying these scopes, delete the file token.json.
SCOPES = 'https://www.googleapis.com/auth/calendar.readonly'
day = {}

def time(D):
    # D = D.split(" ")
    today = datetime.datetime.today()
    numMonth = datetime.datetime.strptime(D[1], '%B')
    if len(D) == 1:
        timeMin = (str(today.year)+'-'+str(today.month)+'-'+D[0]+'T01:00:00Z')
        timeMax = (str(today.year)+'-'+str(today.month)+'-'+D[0]+'T16:59:59Z')
    elif len(D) == 2:
        timeMin = (str(today.year)+'-'+str(numMonth.month)+'-'+D[0]+'T01:00:00Z')
        timeMax = (str(today.year)+'-'+str(numMonth.month)+'-'+D[0]+'T16:59:59Z')
    else:
        timeMin = (D[2]+'-'+str(numMonth.month)+'-'+D[0]+'T01:00:00Z')
        timeMax = (D[2]+'-'+str(numMonth.month)+'-'+D[0]+'T16:59:59Z')
    return timeMin,timeMax



def renametoken(username):
    x = tokenname.find()
    k = len( list(x) ) ##ดึง จน. ข้อมูลจาก db มา วัด
    token = 'token' + str(k) + '.json'
    rename = str('/Users/srboomc/Documents/fundamentals of programming/project'+token)
    move('/Users/srboomc/Documents/fundamentals of programming/project/token.json', str(rename))
    # print(token)
    tokenkey = { 'username' : username ,
                 'token' : token }
    # print(tokenkey)
    tokenname.insert_one(tokenkey)
    # print(tokenname)

def main(user, day):
    userEvents = []
    # print(user)
    # print(day)
    # print(len(list(tokenname.find())))
    for i in range(len(list(tokenname.find()))):
        account = tokenname.find()
        if account[i]['username'] in user:
            token = account[i]['token']
            store = file.Storage(token)
            creds = store.get()
            if not creds or creds.invalid:
                flow = client.flow_from_clientsecrets('credentials.json', SCOPES)
                creds = tools.run_flow(flow, store)
            service = build('calendar', 'v3', http=creds.authorize(Http()))

            timeMin, timeMax = time(day)
            # print(timeMin, timeMax)
            # Call the Calendar API
            now = datetime.datetime.utcnow().isoformat() + 'Z' # 'Z' indicates UTC time
            # print('Getting the upcoming events within today from account number ')
            events_result = service.events().list(calendarId='primary', timeMin=timeMin, timeMax= timeMax, singleEvents=True,
                                                orderBy='startTime', timeZone=None).execute()
            events = events_result.get('items', [])

            if not events:
                print('No upcoming events found.')
            userEvents.append(events)
            # print(events)
            # for event in events:
            #     start = event['start'].get('dateTime', event['start'].get('date'))
            #     end = event['end'].get('dateTime', event['end'].get('date'))
            #     x = mycol.insert_one(event)   ##for every events that is found within the next 10 events it will be added into the database
                
                # print(event)
                # print(event['summary'])    
                # print(x) ##print the commands that shows the addition of information into the database
                # print(myclient.list_database_names())
    return userEvents
    # return events


# if __name__ == '__main__':
#     main(user)

