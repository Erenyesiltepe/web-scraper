from selenium import webdriver
from bs4 import BeautifulSoup

category="MUSIC"
city="ANKARA"

link=f'https://www.biletix.com/search/TURKIYE/tr?category_sb={category}&date_sb=-1&city_sb={city}#!category_sb:MUSIC,city_sb:Ankara'

browser = webdriver.Chrome()
browser.get(link)
txt=browser.page_source
browser.quit()

with open("index.html","w", encoding="utf-8") as f:
    f.write(txt)

# soup=BeautifulSoup(browser.page_source,"lxml")

# events=soup.find_all("div",class_="grid_21 alpha omega listevent searchResultEvent")

# #print(link)
# print("events:\n",events)
# browser.close()