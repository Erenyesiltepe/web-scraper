from playwright.async_api import async_playwright
import asyncio
from datetime import datetime
import time
import googlemaps

async def login(page):
    await page.goto("https://biletinial.com/tr-tr/WebLogin")
    await page.get_by_placeholder("E-Mail").fill("metojal303@nasmis.com")
    await page.get_by_placeholder("Şifre").fill("aA.123456789")
    await page.locator("button.mt-10").click()

async def get_category_events(page, category="sinema"):
    print("Loading",category)
    link=f"https://biletinial.com/tr-tr/{category}"
    await page.goto(link,timeout=0)

    event_div = await page.query_selector("div#kategori__etkinlikler")
    events = await event_div.query_selector_all("h3")
    event_links = []
    for event in events:
        ref = await event.query_selector("a")
        ref = await ref.get_attribute("href")
        if ref is not None:
            event_links.append("https://biletinial.com/"+ref)

    return event_links

async def get_sport_events( page):
    print("Loading sports")
    await page.goto("https://biletinial.com/tr-tr/spor")
    city_options= await page.query_selector("select#slcCity")
    await city_options.select_option(value=["3"])
    events= await page.query_selector_all("div.voleybolDetay_fikstur li")
    event_links=[]
    pre={"heading":"","link":""}
    for event in events:
        if await event.is_visible():
            head = await event.query_selector("p.mb-15 b")
            head = await head.inner_text()
            if head != pre["heading"]:
                event_link = await event.get_attribute("data-link")
                event_links.append("https://biletinial.com"+event_link)

    print("sport is returned")
    return event_links

async def get_standup_events( page):
    print("Loading stand-up")
    await page.goto("https://biletinial.com/tr-tr/etkinlikleri/stand-up")
    city_options= await page.query_selector("select#citySelect")
    await city_options.select_option(value=["3"])
    events= await page.query_selector_all("div.resultsGrid a")

    event_links=[]
    for event in events:
        if await event.is_visible():
            event_link = await event.get_attribute("href")
            event_links.append("https://biletinial.com"+event_link)

    print("standup is returned")
    return event_links


async def get_event_details(link, category, page, location_page):
    print("Trying:",link)
    await page.goto(link, timeout=0)

    try:
        heading = await page.inner_text("h1")
        img = await page.query_selector("img.eventPoster")
        img_link = await img.get_attribute("src")
        desc = await page.inner_text("div.tabContent.flex.directionColumn")
        rules = await page.inner_text("div.tabContent.row")
        different_dates = await page.query_selector_all("div.ed-biletler__sehir__gun")
        events=[]
    except:
        print("Event page could not be loaded")
        return []

    pre = {"title":"", "lng":-1, "lat":-1}

    for date in different_dates:
        try:
            ifsold = await date.query_selector("div.ed-biletler__sehir__gun__fiyat")
            ifsold = await ifsold.inner_text() 
            if ifsold[0] == "B":
                start_date = await date.query_selector("[itemprop='startDate']")
                start_date = await start_date.get_attribute("content")
                start_date = datetime.strptime(start_date, "%Y-%m-%dT%H:%M")
                end_date = await date.query_selector("[itemprop='endDate']")
                end_date = await end_date.get_attribute("content")
                end_date = datetime.strptime(end_date, "%Y-%m-%dT%H:%M")

                address_part = await date.query_selector("[itemprop='location']")
                address_title= await address_part.get_attribute("title")

                try:
                    if address_title != pre["title"]:
                        address_link = await  address_part.get_attribute("href")
                        await location_page.goto("https://biletinial.com/"+address_link)
                        det_address= await location_page.query_selector("div#contact li:nth-of-type(2) p")
                        det_address= await det_address.inner_text()

                        if det_address.strip()=="":
                            geocode_result = gmaps.geocode(address_title)
                        else:
                            geocode_result = gmaps.geocode(det_address)
                            
                        geocode_result = geocode_result[0]["geometry"]["location"]
                        latitude=geocode_result["lat"]
                        longitude=geocode_result["lng"]
                        pre = {"title":address_title, "lng":longitude, "lat":latitude}
                    else:
                        latitude= pre["lat"]
                        longitude= pre["lng"]
                    print("lat:",latitude,"lng:",longitude)
                    desc=desc+"\n"+rules
                    desc=desc.replace("\xa0","").replace("\n\n","\n")
                    events.append(
                    {
                        "name":heading,
                        "description":desc,
                        "links":["link"],
                        "start_date":start_date.strftime("%d-%m-%Y %H:%M"),
                        "end_date":end_date.strftime("%d-%m-%Y %H:%M"),
                        "media":[img_link],
                        "latitude":latitude,
                        "longitude":longitude,
                        "category":category.lower()
                        #place
                        #dateandplace=[{place= lat long date}]
                    }
                    )
                    
                except:
                    print("Event location could not found:",address_title)
        except:
            print("Event dates could not found")
  #  print(events)
    print("event is completed")
    return events

async def get_price(page):
    ticket_details=[]
    tickets=await page.locator("div.yn_koltuksuz__bilet").all()# no seats
    if tickets is None:
        tickets = await page.locator("div.prices item").all()
        for ticket in tickets:
            type= ticket.locator("small")
            type=await type.inner_text()
            price=ticket.locator("strong")
            price=await ticket.inner_text()
            price=float(price.strip()[::-2].replace(",","."))
            print(price," ",type)
    else:
        for ticket in tickets:
            type=  ticket.locator("h5")
            type=await type.inner_text()
            price= ticket.locator("strong")
            price=await price.inner_text()
            price=float(price[1::].replace(",","."))
            ticket_details.append({"type":type,"price":price})
    return ticket_details

async def main():
    async with async_playwright() as p:
        cur= datetime.now()

        browser = await p.chromium.launch(headless=False)
        page = await browser.new_page()
        #location_page = await browser.new_page()
        await login(page)

        """   events_details=[]
        
        categories=["muzik", "tiyatro","opera-bale"]
        for cat in categories:
            event_links=await get_category_events(page, cat)
            for event_link in event_links:
                print("Trying:", event_link)
                events_details.extend(await get_event_details(event_link,cat,page, location_page))
            
        event_links=await get_standup_events(page)
        for event_link in event_links:
            events_details.extend(await get_event_details(event_link,"stand-up",page, location_page))

        event_links=await get_sport_events(page)
        for event_link in event_links:
            events_details.extend(await get_event_details(event_link,"stand-up",page, location_page))

        import json
        with open("biletinial_event_details.json", 'w',encoding="UTF-8") as json_file:
            json.dump(events_details, json_file)

        next= datetime.now()
        dif=next-cur
        print(dif.total_seconds()/60) """
        
        
        """ await page.goto("https://biletinial.com/tr-tr/muzik/jay-jay-johanson")
        button=await page.query_selector("button.seanceSelect")
        await button.click() """
        await page.goto("https://biletinial.com/tr-tr/sinema/napolyon")
        await page.locator("div.yn_cinema button").first.click()
        await get_price(page)

        # Close the browser when you're done with it
        await browser.close()


# Run the async main functionz
gmaps = googlemaps.Client(key='AIzaSyACez1e0MXMj2eZCPcg7qXsZ3CgDvSofL4')
asyncio.run(main())