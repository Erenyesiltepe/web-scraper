from datetime import datetime
import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse, parse_qs
import time
import random
def calc_run_time(func):
    def wrapper(*args, **kwargs):
        start_time=time.time()
        res=func(*args, **kwargs)
        end_time=time.time()
        print("Runned in seconds:",end_time-start_time)
        return res
    return wrapper
def get_parsed(link,payload="",method="GET"):
    agents=[
        "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Ubuntu Chromium/37.0.2062.94 Chrome/37.0.2062.94 Safari/537.36",
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.85 Safari/537.36",
        "Mozilla/5.0 (Windows NT 6.1; WOW64; Trident/7.0; rv:11.0) like Gecko",
        "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:40.0) Gecko/20100101 Firefox/40.0",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_5) AppleWebKit/600.8.9 (KHTML, like Gecko) Version/8.0.8 Safari/600.8.9",
        "Mozilla/5.0 (iPad; CPU OS 8_4_1 like Mac OS X) AppleWebKit/600.1.4 (KHTML, like Gecko) Version/8.0 Mobile/12H321 Safari/600.1.4",
        "Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.85 Safari/537.36",
        "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.85 Safari/537.36",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.135 Safari/537.36 Edge/12.10240",
        "Mozilla/5.0 (Windows NT 6.3; WOW64; rv:40.0) Gecko/20100101 Firefox/40.0"
    ]
    headersList = {
    "Accept": "*/*",
     "User-Agent": random.choice(agents)
    }   
    response = requests.request(method, link, data=payload,  headers=headersList)
    soup=BeautifulSoup(response.text,"lxml")
    return soup
def get_event_links(event_type="tiyatro"):
    base_link="https://biletinial.com/tr-tr/"+event_type+"/"
    soup=get_parsed(base_link)
    match event_type:
        case "etkinlikleri/stand-up":
             lists=soup.select(".resultsGrid a")
             event_links=["https://biletinial.com"+a.get("href") for a in set(lists)]
        case _:
             lists=soup.select(".kategori__etkinlikler ul li figure a")
             event_links=["https://biletinial.com"+a.get("href") for a in set(lists)]
    
    return event_links
def get_prices(seance_id):
    #create request
    reqUrl = "https://biletinial.com/tr-tr/tiyatro/koltuk_secimi"
    payload = f'seanceId={seance_id}&IsUser=1'
    soup=get_parsed(reqUrl,payload,"POST")

    ticket_details=[]
    tickets=soup.select("div.yiyecek-oner__fiyat__adet")# no seats
    if len(tickets)==0:#no seats
        tickets =soup.select(".prices .item")
        for ticket in tickets:
            type = ticket.find("small").text.strip()
            price = ticket.find("strong").text
            price = float(price.strip()[0:-2].replace(",","."))
            ticket_details.append({"type":type,"price":price})
    else:#seated
        for ticket in tickets:
            type =  ticket.get("data-tickettype")
            price = float(ticket.get("data-ticketprice"))
            ticket_details.append({"type":type,"price":price})
    return ticket_details
def get_place(link):
     # Parse the URL
    parsed_url = urlparse(link)

    # Extract the query parameters
    query_params = parse_qs(parsed_url.query)

    # Extract the latitude and longitude
    if 'q' in query_params:
        coordinates = query_params['q'][0].split(',')
        latitude = float(coordinates[0])
        longitude = float(coordinates[1])
        return latitude, longitude
    else:
        return None   
@calc_run_time
def get_event_details(link,category):
    soup = get_parsed(link)

    try:
        heading = soup.find("h1").text
        print(heading)
        img = soup.select("img.eventPoster")[0]
        img_link = img.get("src")
        desc = soup.select("div.tabContent.flex.directionColumn")[0].text
        rules = soup.select("div.tabContent.row")[0].text
        different_dates = soup.select("div.ed-biletler__sehir__gun")
    except:
        print("Event page could not be loaded")
        return []

    pre = {"title":"", "lng":-1, "lat":-1}
    base= {
            "name":heading,
            "description":desc.replace("\n"," ").replace("\r"," ").replace("\xa0"," "),
            "rules":rules.replace("\n"," ").replace("\r"," ").replace("\xa0"," "),
            "links":link,
            "media":[img_link],
            "category":category.lower()
        }
    places=[]
    for date in different_dates:
        try:
            seance_btn=date.select("button.seanceSelect")[0]
            ifsold = seance_btn.text
            if ifsold[0] == "B":
                start_date_str = date.find('time', attrs={'itemprop': 'startDate'})
                start_date=start_date_str.get("content")
                start_date = datetime.strptime(start_date, "%Y-%m-%dT%H:%M")
                end_date = date.find('meta', attrs={'itemprop': 'endDate'}).get("content")
                end_date = datetime.strptime(end_date, "%Y-%m-%dT%H:%M")

                address_part = soup.find('a', attrs={'itemprop': 'location'})
                address_title= address_part.get("title")

                try:
                    if address_title != pre["title"]:
                        address_link = address_part.get("href")
                        address_page = get_parsed("https://biletinial.com"+address_link)
                        address_raw = address_page.select(".yeniMekan__sayfalar__iletisim__harita iframe")[0].get("src")
                        latitude, longitude=get_place(address_raw)

                    
                    places.append(
                       {
                           "place_name":address_title,
                            "start_date":start_date.strftime("%d-%m-%Y %H:%M"),
                            "end_date":end_date.strftime("%d-%m-%Y %H:%M"),
                            "latitude":latitude,
                            "longitude":longitude,
                            "vendors":[
                                {
                                    "name":"biletinial",
                                    "prices":get_prices(seance_btn.get("data-title"))
                                }
                            ]
                        }
                    )
                except:
                    print("Event location could not found:",address_title)
        except:
            print("Event dates could not found")

    return {
        **base,
        "vendors":places
    }   
@calc_run_time
def scrape_site():
    categories=set(["etkinlikleri/stand-up","tiyatro","müzik","opera-bale","egitim","etkinlik"])
    event_details=[]
    for cat in categories:
        event_links=get_event_links(cat)
        for event_link in event_links:
            event_details.append(get_event_details(event_link,cat))

    print(event_details)

if __name__ == "__main__":
    scrape_site()