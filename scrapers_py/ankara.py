from bs4 import BeautifulSoup
import requests
from datetime import datetime

def findEvents(link):
    pageraw=requests.get(link).text
    page=BeautifulSoup(pageraw,"lxml")
    events=page.find("div",class_="row row-cols-md-5 my-3")
    events=events.find_all("div",class_="col")
    return events

def scrape():

    link="https://www.ankara.edu.tr/kategori/etkinlikler/"

    pageraw=requests.get(link).text
    page=BeautifulSoup(pageraw,"lxml")
    page_nums=page.findAll("li",class_="page-item")[-2].text
    page_nums=int(page_nums)

    event_infos=[]

    for index in range(1,page_nums+1):#get pages
        link_paged=f"https://www.ankara.edu.tr/kategori/etkinlikler/page/{index}/"
        print(link_paged)
        events=findEvents(link_paged)
        for event in events:#get event details

            event_detail_link=event.a["href"]
            category=event.findAll("span")[1].text

            #get event details
            event_detail_page=requests.get(event_detail_link).text
            event_detail=BeautifulSoup(event_detail_page,"lxml")

            heading=event_detail.find("h1",class_="single")
            if heading is None:
                heading=""
            else:
                heading=heading.text
                heading=heading.replace("\r\n","").strip()
            print(heading)
            
            detail_part=event_detail.find("div",class_="row justify-content-center my-4")
            if detail_part is not None:
                images=detail_part.findAll('img',{"src":True})
                img_links=[]
                if images is not None:
                    for img in images:
                         img_links.append(img["src"])

                description=detail_part.p
                if description is None:
                    description=""
                else:
                    description=description.text

                dates=detail_part.findAll("div",class_="p-3 flex-md-fill")
                start_date=dates[0].strong.text
                start_date=datetime.strptime(start_date.replace(" ",""),"%d.%m.%Y-%H:%M")
                if len(dates)<2:
                    end_date=start_date
                else:
                    end_date=dates[1].strong.text
                    end_date=datetime.strptime(end_date.replace(" ",""),"%d.%m.%Y-%H:%M")

                event_infos.append(
                    {
                        "name":heading,
                        "description":description,
                        "link":event_detail_link,
                        "start_date":start_date,
                        "end_date":end_date,
                        "media":images,
                        "qr_code":{},
                        "verification_link":"",
                        "category":category,
                        "place":""
                    }
                )
    return event_infos 

print(scrape())
        
