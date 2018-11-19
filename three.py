from __future__ import print_function
import datetime
from googleapiclient.discovery import build
from httplib2 import Http
from oauth2client import file, client, tools
from shutil import move
import os.path
import pymongo ##first code that I modified ##It is use to import the code from the pymongo library



myclient = pymongo.MongoClient("mongodb://localhost:27017/") 
tokendb = myclient["tokennames1"]
tokenname = tokendb["tokennames1"]
mydb = myclient["eventlist"]
mycol = mydb["eventlist"] ##these lines are use to start and choose the database that are use to append these information
d = {}
l = []
l2 = []

# If modifying these scopes, delete the file token.json.
SCOPES = 'https://www.googleapis.com/auth/calendar.readonly'

def renametoken():
    for j in tokenname.find():
        l2.append(j)

    for i in range(len(l2)):
        if os.path.isfile('token'+i+'.json'):
            ##a = audio.input ##ของมึงไอควาย
            x = tokenname.find()
            k = len( list(x) ) ##ดึง จน. ข้อมูลจาก db มา วัด
            token = 'token' + str(k) + '.json'
            rename = str('C:\\Users\\LENOVO\\Desktop\\Computer Innovation Engineering\\Freshman\\Fundamentals of Computer Programming\\CIEProject1\\'+token)
            move('C:\\Users\\LENOVO\\Desktop\\Computer Innovation Engineering\\Freshman\\Fundamentals of Computer Programming\\CIEProject1\\token.json', str(rename))
            ##d[a] = token
            tokenname.insert_one(d)
            print(x)
            print(k)
            print(token) 
            ## = tokenname.insert_one( { a : token } )

def main():
    for j in tokenname.find():
        l.append(j)
    print(l)
    for i in range(len(l)+1):
        accountno = str(i)
        i = str(i)
        j = "token" + i + ".json"  ## leads to different json file resulting into event inputs from different account
        store = file.Storage(j)
        creds = store.get()
        if not creds or creds.invalid:
            flow = client.flow_from_clientsecrets('credentials.json', SCOPES)
            creds = tools.run_flow(flow, store)
        service = build('calendar', 'v3', http=creds.authorize(Http()))

        # Call the Calendar API
        now = datetime.datetime.utcnow().isoformat() + 'Z' # 'Z' indicates UTC time
        print('Getting the upcoming events within today from account number '+ accountno)
        events_result = service.events().list(calendarId='primary', timeMin=now, singleEvents=True,
                                            orderBy='startTime', timeZone="utc").execute()
        events = events_result.get('items', [])

        if not events:
            print('No upcoming events found.')
        for event in events:
            start = event['start'].get('dateTime', event['start'].get('date'))
            end = event['end'].get('dateTime', event['end'].get('date'))
            x = mycol.insert_one(event)   ##for every events that is found within the next 10 events it will be added into the database
            print(event)
            print(event['summary'])    
            print(x) ##print the commands that shows the addition of information into the database
            print(myclient.list_database_names())


if __name__ == '__main__':
    renametoken()
    main()
