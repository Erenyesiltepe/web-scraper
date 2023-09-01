from playwright.async_api import async_playwright
import asyncio
from bs4 import BeautifulSoup
from datetime import datetime
import googlemaps

def getTime(time_str):
    months={
        "Oca":1,
        "Şub":2,
        "Mar":3,
        "Nis":4,
        "May":5,
        "Haz":6,
        "Tem":7,
        "Ağu":8,
        "Eyl":9,
        "Eki":10,
        "Kas":11,
        "Ara":12,
    }
    time=time_str.split(" ")
    day=int(time[0])
    month=months[time[1]]
    year=int(time[2])
    hour=int(time[3][0:2])
    min=int(time[3][3:5])
    return datetime(year,month,day,hour,min)

async def load_category(category, city, browser):
        #got to the url
        # page = await browser.new_page()
        page=browser
        url=f'https://www.biletix.com/search/TURKIYE/tr?category_sb={category}&date_sb=thisweek&city_sb={city}#!category_sb:{category},city_sb:{city},date_sb:thisweek'
        try:
            await page.goto(url)
            #finds the load button
            try:
                load_more_btn=await page.query_selector("a.search_load_more")
                #clicks the button until it disappears
                count=0
                while await load_more_btn.is_visible():
                    await load_more_btn.click()
                print("Category page is loaded")
            except:
                print("Element not found or there is an another error")
            # await page.close()
            return page
        except:
            print("Category could not be loaded. Url:",url)
            # await page.close()
    
async def load_page(link, browser):
        # page = await browser.new_page()
        page=browser
        try:
            await page.goto(link)
            try:
                show_more_btn= await page.query_selector("a.show-more-button")
                print("show more button is found")
                await show_more_btn.click()
            except:
                print("No show more button")
            print("page is loaded")
            # await page.close()
            return page
        except:
            print("Page could not be loaded. Link:" +link)
            # await page.close()


async def get_event_list(link, browser):
    context= await load_page(link, browser)
    context=await context.content()
    page=BeautifulSoup(context,"html.parser")
    events=page.findAll("btx-list-item",class_="ng-star-inserted")
    event_links=[]
    for event in events:
        still_sale=event.find("mat-basic-chip").text
        if still_sale=="Satışta":
            event_link=event.a["href"]
            event_links.append("https://www.biletix.com"+event_link)
    return event_links

async def get_category_events(browser, category="MUSIC", city="Ankara"):
    context= await load_category(category,city, browser)
    context=await context.content()
    page=BeautifulSoup(context,"html.parser")
    events=page.findAll("div",class_="notliveevent")
    event_links=[]
    for event in events:
        if event.find("span",class_="ln2").text=="Satışta":
            event_link=event.a["href"]
            if event_link[0]=="/":
                # print(event_link)
                #place=event.find("a",class_="searchResultPlace").text+" "+event.find("span",class_="searchResultCity").text
                if "grup" in event_link:
                    event_links.extend(await get_event_list("https://www.biletix.com"+event_link, browser))
                else:
                    event_links.append("https://www.biletix.com"+event_link)
        else:
            print("not on sale")
    return event_links

async def get_event_details(link, category, browser):
    page= await load_page(link, browser)

    heading = await page.inner_text("h1")
    try:
        place = await page.inner_text("a.venue-link.activated.ng-star-inserted span")
        gmaps = googlemaps.Client(key='AIzaSyACez1e0MXMj2eZCPcg7qXsZ3CgDvSofL4')

        # Geocoding an address
        geocode_result = gmaps.geocode(place)
        geocode_result = geocode_result[0]["geometry"]["location"]
        lat=geocode_result["lat"]
        lng=geocode_result["lng"]
    except:
        print("place could not be found")
        place = ""
    print("place:",place,"lat:",lat,"lng:",lng)

    time_elements = await page.query_selector_all("div.perf-date.ng-star-inserted span")
    start_date = await time_elements[0].inner_text()+" "+ await time_elements[1].inner_text()
    end_date = await time_elements[2].inner_text()+" "+await time_elements[3].inner_text()

    head1 = await page.inner_text("h2.heading-medium")
    img = await page.query_selector("div.event-image img")

    img=await img.get_attribute("src")

    context_text = await page.inner_text("div.current-text.ng-tns-c180-9")
    rules = await page.inner_text("section#rules")

    details = head1+"\n"+context_text+"\n"+rules

    return{
        "name":heading,
        "description":details,
        "links":{link},
        "start_date":getTime(start_date),
        "end_date":getTime(end_date),
        "media":{img},
        "latitude":lat,
        "longitude":lng,
        "category":category
    }
    # except:
        # print("Link is wrong: ",link)

async def main():
    async with async_playwright() as p:
        browser = await p.chromium.launch()
        page = await browser.new_page()

        categories=["MUSIC","SPORT","ART","FAMILY","OTHER"]

        event_details=[]
        print(type(event_details))
        events=[]
        for  cat in categories:
            event_links= await get_category_events(page, category=cat)
            events.extend(event_links)
            for i, event_link in enumerate(event_links):
                print(i, event_link)
                event=await get_event_details(event_link,category="cat",browser=page)
                event_details.append(event)
        try:
            import json
            with open("event_details.json", 'w') as json_file:
                json.dump(event_details, json_file)
        except:
            for a in event_details:
                print(a)
        # Close the browser when you're done with it
        await browser.close()


# Run the async main function
asyncio.run(main())
