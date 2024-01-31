import requests
import json

def extract_response(json_string):
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

reqUrl = "https://www.biletix.com/solr/tr/select/?start=0&rows=1300&q=*%3A*&fq=start%3A%5B2024-01-31T00%3A00%3A00Z%20TO%202024-02-14T00%3A00%3A00Z%2B1DAY%5D&sort=start%20asc,%20vote%20desc&=&fq=category:%22MUSIC%22&fq=city:%22Ankara%22&wt=json&indent=true&facet=true&facet.field=category&facet.field=venuecode&facet.field=region&facet.field=subcategory&facet.mincount=1&json.wrf=jQuery111307378109922244118_1706701893629&_=1706701893630"

headersList = {
 "GET": "*&fq=start%3A%5B2024-01-31T00%3A00%3A00Z%20TO%202024-02-14T00%3A00%3A00Z%2B1DAY%5D&sort=start%20asc,%20vote%20desc&&fq=category:%22MUSIC%22&fq=city:%22Ankara%22&wt=json&indent=true&facet=true&facet.field=category&facet.field=venuecode&facet.field=region&facet.field=subcategory&facet.mincount=1&json.wrf=jQuery111307378109922244118_1706701893629&_=1706701893630 HTTP/1.1",
 "Cookie": "BXID=AAAAAAVjmwzRPSkyJ56IiPcINbnNykU57unve+DpWIC2XOIJog==; NSC_JOis2ck3bujiltkdwexni4cp4nzpdds=6ad0a3de34e437b33c92038b913882ffd69245c6b973cfbcaff03bf9ed847ecba4e644d3; NSC_JO1afdbkecz2y1mct020ljedxilundm=7c02a3dc6fea8cd6fab5cefc3e1063fcb232b272c4fb4a11f96e9a4198f4518b31ea2141; region=TURKIYE; NSC_tmc_xxx.cjmfujy.dpn_KCptt_Qppm=0933a3df83e6cba80c670015bd38edb5075142dbd5ade305e15aa63a5c5f76d86bb34c37; SESSIONID=5e7ed587-a60d-45d2-bafe-abc8ae4a386b; JSESSIONID=45EE39151CBA1CE5B17A2F1DAB90DDD2.btx-web-41; main_campaign_TURKIYE=yes; NSC_tmc_xxx.cjmfujy.dpn_tpmS_Qppm=14b5a3d967abe94b19e18968d458bef41a2dd5f9d1df747242ee39fbfcfbb18f9be07752",
}

payload = ""

response = requests.request("GET", reqUrl, data=payload,  headers=headersList)

with open("test3.json", 'w',encoding="UTF-8") as json_file:
            json.dump(extract_response(response.text), json_file)