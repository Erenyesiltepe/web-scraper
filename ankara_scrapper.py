from bs4 import BeautifulSoup
import requests
from datetime import datetime

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

def findEvents(link):
    pageraw=requests.get(link).text
    page=BeautifulSoup(pageraw,"lxml")
    events=page.find("div",class_="row row-cols-md-5 my-3")
    #print(events.prettify)
    events=events.find_all("div",class_="col")
    return events

link="https://www.ankara.edu.tr/kategori/etkinlikler/"
events=findEvents(link)

flag=True
page=1

for event in events:
    date=event.span.text
    if date!="":
        date=getTime(date)

    alink=event.a["href"]
    category=
    
    print(alink)
    
