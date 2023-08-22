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

    # pageraw=requests.get(link).text
    # page=BeautifulSoup(pageraw,"lxml")
    # page_nums=page.findAll("li",class_="page-item")[-2].text
    # page_nums=int(page_nums)

    event_infos=[]

    for index in range(1,6):#page_nums+1):#get pages
       
        print(index)
        link_paged=f"https://www.ankara.edu.tr/kategori/etkinlikler/page/{index}/"
        print(link_paged)
        events=findEvents(link_paged)
        for event in events:#get event details
            try:
                event_detail_link=event.a["href"]
                category=event.findAll("span")[1].text
                #get event details
                event_detail_page=requests.get(event_detail_link)
                event_detail_page.raise_for_status()
                event_detail=BeautifulSoup(event_detail_page.text,"lxml")
                heading=event_detail.find("h1",class_="single")
                if heading is None:
                    heading=""
                else:
                    heading=heading.text
                    heading=heading.replace("\r\n","").strip()
                print(heading)
                detail_part=event_detail.find("div",class_="content order-first order-sm-last col-12 col-md-9 col-lg-8")
                if detail_part is not None:
                    image=detail_part.find('img')
                    img_links=[]
                    if image is not None:
                        #for img in images:
                             img_src=image["data-src"]
                             img_links.append(img_src)
                    description=detail_part.p
                    if description is None:
                        description=""
                    else:
                        description=description.text
                    links=detail_part.findAll("a")
                    llinks=[event_detail_link]
                    if links is not None:
                        for l in links:
                             llinks.append(l["href"])
                    # dates=detail_part.findAll("div",class_="p-3 flex-md-fill")
                    # start_date=dates[0].strong.text
                    # start_date=datetime.strptime(start_date.replace(" ","")[0:16],"%d.%m.%Y-%H:%M")
                    # if len(dates)<2:
                    #     end_date=start_date
                    # else:
                    #     end_date=dates[1].strong.text
                    #     end_date=datetime.strptime(end_date.replace(" ","")[0:16],"%d.%m.%Y-%H:%M")
                    event_infos.append(
                        {
                            "name":heading,
                            "description":description,
                            "link":llinks,
                            "start_date":{},
                            "end_date":{},
                            "media":img_links,
                            "qr_code":{},
                            "verification_link":"",
                            "category":category,
                            "place":""
                        }
                    )
            except:
                print("invalid event link")
    return event_infos 

print(scrape())
        
