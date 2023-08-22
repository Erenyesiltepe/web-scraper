 
from bs4 import BeautifulSoup
import requests
from datetime import datetime

 
def find_events(link):
    
    pageraw=requests.get(link).text
    page=BeautifulSoup(pageraw,"lxml")

    container=page.find("div",class_="view-content")
    if container!=None:
        events=container.findAll("span",class_="field-content")
        return events
    else:
        return container ## container is none

 
def return_links(events):
    links=[]
    for event in events:
        relative_link=event.a["href"]
        abs_link="https://kkm.metu.edu.tr"+relative_link
        links.append(abs_link)
    return links

 
def get_event_details(event_link):
    event_page_raw=requests.get(event_link).text
    event_page=BeautifulSoup(event_page_raw,"lxml")

    heading=event_page.find("h4",class_="page-title").text
    #print(heading)
    main_content=event_page.find(id="maincontent")
    images=main_content.find_all("img")
    img_links=[]
    for image in images:
        img_links.append(image["src"])

    spans=main_content.findAll("span")

    print(spans[0].text)
    dates=spans[0].text.strip().replace("\n","")
    if "·" in dates:
        dates=dates.split("·")

        dates[0]=dates[0].replace("\n","").strip()
        dates[1]=dates[1].replace("\n","").strip()

        start=(dates[0][0:10]+" "+dates[0][-5::]).replace("\n","").strip()
        end=(dates[1][0:10]+" "+dates[1][-5::]).replace("\n","").strip()
    else:
        start=end=dates

    start=datetime.strptime(start,"%d/%m/%Y %H:%M")
    end=datetime.strptime(end,"%d/%m/%Y %H:%M")

    place="ODTÜ"+spans[1].text+" "+spans[2].text

    return {
        "name":heading,
        "description":"",
        "link":event_link,
        "start_date":start,
        "end_date":end,
        "media":img_links,
        "qr_code":{},
        "verification_link":"",
        "category":"",
        "place":place,
     }

def scrape():
    link="https://kkm.metu.edu.tr/calendar-node-field-etkinlik-tarihi/year/{}?page=0"

    event_details=[]
    this_year=datetime.now().year

    this_year_events=find_events(link.format(this_year))
    this_year_links=[]
    if this_year_events!=None:
        this_year_links=return_links(this_year_events)
    
    for event_link in this_year_links:
        print(event_link)
        event_details.append(
            get_event_details(event_link)
        )
    
    next_year_events=find_events(link.format(this_year+1))
    if next_year_events!=None:
        next_year_events=return_links(next_year_events)
        for event_link in next_year_events:
            event_details.append(
                get_event_details(event_link)
            )

    return event_details

print(scrape())