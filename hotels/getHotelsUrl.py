from bs4 import BeautifulSoup
import pandas as pd
from selenium import webdriver
from time import sleep
import csv
import requests

SCARP_URL = " https://fr.hotels.com/search.do?destination-id=10233175&q-check-in=2021-12-29&q-check-out=2021-12-30&q-rooms=1&q-room-0-adults=2&q-room-0-children=0&sort-order=BEST_SELLER"
out_df = pd.DataFrame()

driver = webdriver.chrome.webdriver.WebDriver(executable_path=r'C:/Users/21655/Desktop/chromedriver')
print('opening drive')

search_list_to_prase_link = requests.get(str(SCARP_URL))

hotel_names = []
hotel_price = []

if search_list_to_prase_link.status_code == 200:
    driver.get(search_list_to_prase_link.url)
    print("Scrolling ... ")
    scrolling = 2000
    estimated_pages = 10
    i = 0
    while i <= 20:
        # Scroll down to bottom
        print(i + 1, "iteration")
        print('Scrolling:', scrolling)
        driver.execute_script("window.scrollTo(0," + str(scrolling) + ")")
        if 2 <= i <= 4:
            scrolling += 2600
        elif 5 <= i:
            scrolling += 2800
        else:
            scrolling += 2300
        # Wait to load page
        sleep(15)
        i += 1

    sleep(10)

    print('Getting the web page')
    web_page = driver.page_source
    soup = BeautifulSoup(web_page, 'lxml')
    # Filtering the wanted tags from the fetched html
    hotelNames = soup.find_all("h2", {"class": "_3zH0kn"})
    hotelPrice = soup.find_all("span", {"class": "_2R4dw5"})
    for hotelName in hotelNames:
        hotel_names.append(hotelName.text)
    print(len(hotel_names))
else:
    pass

print("waiting 5 sec")
sleep(5)
print("Closing driver")
driver.close()
driver.quit()

# Saving all the  data in a df
# out_df.to_csv("links_out.csv", encoding='utf-8')
