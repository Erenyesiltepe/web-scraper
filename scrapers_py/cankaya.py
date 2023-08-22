 
from bs4 import BeautifulSoup
import requests
from datetime import datetime
import re
 
def getTime(time_str):
    months={
        "OCAK":1,
        "ŞUBAT":2,
        "MART":3,
        "NİSAN":4,
        "MAYIS":5,
        "HAZİRAN":6,
        "TEMMUZ":7,
        "AĞUSTOS":8,
        "EYLÜL":9,
        "EKİM":10,
        "KASIM":11,
        "ARALIK":12,
    }
    numbers=re.findall(r"\d+",time_str)
    day=int(numbers[0])
    month_str=re.findall(r"[^0-9]+",time_str)[0]
    month=months[month_str.upper()]
    year=int(numbers[1])
 
    return datetime(year,month,day)

 
def get_detail_page_links():
    link="https://kultur.cankaya.edu.tr/event/"
    pageraw=requests.get(link).text
    page=BeautifulSoup(pageraw,"lxml")
    links=page.find("div",class_="factory-blog factory-blog-grid").findAll("a")
    ref_links=[]
    length=len(links)
    if length<60:
        for link in links:
            ref_links.append(link["href"])
    else:
        for a in range(60):
            ref_links.append(links[a]["href"])
    print(ref_links)
    return ref_links

 
def get_event_details(link):
    pageraw=requests.get(link).text
    page=BeautifulSoup(pageraw,"lxml")
    heading=page.h1.text
    cankslider=page.find(id="cankSlider")
    image=cankslider.img["src"]
    time_str=cankslider.time.text.strip().replace("\n","").replace(" ","")
    final_date=getTime(time_str)
    description=cankslider.findAll("p")[1].text
    return {
            "name":heading,
            "description":description,
            "link":link,
            "start_date":final_date,
            "end_date":final_date,
            "media":[image],
            "qr_code":{},
            "verification_link":"",
            "category":"",
            "place":""
            }

def scrape():
    links=get_detail_page_links()
    details=[]
    for link in links:
        details.append(
            get_event_details(link)
        )
    return details

print(scrape())
