import requests
import json
from datetime import datetime

def get_request(url):
    cookies = {
    'BXID': 'AAAAAAVjmwzRPSkyJ56IiPcINbnNykU57unve+DpWIC2XOIJog==',
    'region': 'TURKIYE',
    'NSC_JOis2ck3bujiltkdwexni4cp4nzpdds': '14b5a3d96abc0d4515cfad42adc64fb98e1180325c55d3cf3c0e93138bbf62bc4ac3fcbd',
    'NSC_JO1afdbkecz2y1mct020ljedxilundm': '30dfa3db6fa389335402468bb6f364589a4c2971d77fad77a0afdbe44a5f235eb9e54986',
    'NSC_tmc_xxx.cjmfujy.dpn_KCptt_Qppm': '30dfa3db5138885a0a4780511bd8db8dc150ff1203fbee2c2b4810cec0e08c5f0aebe849',
    'main_campaign_TURKIYE': 'yes',
    }

    headers = {
        'Accept': 'application/json, text/plain, */*',
        'Accept-Language': 'tr',
        'CHANNEL': 'INTERNET',
        'CPU': '32100',
        'Connection': 'keep-alive',
        'Referer': 'https://www.biletix.com/performance/3OU01/013/TURKIYE/tr',
        'Sec-Fetch-Dest': 'empty',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Site': 'same-origin',
        'Sec-GPC': '1',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36',
        'sec-ch-ua': '"Not A(Brand";v="99", "Brave";v="121", "Chromium";v="121"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
    }
    response = requests.get(
        url,
        cookies=cookies,
        headers=headers,
    )
    if response.status_code!=200:
        return

    obj=json.loads(response.text)
    return obj["data"]

#price section
def get_profiles(event_id):
    link=f'https://www.biletix.com/wbtxapi/api/v1/bxcached/event/getEventPerfProfiles/{event_id}/001/INTERNET/tr'
    profiles=get_request(link)
    if profiles==None:
        return
    return [{"name":pr["profileName"],"id":pr["profileId"]} for pr in profiles]

def get_performances(event_id):
    profiles=get_profiles(event_id)
    
    if profiles==None:
        return
    
    performances=[]
    for profile in profiles:
        link=f'https://www.biletix.com/wbtxapi/api/v1/bxcached/event/getPerformance/{profile["id"]}/001/INTERNET/tr'
        performance=get_request(link)
        performances.append(
            {"name":profile["name"],"id":performance["id"]}
        )
    return performances

def get_event_prices(event_id):
    performances=get_performances(event_id)
    
    if performances==None:
        return
    
    prices=[]
    for performance in performances:
        link=f'https://www.biletix.com/wbtxapi/api/v1/bxcached/event/getPriceInfos/{performance["id"]}/INTERNET/tr'
        categories=get_request(link)
        performance_prices=[]
        for category in categories:
            category_prices=[]
            base_price=category["minPrice"]
            
            for pr in category["concessionInfos"]:
                category_prices.append(
                    {
                        "type":pr["name"],
                        "price":(base_price-pr["amount"])/100
                    }
                )
            performance_prices.append({"category":category["description"],"category_price":category_prices})
        prices.append({"perf_name":performance["name"],"perf_prices":performance_prices})
            
    return prices
    
def get_event_details(id):
    reqUrl = f'https://www.biletix.com/wbtxapi/api/v1/bxcached/event/getEventDetail/{id}/INTERNET/tr'
    details=get_request(reqUrl)
    
    if details == None:
        return
    
    print(details["eventName"])
    if(details["firstPerformanceDate"]!=None and details["lastPerformanceDate"]):
        start = datetime.fromtimestamp(details["firstPerformanceDate"]/1000)
        end = datetime.fromtimestamp(details["lastPerformanceDate"]/1000)
        
        price=get_event_prices(details["eventCode"])
        if price==None:
            return
        
        return {
                "name": details["eventName"],
                "description": details["eventDescription"],
                "links": ["https://www.biletix.com/performance/"+details["eventCode"]+"/001/TURKIYE/tr"],
                "media": ["https://www.biletix.com/static/images/live/event/eventimages/"+details["image"]],
                "category": details["eventCategoryCode"],
                "places": [
                  {
                    "name": details["venueName"],
                    "lat": details["venueLatitude"],
                    "long": details["venueLatitude"],
                    "start_time": start.strftime("%d-%m-%Y %H:%M"),
                    "end_time": end.strftime("%d-%m-%Y %H:%M"),
                    "vendors": [
                      {
                        "name": "biletix",
                        "prices": price
                      }
                    ]
                  }
                ]
            }

