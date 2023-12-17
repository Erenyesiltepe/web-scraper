from datetime import datetime
import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse, parse_qs

def get_parsed(link):
    headersList = {
    "Accept": "*/*",
     "User-Agent": "Thunder Client (https://www.thunderclient.com)" 
    }   
    payload = ""
    response = requests.request("GET", link, data=payload,  headers=headersList)
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
    headersList = {
     "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
     "Content-Type": "application/x-www-form-urlencoded" 
    }
    payload = f'__RequestVerificationToken=OGTDPYLad2EXfhn8gkeERNJs6qaCfq17QfQFHW7jPave8GnDyWce1HY1KohFyrGT5fHZNg8qKqhp7KLvIyqdHOL_-041&seanceId={seance_id}&IsUser=1'
    response = requests.request("POST", reqUrl, data=payload,  headers=headersList)
    
    #create soup from response
    soup=BeautifulSoup(response.text,"lxml")

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
def get_event_details(link,category):
    soup = get_parsed(link)

    try:
        heading = soup.find("h1").text
        img = soup.select("img.eventPoster")[0]
        img_link = img.get("src")
        desc = soup.select("div.tabContent.flex.directionColumn")[0].text
        rules = soup.select("div.tabContent.row")[0].text
        different_dates = soup.select("div.ed-biletler__sehir__gun")
        events=[]
    except:
        print("Event page could not be loaded")
        return []

    pre = {"title":"", "lng":-1, "lat":-1}

    for date in different_dates:
        try:
            ifsold = date.select("button.seanceSelect")[0].text
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

                    desc=desc+"\n"+rules
                    events.append(
                        {
                            "name":heading,
                            "description":desc,
                            "links":link,
                            "start_date":start_date.strftime("%d-%m-%Y %H:%M"),
                            "end_date":end_date.strftime("%d-%m-%Y %H:%M"),
                            "media":[img_link],
                            "latitude":latitude,
                            "longitude":longitude,
                            "category":category.lower()
                        }
                    )
                    
                except:
                    print("Event location could not found:",address_title)
        except:
            print("Event dates could not found")
  #  print(events)
    print("event is completed")
    return events   
    
categories=set(["etkinlikleri/stand-up","tiyatro","müzik","opera-bale","egitim","etkinlik"])

det=get_event_details("https://biletinial.com/tr-tr/tiyatro/gokhan-unver","tiyatro")
print(det)
print(len(det))