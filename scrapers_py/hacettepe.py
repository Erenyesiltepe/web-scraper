from bs4 import BeautifulSoup
import requests
from datetime import datetime

def scrape():
    link="https://etkinlikler.hacettepe.edu.tr/"
    p=requests.get(link).text

    page=BeautifulSoup(p,"lxml")
    habers=page.findAll("div",class_="haber_card h-100")

    event_infos=[]

    for haber in habers:
        ahref=link+haber.find("a")["href"].replace("\r\n","")[1::]
        detail=requests.get(ahref).text
        page_obj=BeautifulSoup(detail,"lxml")
        date_and_category=page_obj.find("div",class_="icerik_alt")
        print(date_and_category)
        heading=page_obj.find("div",class_="baslik")
        if heading is not None and date_and_category is not None:
            date_and_category=date_and_category.text.replace(" ","").split("/")
            date=datetime.strptime(date_and_category[0],"%d.%m.%Y")
            heading=heading.text.replace("\r\n"," ")
            content=page_obj.find("div",class_="icerik")
            imglinks=content.find_all("img")
            p_s=content.findAll("p")
            description=""
            for p in p_s:
                description+=p.text
            images=[]
            for img in imglinks:
                images.append(img["src"])

            event_infos.append(
                {
                    "name":heading,
                    "description":description,
                    "links":ahref,
                    "form":{},
                    "start_date":date,
                    "end_date":date,
                    "media":images,#list
                    "qr_code":{},
                    "verification_link":"",
                    "category":date_and_category[1],
                }
            )

    return event_infos

print(scrape())