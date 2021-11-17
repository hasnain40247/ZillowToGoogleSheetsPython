import time
from pprint import pprint
from selenium import webdriver
from selenium.webdriver import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.edge.service import Service
import requests
from bs4 import BeautifulSoup
import lxml
zillow_endpoint="https://www.zillow.com"
header = {
    "User-Agent": "",
    "Accept-Language": ""
}

url = "https://www.zillow.com/homes/for_rent/3-_beds/?searchQueryState=%7B%22pagination%22%3A%7B%7D%2C%22mapBounds%22" \
      "%3A%7B%22west%22%3A-122.67605818701172%2C%22east%22%3A-122.1363548178711%2C%22south%22%3A37.646306078671735%2C" \
      "%22north%22%3A37.8614008738129%7D%2C%22mapZoom%22%3A11%2C%22isMapVisible%22%3Atrue%2C%22filterState%22%3A%7B" \
      "%22price%22%3A%7B%22max%22%3A872627%7D%2C%22beds%22%3A%7B%22min%22%3A3%7D%2C%22fore%22%3A%7B%22value%22" \
      "%3Afalse%7D%2C%22mp%22%3A%7B%22max%22%3A3000%7D%2C%22auc%22%3A%7B%22value%22%3Afalse%7D%2C%22nc%22%3A%7B" \
      "%22value%22%3Afalse%7D%2C%22fr%22%3A%7B%22value%22%3Atrue%7D%2C%22fsbo%22%3A%7B%22value%22%3Afalse%7D%2C" \
      "%22cmsn%22%3A%7B%22value%22%3Afalse%7D%2C%22fsba%22%3A%7B%22value%22%3Afalse%7D%7D%2C%22isListVisible%22" \
      "%3Atrue%7D "
response = requests.get(url=url, headers=header)
soup = BeautifulSoup(response.text, "lxml")
list = soup.find(name="ul", class_="photo-cards photo-cards_wow photo-cards_short")
itemlist = list.select(".list-card-price")
price_list = []
for item in itemlist:
    price_list.append(item.get_text().split("/")[0].split("+")[0])

itemlist = list.select(".list-card-addr")
address_list = []
for item in itemlist:
    address_list.append(item.get_text().split("| ")[-1])

itemlist = list.select(".list-card-top a")
link_list = []
for item in itemlist:
    if item["href"][0]=="/":
        link=f"{zillow_endpoint}{item['href']}"
        link_list.append(link)
    else:
        link_list.append(item["href"])

edge_driver = "../msedgedriver.exe"
ser = Service(edge_driver)
op = webdriver.EdgeOptions()
driver = webdriver.Edge(service=ser, options=op)
for addressItem,priceItem,linkItem in zip(address_list,price_list,link_list):
    driver.get("GOOGLE FORM LINK")
    time.sleep(3)
    address=driver.find_element(By.XPATH,'//*[@id="mG61Hd"]/div[2]/div/div[2]/div[1]/div/div/div[2]/div/div['
                                         '1]/div/div[1]/input')
    address.send_keys(f"{addressItem}")
    price=driver.find_element(By.XPATH,'//*[@id="mG61Hd"]/div[2]/div/div[2]/div[2]/div/div/div[2]/div/div[1]/div/div['
                                       '1]/input')
    price.send_keys(f"{priceItem}")
    link=driver.find_element(By.XPATH,'//*[@id="mG61Hd"]/div[2]/div/div[2]/div[3]/div/div/div[2]/div/div[1]/div/div['
                                      '1]/input')
    link.send_keys(f"{linkItem}")
    time.sleep(1)
    button=driver.find_element(By.XPATH,'//*[@id="mG61Hd"]/div[2]/div/div[3]/div[1]/div[1]/div/span/span')
    button.click()
    time.sleep(2)
driver.get("RESPONSES GOOGLE SHEET")

driver.close()