from datetime import datetime, timedelta
import dateutil.parser
from renametokensuccess1 import main
import arrow # convert datetime string to datetime object
from intersect import intersection

def findSlot(users,date):
    # day = date
    today = datetime.today()
    date = date.split(" ")
    if len(date) == 1:
        tstart = datetime.strptime(str(today.year)+'-'+str(today.month)+'-'+ date[0] +" 08:00:00", "%Y-%B-%d %H:%M:%S")
        tstop = datetime.strptime(str(today.year)+'-'+str(today.month)+'-'+ date[0] +" 23:59:59", "%Y-%B-%d %H:%M:%S")
    elif len(date) == 2:
        tstart = datetime.strptime(str(today.year)+'-'+ date[1]+'-'+date[0] +' 08:00:00', '%Y-%B-%d %H:%M:%S')
        tstop = datetime.strptime(str(today.year)+'-'+ date[1]+'-'+date[0] +' 23:59:59', '%Y-%B-%d %H:%M:%S')
    else:
        tstart = datetime.strptime(date[2]+'-'+date[1]+'-'+date[0] +' 08:00:00', '%Y-%B-%d %H:%M:%S')
        tstop = datetime.strptime(date[2]+'-'+date[1]+'-'+date[0] +' 23:59:59', '%Y-%B-%d %H:%M:%S')

    # Time format
    # appointments = ([
    #     {
    #         'start' : datetime.strptime('08:30:00', '%H:%M:%S'),
    #         'end' : datetime.strptime('10:00:00', '%H:%M:%S')
    #     }
    # ])
    user_freeTime = []
    # appointments = []
    # appointments.append(main(user, date))
    appointments = main(users,date)
    # for idx, i in enumerate (appointments):
    #     for j in i:
    #         print(idx)
    #         print(j['start'])
    #         print(j['end'])
    # print(appointments)
    # print(len(appointments))
    for user in appointments:
        free_time = []
        # print(user)
        tp = [(tstart , tstart)]
        for t in user:
            tstart2 = convertDatetime(t['start']['dateTime'])  #call convertDatetime function to convert string in the dict to dateTime object
            tend = convertDatetime(t['end']['dateTime'])
            tp.append( ( tstart2 , tend ) )
        tp.append( (tstop , tstop) )
        # print(tp)
        for i,v in enumerate(tp):
            if i > 0:
                if (tp[i][0] - tp[i-1][1]) > timedelta(minutes=30):  #check the freetime that should be more than 30 minutes
                    tf_start = tp[i-1][1]
                    delta = tp[i][0] - tp[i-1][1]
                    tf_end = tf_start + delta
                    free_time.append( (dict(start=(dict(dateTime=tf_start.strftime("%Y-%m-%dT%H:%M:%S"))),end=(dict(dateTime=tf_end.strftime("%Y-%m-%dT%H:%M:%S"))))) )
        user_freeTime.append(free_time)
    # print(user_freeTime)
    # print()
    print(intersection(user_freeTime))
    return intersection(user_freeTime)[0]
        # return intersection(user_freeTime)
        # return free_time
   # for tp in free_time:
   #     print (tp)                                                                                                                                                                                                                                                                                                                         ```````             `````````````````````````````````````````

def convertDatetime(date):
    date = arrow.get(date)
    dateObj = date.datetime
    dateObj = dateObj.replace(tzinfo=None) #remove time zone (+7)
    dateStr = dateObj.isoformat(' ') #remove T
    return dateutil.parser.parse(dateStr)

# findSlot(['gun','boom'], "22 November")