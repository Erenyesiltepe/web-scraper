from bs4 import BeautifulSoup
import requests
from datetime import datetime

def findEvents(link):
    pageraw=requests.get(link).text
    page=BeautifulSoup(pageraw,"lxml")
    events=page.find("div",class_="row row-cols-md-5 my-3")
    #print(events.prettify)
    events=events.find_all("div",class_="col")
    return events

def ankara():

    link="https://www.ankara.edu.tr/kategori/etkinlikler/"

    pageraw=requests.get(link).text
    page=BeautifulSoup(pageraw,"lxml")
    page_nums=page.findAll("li",class_="page-item")[-2].text
    page_nums=int(page_nums)

    event_infos=[]

    for index in range(1,page_nums+1):#get pages
        link_paged=f"https://www.ankara.edu.tr/kategori/etkinlikler/page/{index}/"
        events=findEvents(link_paged)
        for event in events:#get event details

            event_detail_link=event.a["href"]
            category=event.findAll("span")[1].text

            #get event details
            event_detail_page=requests.get(link).text
            event_detail=BeautifulSoup(event_detail_page,"lxml")

            heading=event_detail.find("h1",class_="single")
            detail_part=event_detail.find("div",class_="row justify-content-center my-4")
            images=detail_part.findAll("img")
            img_links=[]
            for img in images:
                 img_links.append(img["src"])

            dates=detail_part.findAll("div",class_="p-3 flex-md-fill")
            start_date=dates[0].strong.text
            end_date=dates[1].strong.text

            event_infos.append(
                {
                    "heading":heading,
                    "start_date":start_date,
                    "end_date":end_date,
                    "category":category,
                    "images":images,
                    "event_details":event_detail_link,
                    #no place added
                }
            )
    return {"ankara":event_infos} 

print(ankara())
        
