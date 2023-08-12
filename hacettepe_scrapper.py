from bs4 import BeautifulSoup
import requests

def hacettepe():
    link="https://etkinlikler.hacettepe.edu.tr/"
    p=requests.get(link).text

    page=BeautifulSoup(p,"lxml")
    habers=page.findAll("div",class_="haber_card h-100")

    event_infos=[]

    for haber in habers:
        ahref=haber.find("a")["href"].replace("\r\n","")
        detail=requests.get(link+ahref[1::]).text
        page_obj=BeautifulSoup(detail,"lxml")
        date_and_category=page_obj.find("div",class_="icerik_alt")
        print(date_and_category)
        heading=page_obj.find("div",class_="baslik")
        if heading is not None and date_and_category is not None:
            date_and_category=date_and_category.text.replace(" ","").split("/")
            heading=heading.text.replace("\r\n"," ")
            imglinks=page_obj.find("div",class_="icerik").find_all("img")
            images=[]
            for img in imglinks:
                images.append(img["src"])

            event_infos.append(
                {
                    "heading":heading,
                    "date":date_and_category[0],
                    "category":date_and_category[1],
                    "images":images
                }
            )

    return {"hacettepe":event_infos}
