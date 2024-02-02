from biletinialBs4 import scrape_site as biletinial
from biletixvtwo import scrape_site as biletix
import json

def merge(merged,event):
    name=event["name"] 
    if name in merged:
        merged[name]["places"].extend(event["places"])
    else:
        merged[name]=event

if __name__=="__main__":
    #biletixa=biletix()
    biletiniala=biletinial()
    
    merged={}
    
    for bilet in biletiniala:
        merge(merged,bilet)
    """     for bilet in biletixa:
        merge(merged,bilet) """

    merged_values=list(merged.values())
    with open("test4.json","w",encoding="UTF-8") as jsonfile:
        json.dump(merged_values,jsonfile)