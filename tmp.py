from datetime import datetime
# for event in events:
#     date=event.span.text
#     if date!="":
#         date=getTime(date)

#     alink=event.a["href"]
#     category=
    
#     print(alink)


def getTime(time_str):
    months={
        "Ocak":1,
        "Şubat":2,
        "Mart":3,
        "Nisan":4,
        "Mayıs":5,
        "Haziran":6,
        "Temmuz":7,
        "Ağustos":8,
        "Eylül":9,
        "Ekim":10,
        "Kasım":11,
        "Aralık":12,
    }
    time=time_str.split(" ")
    day=int(time[0])
    month=months[time[1]]
    year=int(time[2])
    return datetime(year,month,day)