def extract_json_from_category(json_string):
    # Find the index of the opening brace '{' of the JSON object
    start_index = json_string.find('{')
    # Find the index of the closing brace '}' of the JSON object
    end_index = json_string.rfind('}')
    
    # Extract the JSON object string
    json_object_string = json_string[start_index:end_index+1]
    
    # Parse the JSON object
    json_object = json.loads(json_object_string)
    
    # Extract and return the 'response' field
    return json_object['response']["docs"]
def get_category_event_details(category="MUSIC",city="Ankara"):
    
    reqUrl = f'https://www.biletix.com/solr/tr/select/?start=0&rows=1300&q=*%3A*&fq=start%3A%5B2024-01-31T00%3A00%3A00Z%20TO%202024-02-14T00%3A00%3A00Z%2B1DAY%5D&sort=start%20asc,%20vote%20desc&=&fq=category:%22{category}%22&fq=city:%22{city}%22&wt=json&indent=true&facet=true&facet.field=category&facet.field=venuecode&facet.field=region&facet.field=subcategory&facet.mincount=1&json.wrf=jQuery111307378109922244118_1706701893629&_=1706701893630'
    if city==-1:
        reqUrl="https://www.biletix.com/solr/tr/select/?start=0&rows=1300&q=*:*&fq=start%3A%5B2024-02-01T00%3A00%3A00Z%20TO%202026-02-01T00%3A00%3A00Z%2B1DAY%5D&sort=score%20desc,start%20asc&&wt=json&indent=true&facet=true&facet.field=category&facet.field=venuecode&facet.field=region&facet.field=subcategory&facet.mincount=1&json.wrf=jQuery111309780652212439103_1706816560308&_=1706816560309"
  
    headersList = {
     "Cookie": "BXID=AAAAAAVjmwzRPSkyJ56IiPcINbnNykU57unve+DpWIC2XOIJog==; NSC_JOis2ck3bujiltkdwexni4cp4nzpdds=6ad0a3de34e437b33c92038b913882ffd69245c6b973cfbcaff03bf9ed847ecba4e644d3; NSC_JO1afdbkecz2y1mct020ljedxilundm=7c02a3dc6fea8cd6fab5cefc3e1063fcb232b272c4fb4a11f96e9a4198f4518b31ea2141; region=TURKIYE; NSC_tmc_xxx.cjmfujy.dpn_KCptt_Qppm=0933a3df83e6cba80c670015bd38edb5075142dbd5ade305e15aa63a5c5f76d86bb34c37; SESSIONID=5e7ed587-a60d-45d2-bafe-abc8ae4a386b; JSESSIONID=45EE39151CBA1CE5B17A2F1DAB90DDD2.btx-web-41; main_campaign_TURKIYE=yes; NSC_tmc_xxx.cjmfujy.dpn_tpmS_Qppm=14b5a3d967abe94b19e18968d458bef41a2dd5f9d1df747242ee39fbfcfbb18f9be07752",
    }
    
    response = requests.get(reqUrl,headers=headersList)
    category_details=extract_json_from_category(response.text)
    category_ids=[event["id"] for event in category_details if "onsale" in  event["status"] ]
    
    events_details=[]
    for id in category_ids:
        if len(id)==5:
            event=get_event_details(id)
            if event != None:
                events_details.append(event)

    return events_details

def scrape_site():
    categories=["MUSIC","SPORT","ART","FAMILY","OTHER"]
    events=[]
    for cat in categories:
        events.extend(get_category_event_details(cat))
        break
    return events
    
if __name__ == "__main__":
    #print(get_category_event_details())
    print(scrape_site())