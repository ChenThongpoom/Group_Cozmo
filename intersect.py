# user1 = [{
#     "start": {
#             "dateTime": "2018-10-19T14:00:00+07:00"
#         },
#         "end": {
#             "dateTime": "2018-10-19T15:00:00+07:00"
#         }},
#         {"start": {
#             "dateTime": "2018-10-19T15:00:00+07:00"
#         },
#         "end": {
#             "dateTime": "2018-10-19T16:00:00+07:00"
#         }}
# ]
# user2 = [{
#     "start": {
#             "dateTime": "2018-10-19T14:30:00+07:00"
#         },
#         "end": {
#             "dateTime": "2018-10-19T16:30:00+07:00"
#         }}
# ]
# user3 = [{
#     "start": {
#             "dateTime": "2018-10-19T14:00:00+07:00"
#         },
#         "end": {
#             "dateTime": "2018-10-19T16:00:00+07:00"
#         }},
#         {"start": {
#             "dateTime": "2018-10-19T15:30:00+07:00"
#         },
#         "end": {
#             "dateTime": "2018-10-19T15:45:00+07:00"
#         }}
# ]
def intersection(lst):
    intersect = []
    # print(lst)
    # print(len(lst))
    if len(lst) == 1:
        return lst
    else:
        for eventUser1 in lst[0]:
            for eventUser2 in lst[1]:
                ts1_start, ts1_end, ts2_start, ts2_end = "", "", "", ""
                if eventUser1['start']['dateTime'] <= eventUser2['start']['dateTime']:
                    ts1_start, ts1_end = eventUser1['start']['dateTime'], eventUser1['end']['dateTime']
                    ts2_start, ts2_end = eventUser2['start']['dateTime'], eventUser2['end']['dateTime']
                else: 
                    ts2_start, ts2_end = eventUser1['start']['dateTime'], eventUser1['end']['dateTime']
                    ts1_start, ts1_end = eventUser2['start']['dateTime'], eventUser2['end']['dateTime']

                if ts1_end > ts2_start:
                    if ts1_end <= ts2_end:
                        intersect.append(dict(start=(dict(dateTime=ts2_start)), end=(dict(dateTime=ts1_end))))
                    else:
                        intersect.append(dict(start=(dict(dateTime=ts2_start)), end=(dict(dateTime=ts2_end))))
        lst[0] = intersect
        lst.pop(1)
        return intersection(lst)
            


            # if eventUser1['start']['dateTime'] <= eventUser2['start']['dateTime'] and eventUser2['start']['dateTime'] <= eventUser1['end']['dateTime']:
            #     intersect.append(dict(start=(dict(dateTime=(eventUser2['start']['dateTime']))), end =(dict(dateTime=(eventUser1['end']['dateTime'])))))
            # elif eventUser2['start']['dateTime'] <= eventUser1['start']['dateTime'] and eventUser1['end']['dateTime'] <= eventUser2['end']['dateTime']:
            #     intersect.append(dict(start=(dict(dateTime=(eventUser1['start']['dateTime']))), end=(dict(dateTime=(eventUser1['end']['dateTime'])))))
            # elif eventUser1['start']['dateTime'] <= eventUser2['start']['dateTime'] and eventUser2['end']['dateTime'] <= eventUser1['end']['dateTime']:
            #     intersect.append(dict(start=(dict(dateTime=(eventUser2['start']['dateTime']))), end=(dict(dateTime=(eventUser2['end']['dateTime'])))))
            # elif eventUser2['start']['dateTime'] <= eventUser1['start']['dateTime'] and eventUser1['start']['dateTime'] <= eventUser2['end']['dateTime']:
            #     intersect.append(dict(start=(dict(dateTime=(eventUser1['start']['dateTime']))), end=(dict(dateTime=(eventUser2['end']['dateTime'])))))
    # return intersect


# def union(user1,user2):
#     user1.extend(user2)
#     return user1